from requests import get
from lxml.html import fromstring
from smtplib import SMTP_SSL
from ssl import create_default_context
from dotenv import load_dotenv
from os import getenv


load_dotenv()


def scrap(artist:str):
    """Get the html source from the ticket master webpage, based on the given 
    artist name.

    Args:
        artist (str): Name of artist to q on ticketmaster

    Returns:
        bytes: html source
    """
    url = f"https://www.ticketmaster.ca/search?q={artist}"
    response = get(url)
    source = response.content
    return source


def extract(source:bytes):
    """Extracts events data from the given html source.

    Args:
        source (bytes): html source

    Returns:
        tuple[list, str]: List of tuples with the events extracted, 
        str of artist ticketmaster link. 
    """
    events_data = []
    xpath_index = 1
    webpage = fromstring(source)
    
    while True:
        # Use xpaths to extract the events data from the html source,
        # the try except is used to know when there is no more data.
        try:
            event = webpage.xpath("//*[@id='pageInfo']/div[2]/div[1]/div[2]"\
                f"/div/ul/li[{str(xpath_index)}]/div[1]/div/div[3]/a/span/span"\
                "/span[2]/text()")[0]
            date = webpage.xpath("//*[@id='pageInfo']/div[2]/div[1]/div[2]"\
                f"/div/ul/li[{str(xpath_index)}]/div[1]/div/div[3]/a/span/span"\
                "/span[2]/span/text()")[0]
            link = webpage.xpath("//*[@id='pageInfo']/div[2]/div[1]/div[2]"\
                f"/div/ul/li[{str(xpath_index)}]/div[1]/div/div[3]/a/@href")[0]
            events_data.append((event, date, link))
            xpath_index += 1
        except IndexError:
            break
    artist_link = webpage.xpath("//*[@id='main-content']/div/div[1]/div[2]"\
        "/div/ul/li/a/@href")[0]
    
    return events_data, artist_link


def send_email(data:list, artist:str, artist_link:str):
    """Sends an email with the new events data with a formatted message (body).

    Args:
        data (list): List of tuples with the events data.
        artist (str): Name of the artist.
        artist_link (str): Ticketmaster link of the artist.
    """
    sender = getenv("sender")
    receiver = getenv("receiver")
    password = getenv("sender_pass")
    
    # Format the given events data to construct the email message.
    formatted_events = [f"{event[0]} - {event[1]}\nBuy tickets! : {event[2]}\n\n"
                        for event in data]
    formatted_events = "".join(formatted_events)
    artist_link = f"https://www.ticketmaster.ca{artist_link}"
    
    message = f"Subject: Hey, new {artist.title()} upcoming event!\n\n"\
        f"{formatted_events}"\
        f"Or check it on the ticketmaster webpage: {artist_link}"
      
    with SMTP_SSL("smtp.gmail.com", context=create_default_context()) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.encode("utf-8"))
    

def check_artist(source:bytes):
    """Checks the validity of the given artist name

    Args:
        source (bytes): html source

    Returns:
        bool: If the artist name is valid returns True, otherwise returns False
    """
    webpage = fromstring(source)
    
    # Try except block is used to know if the given artist name is valid.
    try:
        webpage.xpath("//*[@id='main-content']/div/div[1]/div[2]"\
            "/div/ul/li/a/@href")[0]
    except IndexError:
        return False
    
    return True

def dummy_email():
    """
    Sens a simple email to let the user know when the given artist name is 
    not valid.
    """
    sender = getenv("sender")
    receiver = getenv("receiver")
    password = getenv("sender_pass")
    
    message = "Subject: Ticketmaster scraper: wrong artist name!\n\n"\
        "Hey buddy!,\n\n Please check the given name for the artist on the "\
        "ticketmaster scraper. You can use this url 'https://www.ticketmaster"\
        ".ca/search?q=' to check for a valid artist name\n\nGood luck!"
      
    with SMTP_SSL("smtp.gmail.com", context=create_default_context()) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.encode("utf-8"))
    
    
if __name__ == "__main__":
    scraped = scrap("nothing but thieves")
    extracted, extracted_link = extract(scraped)
    print(extracted)
    send_email(extracted, "nothing but thieves", extracted_link)