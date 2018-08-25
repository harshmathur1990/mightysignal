# -*- coding: utf-8 -*-


import unittest
from datetime import date

import operator

from filters import FilterChain, DateFilter, Filter
from scraper import check_for_valid_arguents


class TestScrapper(unittest.TestCase):

    def test_check_for_valid_arguments(self):
        filename = 'input.csv'

        output = [
            {
                'app_name': u'Uber',
                'app_store_url': u'https://itunes.apple.com/us/app/id368677368'
            },
            {
                'app_name': u'Fortnite',
                'app_store_url': u'https://itunes.apple.com/us/app/id1261357853'
            },
            {
                'app_name': u'Tinder',
                'app_store_url': u'https://itunes.apple.com/us/app/id547702041'
            },
            {
                'app_name': u'Instagram',
                'app_store_url': u'https://itunes.apple.com/us/app/id389801252'
            }
        ]

        out = check_for_valid_arguents(filename)

        assert self._compare_list(out, output)

    def _compare_list(self, list1, list2):

        if len(list1) != len(list2):
            return False

        for l1, l2 in zip(list1, list2):
            if type(l1) != type(l2):
                return False
            if isinstance(l1, list):
                if not self._compare_list(l1, l2):
                    return False

            elif isinstance(l1, dict):
                if not self._compare_dict(l1, l2):
                    return False
            elif l1 != l2:
                    return False

        return True

    def _compare_dict(self, d1, d2):
        if len(d1.keys()) != len(d2.keys()):
            return False

        for k, v in d1.iteritems():
            if type(v) != type(d2.get(k)):
                return False
            if isinstance(v, list):
                if not self._compare_list(v, d2.get(k)):
                    return False
            elif isinstance(v, dict):
                if not self._compare_dict(v, d2.get(k)):
                    return False
            elif v != d2.get(k):
                    return False
        return True

    def test_normal_filter(self):
        data = [
            {
                "app_name": u'Test1',
                "app_identifier": 123456,
                "minimum_version": u'9.0',
                "languages": [u'English'],
                "country": 'us'
            },
        ]

        expected_data = [

        ]

        filter_chain = FilterChain()
        date_filter = DateFilter('finish_date', operator.le, date(year=2018, month=6, day=1))
        category_filter = Filter('category', operator.eq, 'Marine')
        filter_chain.add_filter(date_filter).add_filter(category_filter)

        filtered_data = filter_chain.filter(data)

        assert self._compare_list(filtered_data, expected_data)


if __name__ == '__main__':
    unittest.main()