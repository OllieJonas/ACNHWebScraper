import requests
from bs4 import BeautifulSoup

import schemas


def scrape():
    print("Performing villagers scrape...")
    url = "https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)"
    response = requests.get(url)
    rep_text = response.text
    soup = BeautifulSoup(rep_text, 'html.parser')
    table = soup.find_all("table", {"class": "sortable"})

    items = []

    for tr in table[0].find_all("tr")[1:]:
        children = tr.find_all("td")

        name = children[0].a.text
        link = children[1].a['href']
        personality = children[2].text.strip().split()[1]
        gender = gender_from_char(children[2].text.strip().split()[0])
        species = children[3].text.strip()
        birthday = children[4].text.strip()
        catchphrase = children[5].text.strip().replace("\"", "")

        item = schemas.villager(name, link, personality, gender, species, birthday, catchphrase)

        items.append(item)

    return items


def gender_from_char(char):
    if char == '♂':
        return "Male"
    elif char == '♀':
        return "Female"
    else:
        return "Not Specified"
