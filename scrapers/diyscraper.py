import requests
from bs4 import BeautifulSoup
import schemas
import re

urls = {
    "tools": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Tools",
    "housewares": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Housewares",
    "misc": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Miscellaneous",
    "equipment": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Equipment",
    "other": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Other",
    "wallmounted": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wall-mounted",
    "wallpaper_rugs_flooring": "https://animalcrossing.fandom.com/wiki/DIY_recipes/Wallpaper,_rugs_and_flooring",
}


def scrape(key):
    response = requests.get(urls.get(key))
    rep_text = response.text
    response.close()
    soup = BeautifulSoup(rep_text, 'html.parser')

    tables = soup.find_all("table", {"class": "sortable"})

    for tr in tables[0].find_all("tr")[1:]:
        children = tr.find_all("td")

        name = strip(children[0].text)
        image_link = children[1].a['href']
        materials = materials_from_str(strip(children[2].text))
        size = size_from_url(children[3].a['href'])
        source = strip(children[4].text)

        item = {
            "name": name,
            "type": tool_type_from_name(name),
            "imageLink": image_link,
            "materials": materials,
            "size": size,
            "source": source
        }
        print(item)
        pass


def materials_from_str(string):
    return string


def tool_type_from_name(string):
    return string.split()[0] if len(string.split()) < 2 else ' '.join(map(str, string.split()[1:])).capitalize()


def size_from_url(param):
    return [float(x) for x in re.search("[0-5][.][05][x][0-5][.][05]", param).group(0).split("x")]


def strip(string):
    return string.replace("\n", "").strip()


if __name__ == "__main__":
    print(scrape("housewares"))
    print(materials_from_str("x5 tree branchx3 star fragment"))
