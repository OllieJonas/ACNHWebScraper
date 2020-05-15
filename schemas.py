def fish(name, image_link, price, location, shadow_size, times, northern_months,
         southern_months):
    return {
        "name": name,
        "imageLink": image_link,
        "price": price,
        "location": location,
        "shadowSize": shadow_size,
        "times": times,
        "northern_months": northern_months,
        "southern_months": southern_months,
    }


def bug(name, image_link, price, location, times, northern_months, southern_months):
    return {
        "name": name,
        "imageLink": image_link,
        "price": price,
        "location": location,
        "times": times,
        "northern_months": northern_months,
        "southern_months": southern_months,
    }


def art(name, real_image_link, fake_image_link, description):
    return {
        "name": name,
        "realImage": real_image_link,
        "fakeImage": fake_image_link,
        "description": description
    }


def standalone_fossil(name, image_link, price):
    return {
        "name": name,
        "imageLink": image_link,
        "price": price,
    }


def multipart_fossil(name, price, parts):
    return {
        "name": name,
        "price": price,
        "parts": parts
    }


def villager(name, image_link, personality, gender, species, birthday, catchphrase):
    return {
        "name": name,
        "imageLink": image_link,
        "personality": personality,
        "gender": gender,
        "species": species,
        "birthday": birthday,
        "catchphrase": catchphrase
    }


def furniture_rug(name, image_link, buy_price, sell_price, source, size):
    return {
        "name": name,
        "imageLink": image_link,
        "buyPrice": buy_price,
        "sellPrice": sell_price,
        "source": source,
        "size": size
    }


def furniture_house(name, image_link, buy_price, sell_price, source):
    return {
                "name": name,
                "imageLink": image_link,
                "buyPrice": buy_price,
                "sellPrice": sell_price,
                "source": source
            }


def furniture_detailed(name, image_link, buy_price, sell_price, source, variations, customize, size):
    return {
                "name": name,
                "imageLink": image_link,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "source": source,
                "variations": variations,
                "customization": customize,
                "size": size
            }