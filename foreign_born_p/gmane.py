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
baseurl = "https://zircon.datausa.io/api/data?measure=Foreign-Born%20Citizens,Population&drilldowns=State"

cur.execute(
    """CREATE TABLE IF NOT EXISTS borns
          (id INTEGER PRIMARY KEY, id_state TEXT, state TEXT,
          id_year INTEGER, year TEXT,
          slug_state TEXT, population INTEGER)"""
)

years = None
cur.execute("SELECT DISTINCT id_year FROM borns")

years = [i[0] for i in cur.fetchall()]

many = 0
count = 0
fail = 0

while True:
    if many < 1:
        conn.commit()
        if len(years) > 0:
            print("years saved: ", years)
        sval = input("Choose the Year of the report (From 2013 to 2021): ")
        if len(sval) < 1:
            break

        ask = False

        while True:
            if ask:
                sval = input("Choose the Year of the report (From 2013 to 2021): ")
            ask = True
            try:
                sval = int(sval)
            except:
                print("\nPlease, write a number.\n")
                continue
            if sval < 2013 or sval > 2021:
                print("The year is out of range.")
            elif sval in years:
                print("We already have the data from that year.")
            else:
                break
            # sval = input("Choose the Year of the report (From 2013 to 2021): ")
        many = sval

    url = baseurl + "&year=" + str(many)

    text = None
    try:
        # Open with a timeout of 30 seconds
        print("Loading...")
        response = requests.get(url)
        json = response.json()
        years.append(many)

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
    print(url, len(json))

    # ! [FIX] we are doing more iterations than necessary

    for idx, born in enumerate(json["data"]):
        count += 1
        cur.execute(
            """INSERT OR IGNORE INTO borns (id_state, state, id_year, year,
                slug_state, population) VALUES (? , ?, ?, ?, ?, ?)""",
            (
                born.get("ID State"),
                born.get("State"),
                born.get("ID Year"),
                born.get("Year"),
                born.get("Slug State"),
                born.get("Population"),
            ),
        )

        # acomulate some date before insert them into the DB
        if count % 50 == 0:
            conn.commit()
        if count % 100 == 0:
            time.sleep(1)

    many = 0


conn.commit()
cur.close()
