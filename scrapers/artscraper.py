import requests
from bs4 import BeautifulSoup
import schemas
import re


PAINTING = 0
SCULPTURE = 1


# 0 = Painting, 1 = Sculpture
def scrape(index):
    print("Performing Art Scrape for " + str(index) + "...")
    url = "https://animalcrossing.fandom.com/wiki/Art_(New_Horizons)"
    response = requests.get(url)
    rep_text = response.text
    response.close()

    soup = BeautifulSoup(rep_text, 'html.parser')
    table = soup.find_all('table')

    items = []

    for tr in table[index].find_all("tr")[1:]:
        children = tr.find_all("td")

        name = children[0].a.text
        real_link = ""
        fake_link = ""
        description = ""

        if children[1].a is not None:
            fake_link = children[1].a['href']

        if children[2].a is not None:
            real_link = children[2].a['href']

        if children[3] is not None:
            description = re.sub("\n", "", children[3].text).strip()

        art = schemas.art(
            name,
            real_link,
            fake_link,
            description
        )

        items.append(art)

    return items
