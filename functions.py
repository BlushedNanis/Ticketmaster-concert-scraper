from requests import get
from lxml.html import fromstring
from smtplib import SMTP_SSL
from ssl import create_default_context
from dotenv import load_dotenv
from os import getenv


load_dotenv()


def scrap(artist:str):
    url = f"https://www.ticketmaster.ca/search?q={artist}"
    response = get(url)
    source = response.content
    return source

def extract(source:bytes):
    events_data = []
    xpath_index = 1
    webpage = fromstring(source)
    while True:
        try:
            event = webpage.xpath(f'//*[@id="pageInfo"]/div[2]/div[1]/div[2]/div/ul/li[{str(xpath_index)}]/div[1]/div/div[3]/a/span/span/span[2]/text()')[0]
            date = webpage.xpath(f'//*[@id="pageInfo"]/div[2]/div[1]/div[2]/div/ul/li[{str(xpath_index)}]/div[1]/div/div[3]/a/span/span/span[2]/span/text()')[0]
            link = webpage.xpath(f'//*[@id="pageInfo"]/div[2]/div[1]/div[2]/div/ul/li[{str(xpath_index)}]/div[1]/div/div[3]/a/@href')[0]
            events_data.append((event, date, link))
            xpath_index += 1
        except IndexError:
            break
    artist_link = webpage.xpath('//*[@id="main-content"]/div/div[1]/div[2]/div/ul/li/a/@href')[0]
    return events_data, artist_link
  
def send_email(data:list, artist:str, artist_link:str):
    sender = getenv("sender")
    receiver = getenv("receiver")
    password = getenv("sender_pass")
      
    formatted_events = [f"{event[0]} - {event[1]}\nBuy tickets! : {event[2]}\n\n" for event in data]
    formatted_events = "".join(formatted_events)
    message = f"Subject: Hey, new {artist.title()} upcoming event!\n\n"\
        f"{formatted_events}"\
        f"Or check it on the ticketmaster webpage: https://www.ticketmaster.ca{artist_link}"
      
    with SMTP_SSL("smtp.gmail.com", context=create_default_context()) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
    
if __name__ == "__main__":
    scraped = scrap("nothing but thieves")
    extracted, extracted_link = extract(scraped)
    print(extracted)
    send_email(extracted, "nothing but thieves", extracted_link)