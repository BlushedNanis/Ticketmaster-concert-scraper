import sqlite3 as db
import backend

# Name of the artist to be scraped from ticketmaster
ARTIST = "nothing but thugs"

# Get data from ticket master
scraped = backend.scrap(ARTIST)

artist_check = backend.check_artist(scraped)

if artist_check == True:
    # If th given artist name is valid the scrip will run normally, otherwise
    # it will send an email to let the user know that the name is not valid.
    con = db.Connection("data.db")
    cur = con.cursor()

    # Create table 'events' if it doesn't exists
    cur.execute("SELECT name FROM sqlite_master WHERE name=='events'")
    result = cur.fetchone()
    if result is None:
        cur.execute("CREATE TABLE events(event, date, link)")

    #Extract events and artist information from the source
    events_data, artist_link = backend.extract(scraped)

    # List to contain new events
    events_to_mail = []

    # Save new events into db 
    for event in events_data:
        event_date = event[1]
        cur.execute(f"SELECT date FROM events WHERE date=='{event_date}'")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO events VALUES (?,?,?)", event)
            con.commit()
            events_to_mail.append(event)

    # Send email if there is new events
    if len(events_to_mail) > 0:
        backend.send_email(events_to_mail, ARTIST, artist_link)
        
else:
    backend.dummy_email()