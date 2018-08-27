# -*- coding: utf-8 -*-
import httplib
import json
import re
import socket
import sys
import os
import csv
import traceback
import urllib2
import operator

from bs4 import BeautifulSoup
from marshmallow import ValidationError
from urlparse import urlparse
from filters import Filter, FilterChain, ListContainedinListFilter, CaseInsensitiveStringFilter
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


def check_for_valid_arguents(filename):

    return validate_csv_file(filename)


def get_name(soup):
    name = soup.find('h1', attrs={'class': 'product-header__title product-header__title--app-header'})

    for child in name.find_all("span"):
        child.decompose()

    return name.get_text().strip()


def get_app_identifier(url):
    parsed_url = urlparse(url)
    return int(parsed_url.path.split('/')[-1][2:])


def get_minimum_ios_version(soup):
    '''
    Finding information section, which is the fourth element in the list
    :param soup:
    :return:
    '''
    bordered_section = soup.find_all('section', attrs={'class': 'l-content-width section section--bordered'})

    for element in bordered_section:
        if element.get_text().strip().startswith(u'Information'):
            return u'{}'.format(re.findall('Requires iOS(.*)or later.', element.get_text())[0].strip())


def get_languages(soup):
    '''
    Finding information section, which is the fourth element in the list
    :param soup:
    :return:
    '''

    bordered_section = soup.find_all('section', attrs={'class': 'l-content-width section section--bordered'})

    for element in bordered_section:
        if element.get_text().strip().startswith(u'Information'):
            languages = re.findall('Languages(\n\s*)(.*)(\n\s*)Age', element.get_text())
            languages_as_string = ' '.join(languages[0]).strip()
            return [u'{}'.format(language.strip()) for language in languages_as_string.split(',')]


def open_page(url):
    try:
        page = urllib2.urlopen(url)
        return page
    except urllib2.HTTPError, e:
        sys.stderr.write('url:{} HTTP Error: {}'.format(url, e.reason))
        sys.exit(1)
    except urllib2.URLError, e:
        sys.stderr.write('url:{} URL Error: {}'.format(url, e.reason))
        sys.exit(1)
    except httplib.HTTPException, e:
        sys.stderr.write('url:{} HTTP Exception: {}'.format(url, e.reason))
        sys.exit(1)
    except socket.timeout, e:
        sys.stderr.write('url:{} Socket Timed out'.format(url))
        sys.exit(1)
    except Exception:
        sys.stderr.write('url:{} Blanket Exception'.format(url))
        err = traceback.format_exc()
        sys.stderr.write(err)
        sys.exit(1)


def gather_data(data):

    rv = list()

    for _data in data:
        url = _data.get('app_store_url')
        name = u'{}'.format(_data.get('app_name'))

        page = open_page(url)

        soup = BeautifulSoup(page, 'lxml')

        app_identifier = get_app_identifier(url)

        minimum_ios_version = get_minimum_ios_version(soup)

        languages = get_languages(soup)

        _rv = {
            'name': name,
            'app_identifier': app_identifier,
            'minimum_version': minimum_ios_version,
            'languages': languages
        }

        rv.append(_rv)

    return rv


def write_json_to_file(data, filename):
    with open(filename, 'w+') as f:
        data_as_string = unicode(json.dumps(data)).encode('utf-8')
        f.write(data_as_string)


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

    spanish_and_tagalog_filter = ListContainedinListFilter(
        field='languages',
        op=operator.contains,
        value=[u'Spanish', u'Tagalog']
    )

    filter_chain = FilterChain()

    filter_chain.add_filter(spanish_and_tagalog_filter)

    spanish_and_tagalog_data = filter_chain.filter(gathered_data)

    insta_in_name_filter = CaseInsensitiveStringFilter(
        field='name',
        op=operator.contains,
        value='insta'
    )

    filter_chain = FilterChain()

    filter_chain.add_filter(insta_in_name_filter)

    insta_in_name_data = filter_chain.filter(gathered_data)

    filtered_data = {
        'apps_in_spanish_and_tagalog': [_d.get('app_identifier') for _d in spanish_and_tagalog_data],
        'apps_with_insta_in_name': [_d.get('app_identifier') for _d in insta_in_name_data]
    }
    write_json_to_file(filtered_data, 'filtered_apps.json')
    write_json_to_file(gathered_data, 'apps.json')


if __name__ == '__main__':
    arguments = sys.argv

    if not arguments or len(arguments) < 2:
        sys.stderr.write(help_text)
        sys.exit(1)

    data = check_for_valid_arguents(arguments[1])
    scrape(data)
