from scrapers import artscraper as art, bugscraper as bug, fishscraper as fish, fossilscraper as fossil, \
    villagerscraper as villager, furniturescraper as furniture
import util


if __name__ == "__main__":

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
    util.dump(furniture.scrape("housewares"), "furniture/furniture_housewares.json")
    util.dump(furniture.scrape("misc"), "furniture/furniture_misc.json")
    util.dump(furniture.scrape("wallmounted"), "furniture/furniture_wallmounted.json")
    util.dump(furniture.scrape("wallpaper"), "furniture/furniture_wallpaper.json")
    util.dump(furniture.scrape("flooring"), "furniture/furniture_flooring.json")
    util.dump(furniture.scrape("rugs"), "furniture/furniture_rugs.json")

