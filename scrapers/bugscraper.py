from scrapers import Scraper
import util
import schemas


def scrape():
    print("Performing bug scrape...")

    csv, urls = Scraper.parse_museum("https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)", True)

    count = 0
    items = []
    for entry in csv:
        split = entry.split(",")

        if len(split) > 14:
            bug = schemas.bug(
                split[1],
                urls[count],
                split[3],
                split[4],
                util.time_from_str(split[5]),
                util.dates_from_ticks(split[6:14]),
                util.to_southern_months(util.dates_from_ticks(split[6:14]))
            )
            # print(fish)
            items.append(bug)
            count += 1

    return items
