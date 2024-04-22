import sqlite3 as db
import functions

# Name of the artist to be scraped from ticketmaster
ARTIST = "nothing but thieves"

con = db.Connection("data.db")
cur = con.cursor()

# Create table 'events' if it doesn't exists
cur.execute("SELECT name FROM sqlite_master WHERE name=='events'")
result = cur.fetchone()
if result is None:
    cur.execute("CREATE TABLE events(event, date, link)")


scraped = functions.scrap(ARTIST)
events_data, artist_link = functions.extract(scraped)

for event in events_data:
    event_date = event[1]
    cur.execute(f"SELECT date FROM events WHERE date=='{event_date}'")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO events VALUES (?,?,?)", event)
        con.commit()
        
        