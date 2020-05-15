import json
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd


def is_tick(char):
    """
    Boolean returning whether a particular character is a tick char

    :param char: Char in question
    :return: Whether it's a tick
    """
    return char == "✓"


def dates_from_ticks(items):
    """
    Converts a list of ticks into a list of months

    :param items: The list of ticks
    :return: The appropriate months
    """
    months = []

    for i in range(0, len(items)):
        if is_tick(items[i]):
            months.append(i + 1)

    return months


def strip_bells(text):
    """
    Removes any extra characters in something to do with bells, and then converts to an integer.
    For example: 1,000 Bells becomes 1000

    :param text: The text containing the bells
    :return: Stripped version of bells.
    """
    return int(re.sub("[,\"]|[Bells]", "", text))


def pretty_print(text):
    """
    Prints any JSON text in an indented fashion.

    :param text: The text to print
    """
    print(json.dumps(text, indent=4, sort_keys=False))


def time_from_str(time_range):
    """
    Takes a time range as a string formatted according to the AC Wiki timestamps, and returns a list of given times
    within that range including the start and end times.
    For example, the time range 10PM - 4AM becomes: [22, 23, 0, 1, 2, 3, 4]

    :param time_range: The time range
    :return: A list of times in the given time range
    """
    if time_range == "All day":
        return [x for x in range(0, 24)]

    split = strip_time(re.split("[-&]", time_range))

    start = split[0]
    end = split[1]

    if start > end:
        end += 24

    return [x % 24 for x in range(start, end + 1)]


def strip_time(split):
    for i in range(0, len(split)):
        item = split[i].strip()
        if "PM".lower() in item.lower():
            new = re.sub("[PM]|[pm]", "", item)
            split[i] = int(new) + 12

        else:
            new = re.sub("[AM]|[am]", "", item)
            split[i] = int(new)
    return split


def to_southern_months(items):
    """
    Takes a list of months and moves each one forward by 6 months. This is because Animal Crossing has both Northern
    and Southern hemispheres, where different bugs / fish spawn 6 months apart from each other.

    :param items: The list of months to move
    :return: A list, where each each month has been shifted by 6 months
    """
    return [((x + 5) % 12) + 1 for x in items]


def dump(dictionary, file_name):
    """
    Takes a dictionary, and then saves the file as a JSON file.
    
    :param dictionary: The dictionary to save
    :param file_name: The filename
    """
    with open('data/' + file_name, 'w') as json_file:
        json.dump(dictionary, json_file, indent=4)


def multiple_replace(dictionary, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dictionary.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dictionary[mo.string[mo.start():mo.end()]], text)


def parse_museum(url, is_bug):
    """
    Generic parser for anything to do with the museum (minus art).
    Turns out that anything to do with bugs, fish or fossils are almost identical. It therefore made sense to put these
    into a utility method.

    NOTE: This uses both pandas and Requests / BeautifulSoup. There's no reason to do this from an efficiency purpose,
    however seeing as I'm treating this as a learning exercise I wanted to try to use pandas as well :)

    :param url: The URL in question to perform the scrape on
    :param is_bug: Whether the website in question is the bugs website - this is because bugs seems to have an extra
    table somewhere on the website, and therefore requires to look at one table after in the ResultSet
    :return: A tuple containing the data stored in rows separated by ",", as well as a list of corresponding URLs to
    the icons for each entry. This is because, from what I can tell, there's no easy way to retrieve image URL links
    with panads.
    """

    # Get URLs from Requests and Beautiful Soup
    response = requests.get(url)
    rep_text = response.text
    response.close()

    soup = BeautifulSoup(rep_text, 'html.parser')
    table = soup.find_all('table', {"class": "sortable"})  # Find sortable tables

    urls = []
    for item in table[0].find_all("tr")[1:]:  # Get the urls from each one
        urls.append(item.find_all('a', href=True)[1]['href'])

    # Get everything else from Pandas
    html = pd.read_html(url)

    if is_bug:  # Bug has an extra table somewhere
        table = html[5]
    else:
        table = html[4]

    csv = [x for x in re.split("[\n]", table.to_csv())][1:]

    return csv, urls
