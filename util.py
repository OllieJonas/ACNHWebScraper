import json
import re


def is_tick(char):
    return char == "✓"


def dates_from_ticks(items):
    months = []

    for i in range(0, len(items)):
        if is_tick(items[i]):
            months.append(i + 1)

    return months


def strip_bells(text):
    return int(re.sub("[,\"]|[Bells]", "", text))


def pretty_print(text):
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
    return [((x + 5) % 12) + 1 for x in items]


def dump(items, file_name):
    with open('data/' + file_name, 'w') as json_file:
        json.dump(items, json_file, indent=4)


def multiple_replace(dictionary, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dictionary.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dictionary[mo.string[mo.start():mo.end()]], text)
