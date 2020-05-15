from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


def parse_museum(url, is_bug):
    # Get URLs from Requests and Beautiful Soup
    response = requests.get(url)
    rep_text = response.text
    response.close()

    soup = BeautifulSoup(rep_text, 'html.parser')
    table = soup.find_all('table', {"class": "sortable"})

    urls = []
    for item in table[0].find_all("tr")[1:]:
        urls.append(item.find_all('a', href=True)[1]['href'])

    # Get everything else from Pandas
    html = pd.read_html(url)

    if is_bug:
        table = html[5]
    else:
        table = html[4]

    csv = [x for x in re.split("[\n]", table.to_csv())][1:]
    return csv, urls
