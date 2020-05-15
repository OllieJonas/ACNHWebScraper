from scrapers import artscraper as art, bugscraper as bug, fishscraper as fish, fossilscraper as fossil, \
     villagerscraper as villager, furniturescraper as furniture, diyscraper as diy
import util
import os


def make_dirs():
    try:
        os.mkdir("data")
        os.mkdir("data/diy")
        os.mkdir("data/furniture")
        os.mkdir("data/museum")
    except OSError:
        print("Unable to create directory!")


if __name__ == "__main__":

    make_dirs()
    
    # Art
    util.dump(art.scrape(art.PAINTING), 'museum/paintings.json')
    util.dump(art.scrape(art.SCULPTURE), 'museum/sculptures.json')

    # Museum
    util.dump(bug.scrape(), 'museum/bugs.json')
    util.dump(fish.scrape(), 'museum/fish.json')
    util.dump(fossil.scrape_multipart(), 'museum/multipart.json')
    util.dump(fossil.scrape_standalone(), 'museum/standalone.json')

    # Villagers
    util.dump(villager.scrape(), 'villagers.json')

    # Furniture
    util.dump(furniture.scrape("housewares"), "furniture/housewares.json")
    util.dump(furniture.scrape("misc"), "furniture/misc.json")
    util.dump(furniture.scrape("wallmounted"), "furniture/wallmounted.json")
    util.dump(furniture.scrape("wallpaper"), "furniture/wallpaper.json")
    util.dump(furniture.scrape("flooring"), "furniture/flooring.json")
    util.dump(furniture.scrape("rugs"), "furniture/rugs.json")

    # DIY
    util.dump(diy.scrape("tools"), "diy/tools.json")
    util.dump(diy.scrape("housewares"), "diy/housewares.json")
    util.dump(diy.scrape("misc"), "diy/misc.json")
    util.dump(diy.scrape("equipment"), "diy/equipment.json")
    util.dump(diy.scrape("other"), "diy/other.json")
    util.dump(diy.scrape("wallmounted"), "diy/wallmounted.json")
    util.dump(diy.scrape("wallpaper_rugs_flooring"), "diy/wallpaper.json")

