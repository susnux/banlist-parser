#/usr/bin/env python3

# Copyright (c) 2015, Ferdinand Thiessen (susnux) <rpm@fthiessen.de>
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import urllib.request
import re, errno, sys, datetime
import dateutil.parser
from bs4 import BeautifulSoup

#URL and settings
list_url = "http://cursedearth.us/modules.php?name=Bans&pagenum="
xml_file = "/home/user/somepath/admin.xml"
bans = []

# Error Handling
def error(msg):
	print(msg)
	sys.exit(errno.EREMOTEIO)

#get number of sub sites:
print("Load bans from website")
print("Progress:   0%",end="",flush=True)
h = urllib.request.urlopen(list_url + "1")
content = h.read().decode('iso-8859-1')
h.close()
match = re.search("(?<=<td> Page 1)(.*?)(?=<\/td>)", content)
if match:
	match = re.search("(?<=>)([0-9]?)(?=<\/a>[ ]*$)", match.group(0))
	if match:
		pages = int(match.group(0))
	else:
		error("Error 0x12: Can not read number of pages")
else:
	error("Error 0x11: Can not read pagesize")
pages = int(match.group(0))
del match
print("\rProgress:   %.2f%%" % (100/(pages+1)),end="",flush=True)

def processBans(con):
	match = re.search(r"(?<=<h1>Ban End Date<\/td><td><h1>Ban Date - Reason <\/td><\/tr>)([\s\S]*?)(?=<\/table>)", con)
	if not match:
		error("Error 0x21: Can not read page")
	lines = re.finditer(r"(?<=<tr>)([\s\S]*?)(?=<\/tr>)", match.group(0))
	if not lines:
		error("Error 0x22: Can not read lines")
	for line in lines:
		match = re.search(r"(?<=page=player&id=)([a-zA-z0-9]*?)(?=\">)", line.group(0))
		player = match.group(0)
		del match
		match = re.search(r"Permanent" , line.group(0))
		if match:
			date = datetime.datetime(2114, 3, 20, 11, 13, 37)
		else:
			match = re.search(r"(?<=>)([0-9]{4}-[0-9]{2}-[0-9]{2}?)(?=<\/td>)", line.group(0))
			date = dateutil.parser.parse(match.group(0))
		global bans
		bans.append((player, date.strftime("%m/%d/%Y %I:%M:%S %p")))

#get bans
for page in range(1, pages + 1):
	h = urllib.request.urlopen(list_url + str(x))
	processBans(h.read().decode('iso-8859-1'))
	h.close()
	print("\rProgress:   %.2f%%" % ((x+1) * 100/(pages+1)),end="",flush=True)

#write xml
print("\nWrite to disk")
f = open(xml_file, 'r+')
soup = BeautifulSoup(f.read())
bl_tag = soup.blacklist
bl_tag.clear()

for ban in bans:
	new_tag = soup.new_tag("blacklisted", steamID=ban[0], unbandate=ban[1])
	bl_tag.append(new_tag)

f.seek(0)
f.write(soup.prettify())
f.truncate()
f.close()
print("All done")