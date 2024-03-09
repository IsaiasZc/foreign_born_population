import sqlite3
import time
import ssl
import requests
from datetime import datetime, timedelta
import gzip


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
          (id INTEGER PRIMARY KEY, id_place TEXT, place TEXT,
          id_year INTEGER, year TEXT, citiziens INTEGER,
          slug_place TEXT, population INTEGER)"""
)

start = None
cur.execute("SELECT max(id) FROM borns")
try:
    row = cur.fetchone()
    if row is None:
        start = 0
    else:
        start = row[0]
except:
    start = 0

if start is None:
    start = 0

many = 0
count = 0
fail = 0

while True:
    if many < 1:
        conn.commit()
        sval = input("How many reports: ")
        if len(sval) < 1:
            break
        many = int(sval)

    url = baseurl + "&limit=" + str(many + start)

    text = None
    try:
        # Open with a timeout of 30 seconds
        print("Loading...")
        response = requests.get(url)
        json = response.json()

    except KeyboardInterrupt:
        print("")
        print("Program interrupted by user...")
        break
    except Exception as e:
        print("Unable to retrieve or parse page", url)
        print("Error", e)
        fail = fail + 1
        if fail > 5:
            break
        continue

    # json = eval(json)
    count += 1
    print(url, len(json))

    # ! [FIX] we are doing more iterations than necessary

    for idx, born in enumerate(json["data"]):
        if idx < start : continue
        cur.execute(
            """INSERT OR IGNORE INTO borns (id_place, place, id_year, year,
                     citiziens, slug_place, population) VALUES (? , ?, ?, ?, ?, ?, ?)""",
            (
                born.get('ID Place'),
                born.get('Place'),
                born.get('ID Year'),
                born.get('Year'),
                born.get('Foreign-Born Citizens'),
                born.get('Slug Place'),
                born.get('Population'),
            ),
        )

        # acomulate some date before insert them into the DB
        if count % 50 == 0 : conn.commit()
        if count % 100 == 0 : time.sleep(1)
    
    start = start + many
    many = 0
        

conn.commit()
cur.close()