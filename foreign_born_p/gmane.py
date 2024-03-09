import sqlite3
import time
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import re
from datetime import datetime, timedelta

try:
    import dateutil.parser as parser
except:
    pass

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect("foreign.sqlite")
cur = conn.cursor()

# &limit = how many
# &year =  the specific year of data
baseurl = "https://zircon.datausa.io/api/data?measure=Foreign-Born%20Citizens,Population&drilldowns=Place"

cur.execute(
    """CREATE TABLE IF NOT EXISTS borns
          (id INTEGER UNIQUE, id_place TEXT, place TEXT,
          id_year INTEGER, year TEXT, citiziens INTEGER,
          slug_place TEXT, population INTEGER)"""
)

start = None
cur.execute('SELECT max(id) FROM borns')
try:
    row = cur.fetchone()
    if row is None :
        start = 0
    else:
        start = row[0]
except:
    start = 0

if start is None : start = 0

many = 0
count = 0
fail = 0

while True:
    if (many < 1) :
        conn.commit()
        sval = input('How many reports: ')
        if (len(sval) < 1) : break
        many = int(sval)

    start = start + 1
    cur.execute('SELECT id FROM borns WHERE id=?', (start,))
    try:
        row = cur.fetchone()
        if row is not None : continue
    except:
        row = None
    
    many = many - 1 + start # the number of registers from the user + the current registers
    url = baseurl + '&limit=' + str(many)

    text =  None
    try:
        # Open with a timeout of 30 seconds
        response = urllib.request.urlopen(url, None, 30, context=ctx)
        json = response.read().decode()

        if response.getcode() != 200 :
            print("Error code=", response.getcode(), url)
            break
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page",url)
        print("Error",e)
        fail = fail + 1
        if fail > 5 : break
        continue

    print(url)
    print("json:")
    print(json)
    count += 1
    break