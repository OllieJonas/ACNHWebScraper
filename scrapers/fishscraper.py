import schemas
import util


def scrape():
    print("Performing fish scrape...")
    csv, urls = util.parse_museum("https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)", False)
    count = 0
    items = []
    for entry in csv:
        split = entry.split(",")

        if len(split) > 14:
            fish = schemas.fish(
                split[1],
                urls[count],
                split[3],
                split[4],
                split[5],
                util.time_from_str(split[6]),
                util.dates_from_ticks(split[7:15]),
                util.to_southern_months(util.dates_from_ticks(split[7:15]))
            )
            # print(fish)
            items.append(fish)
            count += 1

    return items
