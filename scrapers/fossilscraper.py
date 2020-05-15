import re

import requests
from bs4 import BeautifulSoup

import schemas
import util
from scrapers import Scraper


def scrape_standalone():
    print("Performing standalone fossil scrape...")
    csv, urls = Scraper.parse_museum("https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)", False)
    items = []
    count = 0
    for item in csv:
        split = item.split(",")
        if len(split) > 2:
            fossil = schemas.standalone_fossil(
                split[1],
                urls[count],
                util.strip_bells(''.join(split[3:])),
            )

            count += 1
            items.append(fossil)

    return items


def scrape_multipart():
    print("Performing multipart fossil scrape...")
    url = "https://animalcrossing.fandom.com/wiki/Fossils_(New_Horizons)"
    response = requests.get(url)
    rep_text = response.text
    response.close()

    soup = BeautifulSoup(rep_text, 'html.parser')
    table = soup.find_all('table', {"class": "sortable"})[1]
    children = table.find_all("tr")

    items = []
    parts = []
    curr_name = ""
    curr_price = 0

    for child in children[1:]:

        info = re.sub("\n", "", child.text).strip().split("   ")
        if len(info) < 2:
            if curr_name != "":
                item = schemas.multipart_fossil(curr_name, curr_price, parts)
                items.append(item)
            curr_name = info[0]
            curr_price = 0
            parts = []
        else:
            name = ""
            link = ""
            price = 0

            # Link
            td = child.find_all("td")

            if len(td) > 0:
                href = td[1].find_all("a")
                if len(href) > 0:
                    link = href[0]['href']

            # Name and Price
            if len(child.text) > 0:
                name = info[0]
                price = util.strip_bells(info[1])

            part = schemas.standalone_fossil(name, link, price)
            curr_price += price
            parts.append(part)

    items.append(schemas.standalone_fossil(curr_name, curr_price, parts))  # Final entry

    return items
