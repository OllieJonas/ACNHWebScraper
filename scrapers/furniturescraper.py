import requests
from bs4 import BeautifulSoup
import util
import schemas

import re

URLS = {
    "housewares": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Housewares",
    "misc": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Miscellaneous",
    "wallmounted": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Wall-mounted",
    "wallpaper": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Wallpaper",
    "flooring": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Flooring",
    "rugs": "https://animalcrossing.fandom.com/wiki/Furniture_(New_Horizons)/Rugs"
}


def scrape(key):
    print("Performing " + key + " (Furniture) scrape...")
    if key in ["housewares", "miscellaneous", "wallmounted", "misc"]:
        return detailed_scrape(URLS.get(key))
    elif key in ["wallpaper", "flooring"]:
        return house_scrape(URLS.get(key))
    elif key in ["rugs"]:
        return rug_scrape(URLS.get(key))
    else:
        raise ValueError("Invalid key!")


def detailed_scrape(url):
    response = requests.get(url)
    rep_text = response.text
    response.close()
    soup = BeautifulSoup(rep_text, 'html.parser')
    tables = soup.find_all("tr")

    items = []

    for table in tables[3:]:
        cells = table.find_all("td")
        size = len(cells)

        if size > 6:
            name = strip(cells[1].text)
            image_link = cells[0].a['href']
            buy_price = strip_cash(cells[2].text)
            sell_price = strip_cash(cells[3].text)

            source = "Unknown"

            if cells[4].a:
                source = process_source(cells[4].a['href'])

            variations = process_variations(strip(cells[5].text))
            customize = process_customizations(strip(cells[6].text))

            size = "Unknown"

            if len(cells) > 7:
                size = size_from_url(cells[7].a['href'])

            item = schemas.furniture_detailed(
                name,
                image_link,
                buy_price,
                sell_price,
                source,
                variations,
                customize,
                size
            )

            items.append(item)
    return items


def house_scrape(url):
    response = requests.get(url)
    rep_text = response.text
    response.close()
    soup = BeautifulSoup(rep_text, 'html.parser')
    tr = soup.find_all("tr")

    items = []

    for entry in tr[1:]:
        children = entry.find_all("td")
        if len(children) > 4:
            name = strip(children[1].text)
            image_link = children[0].a['href']
            buy_price = strip_cash(children[2].text)
            sell_price = strip_cash(children[3].text)

            source = "Unknown"
            if children[4].a:
                source = process_source(children[4].a['href'])

            item = schemas.furniture_house(
                name,
                image_link,
                buy_price,
                sell_price,
                source
            )

            items.append(item)
    return items


def rug_scrape(url):
    response = requests.get(url)
    rep_text = response.text
    response.close()

    soup = BeautifulSoup(rep_text, 'html.parser')
    tr = soup.find_all("tr")

    items = []

    for entry in tr:
        children = entry.find_all("td")
        if len(children) > 4:
            image_link = children[0].a['href']
            name = strip(children[1].text)
            buy_price = strip_cash(children[2].text)
            sell_price = strip_cash(children[3].text)

            source = "Unknown"

            if children[4].a:
                source = process_source(children[4].a['href'])

            size = "Unknown"

            if len(children) > 5 and children[5].a['href']:
                size = size_from_url(children[5].a['href'])

            item = schemas.furniture_rug(
                name,
                image_link,
                buy_price,
                sell_price,
                source,
                size
            )

            items.append(item)

    return items


def process_variations(string):
    typ = string.split(":")

    options = "N/A"

    if len(typ) > 1:
        options = [x.lstrip() for x in typ[1].split(",")]

    return {
        "type": typ[0],
        "options": options
    }


def process_customizations(string):
    if string == "N/A":
        return string

    kits_split = string.split("(")
    kits = kits_split[1].replace(")", "").strip()

    if kits != "NA":
        kits = int(kits)

    types_split = kits_split[0].split(":")

    type = types_split[0]
    options = "N/A"

    if len(types_split) > 1:
        options = [x.lstrip() for x in types_split[1].split(",")]

    customize = {
        "type": type,
        "kits": kits,
        "options": options
    }
    return customize


def strip_cash(string):
    return re.sub("[\n,]", "", string).strip()


def process_source(raw_str):
    replacements = {
        "/wiki/": "",
        "%27": "\'",
        "_": " "
    }
    return util.multiple_replace(replacements, raw_str)


def size_from_url(param):
    return [float(x) for x in re.search("[0-5][.][05][x][0-5][.][05]", param).group(0).split("x")]


def strip(string):
    return string.replace("\n", "").strip()

