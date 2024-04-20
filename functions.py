from requests import get
from selectorlib import Extractor


def scraper(band):
    url = f"https://www.ticketmaster.ca/search?q={band}"
    response = get(url)
    source = response.text
    return source

def extract(source):
    extractor = Extractor.from_yaml_file("")