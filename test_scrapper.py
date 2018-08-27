# -*- coding: utf-8 -*-
import socket
import unittest
import urllib2
from datetime import date

import operator

from mock import mock

from filters import FilterChain, DateFilter, Filter
from scraper import check_for_valid_arguents, open_page


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
            },
            {
                'app_name': u'PhonePe - India\'s Payments App',
                'app_store_url': u'https://itunes.apple.com/in/app/id1170055821'
            },
            {
                'app_name': u'BHIM – Making India Cashless',
                'app_store_url': u'https://itunes.apple.com/in/app/id1200315258'
            },
        ]

        expected_data = [
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

        filter_chain = FilterChain()
        us_apps_filter = Filter(
            field='app_store_url',
            op=operator.contains,
            value='/us/'
        )

        filter_chain.add_filter(us_apps_filter)

        filtered_data = filter_chain.filter(data)

        assert self._compare_list(filtered_data, expected_data)

    @mock.patch('urllib2.urlopen')
    def test_url_open_timeout(self, m_urlopen):
        m_urlopen.side_effect = socket.timeout()

        url = 'https://itunes.apple.com/us/app/id389801252'

        with self.assertRaises(SystemExit) as cm:
            page = open_page(url)

        self.assertEqual(cm.exception.code, 1)

        
if __name__ == '__main__':
    unittest.main()