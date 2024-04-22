from requests import get
from lxml.html import fromstring


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
    

print(extract(scrap("nothing but thieves")))