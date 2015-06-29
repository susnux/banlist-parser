# banlist-parser
Parses global ban list to protect your 7 Days to die server of getting hacked by evil players.

## Usage
Simply change the path to your admin.xml in the bapa.py file and save the file.

Then execute it: `./bapa.py`

**Hint:**

You can make your life easier by adding a cron job for ban list parsing so the blacklist get updated every 24h.

Open a terminal and type:
`crontab -e`
add a new line:

`0 0 * * *       /path/to/bapa.py > /dev/null`

Save crontab, finished.

# Dependencies
1. python 3.0 or higher
2. python3-beautifulsoup4
3. python-urllib3
