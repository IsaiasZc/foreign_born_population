import sqlite3
import string

conn = sqlite3.connect("foreign.sqlite")
cur = conn.cursor()

cur.execute("SELECT * FROM borns")

fhand = open("gborns.js", "w")
fhand.write("export  const gborns = [")
first = True

keys = [
    {"key": "id", "string": False},
    {"key": "id_state", "string": True},
    {"key": "state", "string": True},
    {"key": "id_year", "string": False},
    {"key": "year", "string": True},
    {"key": "slug_state", "string": True},
    {"key": "population", "string": False},
]

for born in cur:
    print(born)
    if not first:
        fhand.write(",\n")
    first = False
    stri = (
        "{"
        + ",".join(
            ""
            + keys[idx].get("key")
            + ":"
            + ('"' if keys[idx].get("string") else "") # add " if string
            + str(val)
            + ('"' if keys[idx].get("string") else "") # add " if string
            for idx, val in enumerate(born)
        )
        + "}"
    )
    fhand.write(stri)

fhand.write("\n];\n")
fhand.write("\nexport default gborns")
fhand.close()

print("gborns.js generated.")
