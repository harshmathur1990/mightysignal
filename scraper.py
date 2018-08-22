# -*- coding: utf-8 -*-


import json
import sys
import os
import csv
import traceback
import urllib2
import operator

from bs4 import BeautifulSoup
from marshmallow import ValidationError
from urlparse import urlparse
from filters import Filter, FilterChain
from mighty_schema import ScrapeRequestSchema


help_text = '''
    Usage: python scraper.py input_csv_path
    The argument input_csv_path is a string path to a local CSV file with this format.
    It’s a CSV containing a list of apps to scrape.

    The csv file must be in this format:

    App Name,App Store URL
    Uber,https://itunes.apple.com/us/app/id368677368
    Fortnite,https://itunes.apple.com/us/app/id1261357853
    Tinder,https://itunes.apple.com/us/app/id547702041
    Instagram,https://itunes.apple.com/us/app/id389801252

    '''


def get_snake_case(key):
    lower_case_string = key.lower()
    return lower_case_string.replace(' ', '_')


def validate_csv_file(csv_file_path):
    if not os.path.exists(csv_file_path):
        sys.stderr.write(u'No Such file or directory')
        sys.exit(1)

    try:
        f = open(csv_file_path)

        reader = csv.DictReader(f)

        reader.fieldnames = [get_snake_case(name) for name in reader.fieldnames]

        schema_request = ScrapeRequestSchema(many=True).load(reader)
        return schema_request.data
    except ValidationError as err:
        sys.stderr.write(json.dumps(err.messages))
        sys.exit(1)
    except Exception:
        err_msg = traceback.format_exc()
        sys.stderr.write(err_msg)
        sys.exit(1)


def check_for_valid_arguents(arguments):

    if not arguments:
        sys.stderr.write(help_text)
        sys.exit(1)

    validate_csv_file(arguments[0])


def get_name(soup):
    name = soup.find('h1', attrs={'class': 'product-header__title product-header__title--app-header'})

    for child in name.find_all("span"):
        child.decompose()

    return name.get_text().strip()


def get_app_identifier(url):
    parsed_url = urlparse(url)
    return int(parsed_url.path.split('/')[-1][2:])


def get_minimum_ios_version(soup):

    pass


def gather_data(data):

    rv = list()

    for _data in data:
        url = _data.get('app_store_url')
        page = urllib2.urlopen(url)

        soup = BeautifulSoup(page, 'lxml')

        name = get_name(soup)

        app_identifier = get_app_identifier(url)

        minimum_ios_version = get_minimum_ios_version(soup)

        languages = get_languages(soup)

        _rv = {
            'name': name,
            'app_identifier': app_identifier,
            'minimum_ios_version': minimum_ios_version,
            'languages': languages
        }

        rv.append(_rv)

    return rv

def scrape(data):
    us_apps_filter = Filter(
        field='app_store_url',
        op=operator.contains,
        value='/us/'
    )
    filter_chain = FilterChain()
    filter_chain.add_filter(us_apps_filter)

    us_apps = filter_chain.filter(data)

    gathered_data = gather_data(us_apps)


if __name__ == '__main__':
    arguments = sys.argv
    check_for_valid_arguents(arguments)
    csv_file_name = arguments[0]
    scrape(csv_file_name)