# -*- coding: utf-8 -*-
import socket
import unittest
import urllib2
from datetime import date

import operator

from mock import mock

from filters import FilterChain, DateFilter, Filter
from scraper import check_for_valid_arguents, open_page, gather_data


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

        self.assertEqual(self._compare_list(out, output), True)

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

        self.assertEqual(self._compare_list(filtered_data, expected_data), True)

    @mock.patch('urllib2.urlopen')
    def test_url_open_timeout(self, m_urlopen):
        m_urlopen.side_effect = socket.timeout()

        url = 'https://itunes.apple.com/us/app/id389801252'

        with self.assertRaises(SystemExit) as cm:
            page = open_page(url)

        self.assertEqual(cm.exception.code, 1)

    @mock.patch('urllib2.urlopen')
    def test_scrapping(self, m_urlopen):
        m_urlopen().read.side_effect = ['''
<!DOCTYPE html>
<html lang="en-us" prefix="og: http://ogp.me/ns#"  lang="en-us" xml:lang="en-us">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    
<meta name="web-experience-app/config/environment" content="%7B%22appVersion%22%3A1%2C%22modulePrefix%22%3A%22web-experience-app%22%2C%22environment%22%3A%22production%22%2C%22rootURL%22%3A%22%2F%22%2C%22locationType%22%3A%22history-hash-router-scroll%22%2C%22historySupportMiddleware%22%3Atrue%2C%22contentSecurityPolicyMeta%22%3Atrue%2C%22contentSecurityPolicy%22%3A%7B%22default-src%22%3A%5B%22'none'%22%5D%2C%22img-src%22%3A%5B%22'self'%22%2C%22http%3A%2F%2F*.mzstatic.com%22%2C%22*.mzstatic.com%22%2C%22*.apple.com%22%2C%22data%3A%22%5D%2C%22style-src%22%3A%5B%22'self'%22%2C%22'unsafe-inline'%22%2C%22*.apple.com%22%5D%2C%22font-src%22%3A%5B%22'self'%22%2C%22http%3A%2F%2F*.apple.com%22%2C%22https%3A%2F%2F*.apple.com%22%5D%2C%22media-src%22%3A%5B%22'self'%22%2C%22blob%3A%22%2C%22http%3A%2F%2F*.apple.com%22%2C%22*.apple.com%22%2C%22http%3A%2F%2F*.akamaihd.net%22%2C%22*.akamaihd.net%22%5D%2C%22connect-src%22%3A%5B%22'self'%22%2C%22*.apple.com%22%2C%22https%3A%2F%2F*.mzstatic.com%22%2C%22*.mzstatic.com%22%5D%2C%22script-src%22%3A%5B%22'self'%22%2C%22'unsafe-inline'%22%2C%22'unsafe-eval'%22%2C%22*.apple.com%22%5D%2C%22frame-src%22%3A%5B%22'self'%22%2C%22*.apple.com%22%2C%22itmss%3A%22%2C%22itms-appss%3A%22%2C%22itms-bookss%3A%22%2C%22itms-itunesus%3A%22%2C%22itms-messagess%3A%22%2C%22itms-podcasts%3A%22%2C%22itms-watchs%3A%22%2C%22macappstores%3A%22%2C%22musics%3A%22%2C%22apple-musics%3A%22%5D%7D%2C%22EmberENV%22%3A%7B%22FEATURES%22%3A%7B%7D%2C%22EXTEND_PROTOTYPES%22%3A%7B%22Date%22%3Afalse%7D%7D%2C%22APP%22%3A%7B%22PROGRESS_BAR_DELAY%22%3A3000%2C%22name%22%3A%22web-experience-app%22%2C%22version%22%3A%221834.7.0%2B4e3cea85%22%7D%2C%22MEDIA_API%22%3A%7B%22teamId%22%3A%22AMPWebPlay%22%2C%22keyId%22%3A%22WebPlayKid%22%2C%22privateKeyPath%22%3A%22ssl%2Fwebplayer.p8%22%2C%22token%22%3A%22eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNTM0ODY3NzA4LCJleHAiOjE1NTA0MTk3MDh9.fxG4E6QczIjV2F5fVIWjBlKdTD8_qF4Hy9Yfz7slvy3YykIIjm-fjLPvpPq_d_utOl5sBhWZ54hF3ymZWxarjw%22%7D%2C%22routerScroll%22%3A%7B%22targetElement%22%3A%22%23ember-app%22%7D%2C%22i18n%22%3A%7B%22defaultLocale%22%3A%22en-gb%22%2C%22useDevLoc%22%3Afalse%2C%22pathToLocales%22%3A%22dist%2Flocales%22%7D%2C%22moment%22%3A%7B%22includeLocales%22%3Atrue%2C%22includeTimezone%22%3A%22subset%22%7D%2C%22browserify%22%3A%7B%22transform%22%3A%5B%5B%22babelify%22%2C%7B%22presets%22%3A%5B%22env%22%5D%2C%22global%22%3Atrue%2C%22only%22%3A%7B%7D%7D%5D%5D%7D%2C%22API%22%3A%7B%22MZStore%22%3A%22https%3A%2F%2Fitunes.apple.com%22%2C%22UTSHost%22%3A%22https%3A%2F%2Ftv.apple.com%2Fapi%2Futs%2Fpreview%22%2C%22StorePlatform%22%3A%22https%3A%2F%2Fuclient-api.itunes.apple.com%2FWebObjects%2FMZStorePlatform.woa%2Fwa%22%2C%22globalElementsPath%22%3A%22%2Fglobal-elements%22%2C%22videoLocalizationPath%22%3A%22%2Fglobal%2Fac_media_player%2Fscripts%2Fac_media_languages%2F%22%2C%22appleTvDomain%22%3A%22tv.apple.com%22%7D%2C%22fastboot%22%3A%7B%22hostWhitelist%22%3A%5B%7B%7D%5D%7D%2C%22ember-a11y-testing%22%3A%7B%22componentOptions%22%3A%7B%22turnAuditOff%22%3Atrue%2C%22axeOptions%22%3A%7B%22rules%22%3A%7B%22color-contrast%22%3A%7B%22enabled%22%3Afalse%7D%7D%7D%7D%7D%2C%22METRICS%22%3A%7B%22isEnabled%22%3Atrue%2C%22autoTrackingEnabled%22%3Atrue%2C%22topic%22%3A%22xp_its_preview%22%2C%22appName%22%3A%22web-experience-app%22%2C%22metricsUrl%22%3A%22https%3A%2F%2Fxp.apple.com%2Freport%22%2C%22compoundSeparator%22%3A%22_%22%7D%2C%22assetHost%22%3A%22https%3A%2F%2Fweb-experience.itunes.apple.com%22%2C%22contentSecurityPolicyHeader%22%3A%22Content-Security-Policy-Report-Only%22%2C%22exportApplicationGlobal%22%3Afalse%7D" />
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' http://*.mzstatic.com *.mzstatic.com *.apple.com data:; style-src 'self' 'unsafe-inline' *.apple.com; font-src 'self' http://*.apple.com https://*.apple.com; media-src 'self' blob: http://*.apple.com *.apple.com http://*.akamaihd.net *.akamaihd.net; connect-src 'self' *.apple.com https://*.mzstatic.com *.mzstatic.com; script-src 'self' 'unsafe-inline' 'unsafe-eval' *.apple.com; frame-src 'self' *.apple.com itmss: itms-appss: itms-bookss: itms-itunesus: itms-messagess: itms-podcasts: itms-watchs: macappstores: musics: apple-musics:; ">
<!-- EMBER_CLI_FASTBOOT_TITLE --><link rel="stylesheet" href="//www.apple.com/wss/fonts?families=SF+Pro,v1|SF+Pro+Icons,v1" name="fonts"><link rel="stylesheet" href="//www.apple.com/wss/fonts?families=SF+Pro,v1|SF+Pro+Icons,v1" name="fonts">  <meta name="ember-cli-head-start" content><title>‎Instagram on the App Store</title>
<link rel="canonical" href="https://itunes.apple.com/us/app/instagram/id389801252?mt=8">
<link rel="manifest" href="https://apps.mzstatic.com/content/static-config/android/manifest.json">
  <meta id="ember32389072" name="description" content="‎Read reviews, compare customer ratings, see screenshots, and learn more about Instagram. Download Instagram and enjoy it on your iPhone, iPad, and iPod touch." class="ember-view">

  <meta id="ember32389074" name="keywords" content="Instagram, Instagram, Inc., Photo &amp; Video, Social Networking, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes" class="ember-view">

  <meta id="ember32389076" property="og:title" content="‎Instagram on the App Store" class="ember-view">

  <meta id="ember32389078" property="og:description" content="‎Read reviews, compare customer ratings, see screenshots, and learn more about Instagram. Download Instagram and enjoy it on your iPhone, iPad, and iPod touch." class="ember-view">

  <meta id="ember32389080" property="og:site_name" content="App Store" class="ember-view">

  <meta id="ember32389082" property="og:url" content="https://itunes.apple.com/us/app/instagram/id389801252?mt=8" class="ember-view">

  <meta id="ember32389084" property="og:image" content="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/1200x630wa.jpg" class="ember-view">

  <meta id="ember32389086" property="og:image:secure_url" content="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/1200x630wa.jpg" class="ember-view">

  <meta id="ember32389088" property="og:image:type" content="image/jpg" class="ember-view">

  <meta id="ember32389090" property="og:image:width" content="1200" class="ember-view">

  <meta id="ember32389092" property="og:image:height" content="630" class="ember-view">

  <meta id="ember32389094" property="og:locale" content="en_US" class="ember-view">

  <meta id="ember32389096" property="fb:app_id" content="116556461780510" class="ember-view">

  <meta id="ember32389098" name="twitter:title" content="‎Instagram on the App Store" class="ember-view">

  <meta id="ember32389100" name="twitter:description" content="‎Read reviews, compare customer ratings, see screenshots, and learn more about Instagram. Download Instagram and enjoy it on your iPhone, iPad, and iPod touch." class="ember-view">

  <meta id="ember32389102" name="twitter:site" content="@AppStore" class="ember-view">

  <meta id="ember32389104" name="twitter:domain" content="AppStore" class="ember-view">

  <meta id="ember32389106" name="twitter:image" content="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/600x600wa.jpg" class="ember-view">

  <meta id="ember32389108" name="twitter:card" content="summary" class="ember-view">

  <meta id="ember32389110" name="apple:content_id" content="389801252" class="ember-view">

  <meta id="ember32389112" property="og:type" content="website" class="ember-view">

  <script id="ember32389114" name="schema:software-application" class="ember-view" type="application/ld+json">{"@context":"http://schema.org","@type":"SoftwareApplication","name":"Instagram","description":"Instagram is a simple way to capture and share the world’s moments. Follow your friends and family to see what they’re up to, and discover accounts from all over the world that are sharing things you love. Join the community of over 1 billion people and express yourself by sharing all the moments of your day — the highlights and everything in between, too.\n\nUse Instagram to:\n\n* Post photos and videos you want to keep on your profile grid. Edit them with filters and creative tools and combine multiple clips into one video.\n* Browse photos and videos from people you follow in your feed. Interact with posts you care about with likes and comments.\n* Share multiple photos and videos (as many as you want!) to your story. Bring them to life with text, drawing tools and other creative effects. . They disappear after 24 hours and won’t appear on your profile grid or in feed.\n* Go live to connect with your friends in the moment. Try going live with a friend and sharing a replay to your story when you’re done.\n* Message your friends privately in Direct. Send them photos and videos that disappear and share content you see on Instagram.\n* Watch stories and live videos from the people you follow in a bar at the top of your feed.\n* Discover photos, videos and stories you might like and follow new accounts on the Explore tab.","screenshot":["https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/300x0w.jpg","https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/300x0w.jpg","https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/300x0w.jpg","https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/300x0w.jpg","https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/300x0w.jpg"],"image":"https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/1200x630wa.jpg","applicationCategory":"Photo &amp; Video","datePublished":"2010-10-06","operatingSystem":"Requires iOS 9.0 or later. Compatible with iPhone, iPad, and iPod touch.","author":{"@type":"Person","name":"Instagram, Inc.","url":"https://itunes.apple.com/us/developer/instagram-inc/id389801255?mt=8"},"aggregateRating":{"@type":"AggregateRating","ratingValue":4.8,"reviewCount":6193151},"offers":{"@type":"Offer","category":"free","price":0}}
</script>

<meta name="ember-cli-head-end" content>

    <meta name="version" content="1834.7.0">

    <link integrity="" rel="stylesheet" href="https://web-experience.itunes.apple.com/assets/web-experience-app-cecc3532fe739072605c09358f921f64.css">

    
  </head>
  <body class="no-js">
    <script type="x/boundary" id="fastboot-body-start"></script><link rel="stylesheet" type="text/css" href="https://www.apple.com/ac/globalnav/3/en_US/styles/ac-globalnav.built.css">
<aside id="ac-gn-segmentbar" class="ac-gn-segmentbar" lang="en-US" dir="ltr" data-strings="{ &apos;exit&apos;: &apos;Exit&apos;, &apos;view&apos;: &apos;{%STOREFRONT%} Store Home&apos;, &apos;segments&apos;: { &apos;smb&apos;: &apos;Business Store Home&apos;, &apos;eduInd&apos;: &apos;Education Store Home&apos;, &apos;other&apos;: &apos;Store Home&apos; } }">
</aside>
<input type="checkbox" id="ac-gn-menustate" class="ac-gn-menustate">
<nav id="ac-globalnav" class="no-js" role="navigation" aria-label="Global Navigation" data-hires="false" data-analytics-region="global nav" lang="en-US" dir="ltr" data-store-locale="us" data-store-api="//www.apple.com/[storefront]/shop/bag/status" data-search-locale="en_US" data-search-api="//www.apple.com/search-services/suggestions/">
	<div class="ac-gn-content">
		<ul class="ac-gn-header">
			<li class="ac-gn-item ac-gn-menuicon">
				<label class="ac-gn-menuicon-label" for="ac-gn-menustate" aria-hidden="true">
					<span class="ac-gn-menuicon-bread ac-gn-menuicon-bread-top">
						<span class="ac-gn-menuicon-bread-crust ac-gn-menuicon-bread-crust-top"></span>
					</span>
					<span class="ac-gn-menuicon-bread ac-gn-menuicon-bread-bottom">
						<span class="ac-gn-menuicon-bread-crust ac-gn-menuicon-bread-crust-bottom"></span>
					</span>
				</label>
				<a href="#ac-gn-menustate" class="ac-gn-menuanchor ac-gn-menuanchor-open" id="ac-gn-menuanchor-open">
					<span class="ac-gn-menuanchor-label">Open Menu</span>
				</a>
				<a href="#" class="ac-gn-menuanchor ac-gn-menuanchor-close" id="ac-gn-menuanchor-close">
					<span class="ac-gn-menuanchor-label">Close Menu</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-apple">
				<a class="ac-gn-link ac-gn-link-apple" href="//www.apple.com/" data-analytics-title="apple home" id="ac-gn-firstfocus-small">
					<span class="ac-gn-link-text">Apple</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-bag ac-gn-bag-small" id="ac-gn-bag-small">
				<a class="ac-gn-link ac-gn-link-bag" href="//www.apple.com/us/shop/goto/bag" data-analytics-title="bag" data-analytics-click="bag" aria-label="Shopping Bag" data-string-badge="Shopping Bag with Items">
					<span class="ac-gn-link-text">Shopping Bag</span>
					<span class="ac-gn-bag-badge"></span>
				</a>
				<span class="ac-gn-bagview-caret ac-gn-bagview-caret-large"></span>
			</li>
		</ul>
		<ul class="ac-gn-list">
			<li class="ac-gn-item ac-gn-apple">
				<a class="ac-gn-link ac-gn-link-apple" href="//www.apple.com/" data-analytics-title="apple home" id="ac-gn-firstfocus">
					<span class="ac-gn-link-text">Apple</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-mac">
				<a class="ac-gn-link ac-gn-link-mac" href="//www.apple.com/mac/" data-analytics-title="mac">
					<span class="ac-gn-link-text">Mac</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-ipad">
				<a class="ac-gn-link ac-gn-link-ipad" href="//www.apple.com/ipad/" data-analytics-title="ipad">
					<span class="ac-gn-link-text">iPad</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-iphone">
				<a class="ac-gn-link ac-gn-link-iphone" href="//www.apple.com/iphone/" data-analytics-title="iphone">
					<span class="ac-gn-link-text">iPhone</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-watch">
				<a class="ac-gn-link ac-gn-link-watch" href="//www.apple.com/watch/" data-analytics-title="watch">
					<span class="ac-gn-link-text">Watch</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-tv">
				<a class="ac-gn-link ac-gn-link-tv" href="//www.apple.com/tv/" data-analytics-title="tv">
					<span class="ac-gn-link-text">TV</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-music">
				<a class="ac-gn-link ac-gn-link-music" href="//www.apple.com/music/" data-analytics-title="music">
					<span class="ac-gn-link-text">Music</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-support">
				<a class="ac-gn-link ac-gn-link-support" href="https://support.apple.com" data-analytics-title="support">
					<span class="ac-gn-link-text">Support</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-item-menu ac-gn-search" role="search">
				<a class="ac-gn-link ac-gn-link-search" href="//www.apple.com/us/search" data-analytics-title="search" data-analytics-click="search" aria-label="Search apple.com">
					<span class="ac-gn-search-placeholder" aria-hidden="true">Search apple.com</span>
				</a>
			</li>
			<li class="ac-gn-item ac-gn-bag" id="ac-gn-bag">
				<a class="ac-gn-link ac-gn-link-bag" href="//www.apple.com/us/shop/goto/bag" data-analytics-title="bag" data-analytics-click="bag" aria-label="Shopping Bag" data-string-badge="Shopping Bag with Items">
					<span class="ac-gn-link-text">Shopping Bag</span>
					<span class="ac-gn-bag-badge" aria-hidden="true"></span>
				</a>
				<span class="ac-gn-bagview-caret ac-gn-bagview-caret-large"></span>
			</li>
		</ul>
		<aside id="ac-gn-searchview" class="ac-gn-searchview" role="search" data-analytics-region="search">
			<div class="ac-gn-searchview-content">
				<form id="ac-gn-searchform" class="ac-gn-searchform" action="//www.apple.com/us/search" method="get">
					<div class="ac-gn-searchform-wrapper">
						<input id="ac-gn-searchform-input" class="ac-gn-searchform-input" type="text" aria-label="Search apple.com" placeholder="Search apple.com" autocorrect="off" autocapitalize="off" autocomplete="off" spellcheck="false">
						<input id="ac-gn-searchform-src" type="hidden" name="src" value="itunes_serp">
						<button id="ac-gn-searchform-submit" class="ac-gn-searchform-submit" type="submit" disabled aria-label="Submit"></button>
						<button id="ac-gn-searchform-reset" class="ac-gn-searchform-reset" type="reset" disabled aria-label="Clear Search"></button>
					</div>
				</form>
				<aside id="ac-gn-searchresults" class="ac-gn-searchresults" data-string-quicklinks="Quick Links" data-string-suggestions="Suggested Searches" data-string-noresults=""></aside>
			</div>
			<button id="ac-gn-searchview-close" class="ac-gn-searchview-close" aria-label="Close Search">
					<span class="ac-gn-searchview-close-wrapper">
						<span class="ac-gn-searchview-close-left"></span>
						<span class="ac-gn-searchview-close-right"></span>
					</span>
				</button>
		</aside>
		<aside class="ac-gn-bagview" data-analytics-region="bag">
			<div class="ac-gn-bagview-scrim">
				<span class="ac-gn-bagview-caret ac-gn-bagview-caret-small"></span>
			</div>
			<div class="ac-gn-bagview-content" id="ac-gn-bagview-content">
			</div>
		</aside>
	</div>
</nav>
<div id="ac-gn-curtain" class="ac-gn-curtain"></div>
<div id="ac-gn-placeholder" class="ac-nav-placeholder"></div>
<script type="text/javascript" src="https://www.apple.com/ac/globalnav/3/en_US/scripts/ac-globalnav.built.js" async></script>
<div class="ember-view" id="ember32389068"><!---->

<main class="is-app-theme">
  <style id="ember32389115" class="ember-view"><!----></style>
  <!---->
  <div id="ember32389118" class="focusing-outlet ember-view"><div id="ember32389119" class="ember-view"><div id="ember32389120" class="focusing-outlet ember-view"><div id="ember32389121" class="ember-view">
  <input id="localnav-menustate" class="localnav-menustate" type="checkbox">
<nav id="localnav" class="we-localnav localnav" role="navigation" data-sticky>
  <div class="localnav-wrapper">
    <div class="localnav-background we-localnav__background"></div>
    <div class="localnav-content">
      <div class="localnav-title we-localnav__title">
        <a><span class="we-localnav__title__product" data-test-we-localnav-store-title>App Store</span> <span class="we-localnav__title__qualifier" data-test-we-localnav-preview-title>Preview</span></a>
      </div>
      <div class="localnav-menu we-localnav__menu we-localnav__menu--app">
        <div class="localnav-actions we-localnav__actions">
            <div class="localnav-action localnav-action-button we-localnav__action">
            </div>
        </div>
      </div>
    </div>
  </div>
</nav>
<label id="localnav-curtain" for="localnav-menustate"></label>



<div id="ember32389124" class="animation-wrapper is-visible ember-view">  <div id="ember32389129" class="ember-view"><div class="l-content-width we-banner" role="alert">
    <p class="we-banner__copy">This app is only available on the App Store for iOS devices.</p>
  </div>
</div>

  <section class="l-content-width section section--hero product-hero">
    <div class="l-row">
      <div class="product-hero__media l-column small-5 medium-4 large-3 small-valign-top">
          <picture id="ember32389130" class="product-hero__artwork we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/230x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/460x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/690x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/217x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/434x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/651x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/246x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/492x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/738x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/246x0w.jpg" style="background-color: #ec5e43;" class="we-artwork__image ember32389130" alt>

  <style>
    .ember32389130, #ember32389130::before {
          width: 246px;
          height: 246px;
        }
        .ember32389130::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389130, #ember32389130::before {
          width: 217px;
          height: 217px;
        }
        .ember32389130::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389130, #ember32389130::before {
          width: 230px;
          height: 230px;
        }
        .ember32389130::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>
      </div>

      <div class="l-column small-7 medium-8 large-9 small-valign-top">
        <header class="product-header app-header product-header--padded-start" role="banner">
          <h1 class="product-header__title app-header__title">
            Instagram
              <span class="badge badge--product-title">12+</span>
          </h1>
<!---->          <h2 class="product-header__identity app-header__identity"><a class="link" href="https://itunes.apple.com/us/developer/instagram-inc/id389801255?mt=8">Instagram, Inc.</a></h2>
          <ul class="product-header__list app-header__list">
              <li class="product-header__list__item">
                <ul class="inline-list inline-list--mobile-compact">
                  <li class="inline-list__item">
                    #2 in Photo & Video
                  </li>
                </ul>
              </li>
              <li class="product-header__list__item app-header__list__item--user-rating">
                <ul class="inline-list inline-list--mobile-compact">
                  <li class="inline-list__item">
                    <figure id="ember32389138" aria-label="4.8 out of 5" class="we-star-rating ember-view"><span class="we-star-rating-stars-outlines">
  <span class="we-star-rating-stars we-star-rating-stars-5"></span>
</span>
  <figcaption class="we-rating-count star-rating__count">4.8, 6.2M Ratings</figcaption>
</figure>
                  </li>
                </ul>
              </li>
          </ul>
          <ul class="product-header__list app-header__list">
<!---->            <li class="product-header__list__item">
              <ul class="inline-list inline-list--mobile-compact">
                <li class="inline-list__item inline-list__item--bulleted">Free</li>
<!---->              </ul>
            </li>
<!----><!---->          </ul>
<!----><!---->        </header>
      </div>
    </div>
  </section>

<!---->
      <section class="l-content-width section section--bordered">
      <h2 class="section__headline">iPhone Screenshots</h2>
    <div id="ember32389152" class="we-screenshot-viewer ember-view"><div class="we-screenshot-viewer__screenshots">
  <ul class="l-row l-row--peek">
        <li class="l-column small-2 medium-3 large-3">
          <picture id="ember32389154" class="we-artwork--fullwidth we-artwork--screenshot-platform-iphone we-artwork--screenshot-version-iphone6+ we-artwork--screenshot-orientation-portrait we-artwork ember-view">
        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/230x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/460x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/690x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/158x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/316x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/300x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/600x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/900x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/300x0w.jpg" style="background-color: #f9f9f9;" class="we-artwork__image ember32389154" alt>

  <style>
    .ember32389154, #ember32389154::before {
          width: 300px;
          height: 533px;
        }
        .ember32389154::before {
          padding-top: 177.66666666666666%;
        }
@media (min-width: 736px) {
          .ember32389154, #ember32389154::before {
          width: 158px;
          height: 280px;
        }
        .ember32389154::before {
          padding-top: 177.2151898734177%;
        }
        }
@media (min-width: 1069px) {
          .ember32389154, #ember32389154::before {
          width: 230px;
          height: 408px;
        }
        .ember32389154::before {
          padding-top: 177.3913043478261%;
        }
        }
  </style>
</picture>
        </li>
        <li class="l-column small-2 medium-3 large-3">
          <picture id="ember32389159" class="we-artwork--fullwidth we-artwork--screenshot-platform-iphone we-artwork--screenshot-version-iphone6+ we-artwork--screenshot-orientation-portrait we-artwork ember-view">
        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/230x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/460x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/690x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/158x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/316x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/300x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/600x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/900x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/300x0w.jpg" style="background-color: #bd8a6b;" class="we-artwork__image ember32389159" alt>

  <style>
    .ember32389159, #ember32389159::before {
          width: 300px;
          height: 533px;
        }
        .ember32389159::before {
          padding-top: 177.66666666666666%;
        }
@media (min-width: 736px) {
          .ember32389159, #ember32389159::before {
          width: 158px;
          height: 280px;
        }
        .ember32389159::before {
          padding-top: 177.2151898734177%;
        }
        }
@media (min-width: 1069px) {
          .ember32389159, #ember32389159::before {
          width: 230px;
          height: 408px;
        }
        .ember32389159::before {
          padding-top: 177.3913043478261%;
        }
        }
  </style>
</picture>
        </li>
        <li class="l-column small-2 medium-3 large-3">
          <picture id="ember32389164" class="we-artwork--fullwidth we-artwork--screenshot-platform-iphone we-artwork--screenshot-version-iphone6+ we-artwork--screenshot-orientation-portrait we-artwork ember-view">
        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/230x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/460x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/690x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/158x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/316x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/300x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/600x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/900x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/300x0w.jpg" style="background-color: #f9f9f9;" class="we-artwork__image ember32389164" alt>

  <style>
    .ember32389164, #ember32389164::before {
          width: 300px;
          height: 533px;
        }
        .ember32389164::before {
          padding-top: 177.66666666666666%;
        }
@media (min-width: 736px) {
          .ember32389164, #ember32389164::before {
          width: 158px;
          height: 280px;
        }
        .ember32389164::before {
          padding-top: 177.2151898734177%;
        }
        }
@media (min-width: 1069px) {
          .ember32389164, #ember32389164::before {
          width: 230px;
          height: 408px;
        }
        .ember32389164::before {
          padding-top: 177.3913043478261%;
        }
        }
  </style>
</picture>
        </li>
        <li class="l-column small-2 medium-3 large-3">
          <picture id="ember32389169" class="we-artwork--fullwidth we-artwork--screenshot-platform-iphone we-artwork--screenshot-version-iphone6+ we-artwork--screenshot-orientation-portrait we-artwork ember-view">
        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/230x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/460x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/690x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/158x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/316x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/300x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/600x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/900x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/300x0w.jpg" style="background-color: #3b0f00;" class="we-artwork__image ember32389169" alt>

  <style>
    .ember32389169, #ember32389169::before {
          width: 300px;
          height: 533px;
        }
        .ember32389169::before {
          padding-top: 177.66666666666666%;
        }
@media (min-width: 736px) {
          .ember32389169, #ember32389169::before {
          width: 158px;
          height: 280px;
        }
        .ember32389169::before {
          padding-top: 177.2151898734177%;
        }
        }
@media (min-width: 1069px) {
          .ember32389169, #ember32389169::before {
          width: 230px;
          height: 408px;
        }
        .ember32389169::before {
          padding-top: 177.3913043478261%;
        }
        }
  </style>
</picture>
        </li>
        <li class="l-column small-2 medium-3 large-3">
          <picture id="ember32389174" class="we-artwork--fullwidth we-artwork--screenshot-platform-iphone we-artwork--screenshot-version-iphone6+ we-artwork--screenshot-orientation-portrait we-artwork ember-view">
        <source srcset="https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/230x0w.jpg 1x,https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/460x0w.jpg 2x,https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/690x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/158x0w.jpg 1x,https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/316x0w.jpg 2x,https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/300x0w.jpg 1x,https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/600x0w.jpg 2x,https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/900x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/300x0w.jpg" style="background-color: #ffffff;" class="we-artwork__image ember32389174" alt>

  <style>
    .ember32389174, #ember32389174::before {
          width: 300px;
          height: 533px;
        }
        .ember32389174::before {
          padding-top: 177.66666666666666%;
        }
@media (min-width: 736px) {
          .ember32389174, #ember32389174::before {
          width: 158px;
          height: 280px;
        }
        .ember32389174::before {
          padding-top: 177.2151898734177%;
        }
        }
@media (min-width: 1069px) {
          .ember32389174, #ember32389174::before {
          width: 230px;
          height: 408px;
        }
        .ember32389174::before {
          padding-top: 177.3913043478261%;
        }
        }
  </style>
</picture>
        </li>
  </ul>
<!----></div>
</div>
  </section>


    <section class="l-content-width section section--bordered">
      <div class="section__description">
        <h2 class="section__headline">Description</h2>
        <p id="ember32389182" aria-label="Instagram is a simple way to capture and share the world’s moments. Follow your friends and family to see what they’re up to, and discover accounts from all over the world that are sharing things you love. Join the community of over 1 billion people and express yourself by sharing all the moments of your day — the highlights and everything in between, too. Use Instagram to: * Post photos and videos you want to keep on your profile grid. Edit them with filters and creative tools and combine multiple clips into one video. * Browse photos and videos from people you follow in your feed. Interact with posts you care about with likes and comments. * Share multiple photos and videos (as many as you want!) to your story. Bring them to life with text, drawing tools and other creative effects. . They disappear after 24 hours and won’t appear on your profile grid or in feed. * Go live to connect with your friends in the moment. Try going live with a friend and sharing a replay to your story when you’re done. * Message your friends privately in Direct. Send them photos and videos that disappear and share content you see on Instagram. * Watch stories and live videos from the people you follow in a bar at the top of your feed. * Discover photos, videos and stories you might like and follow new accounts on the Explore tab." class="we-truncate we-truncate--multi-line we-truncate--interactive ember-view">  <span class="we-truncate__child">
<span id="ember32389187" class="we-clamp ember-view"><span class="we-clamp__contents">
        Instagram is a simple way to capture and share the world’s moments. Follow your friends and family to see what they’re up to, and discover accounts from all over the world that are sharing things you love. Join the community of over 1 billion people and express yourself by sharing all the moments of your day — the highlights and everything in between, too.<br /><br />Use Instagram to:<br /><br />* Post photos and videos you want to keep on your profile grid. Edit them with filters and creative tools and combine multiple clips into one video.<br />* Browse photos and videos from people you follow in your feed. Interact with posts you care about with likes and comments.<br />* Share multiple photos and videos (as many as you want!) to your story. Bring them to life with text, drawing tools and other creative effects. . They disappear after 24 hours and won’t appear on your profile grid or in feed.<br />* Go live to connect with your friends in the moment. Try going live with a friend and sharing a replay to your story when you’re done.<br />* Message your friends privately in Direct. Send them photos and videos that disappear and share content you see on Instagram.<br />* Watch stories and live videos from the people you follow in a bar at the top of your feed.<br />* Discover photos, videos and stories you might like and follow new accounts on the Explore tab.

</span>
</span>  </span>
<!----></p>
      </div>
    </section>

    <section class="l-content-width section section--bordered whats-new">
      <div class="section__nav section__nav--small">
        <h2 class="whats-new__headline">What's New</h2>
<div id="ember32389196" class="version-history ember-view">  <button class="we-modal__show link" id="modal-trigger-ember32389196">Version History</button>
<div class="we-modal we-modal--page-overlay " role="dialog" aria-hidden="true" aria-labelledby="modal-trigger-ember32389196">
  <div class="we-modal__content large-10 medium-12" id="modal-content-ember32389196" role="document" tabindex="0">
    <div class="we-modal__content__wrapper">
                  <h3 class="version-history__headline">Version History</h3>
            <ul class="version-history__items">
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">59.0</h4>
                  <time data-test-we-datetime datetime="Aug 20, 2018" aria-label="August 20, 2018" class="version-history__item__release-date" >Aug 20, 2018</time>
                  <div id="ember32389203" title="We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu. * Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. * Daily Reminder: Set a daily reminder to give yourself an alert when you've reached the amount of time you want to spend for the day. * Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389208" class="we-clamp ember-view"><span class="we-clamp__contents">
        We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu.<br /><br />* Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. <br />* Daily Reminder: Set a daily reminder to give yourself an alert when you&#39;ve reached the amount of time you want to spend for the day. <br />* Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. <br /><br />Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">58.0</h4>
                  <time data-test-we-datetime datetime="Aug 13, 2018" aria-label="August 13, 2018" class="version-history__item__release-date" >Aug 13, 2018</time>
                  <div id="ember32389210" title="We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu. * Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. * Daily Reminder: Set a daily reminder to give yourself an alert when you've reached the amount of time you want to spend for the day. * Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389215" class="we-clamp ember-view"><span class="we-clamp__contents">
        We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu.<br /><br />* Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. <br />* Daily Reminder: Set a daily reminder to give yourself an alert when you&#39;ve reached the amount of time you want to spend for the day. <br />* Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. <br /><br />Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">57.0</h4>
                  <time data-test-we-datetime datetime="Aug 6, 2018" aria-label="August 6, 2018" class="version-history__item__release-date" >Aug 6, 2018</time>
                  <div id="ember32389217" title="We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu. * Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. * Daily Reminder: Set a daily reminder to give yourself an alert when you've reached the amount of time you want to spend for the day. * Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389222" class="we-clamp ember-view"><span class="we-clamp__contents">
        We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu.<br /><br />* Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. <br />* Daily Reminder: Set a daily reminder to give yourself an alert when you&#39;ve reached the amount of time you want to spend for the day. <br />* Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. <br /><br />Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">56.0</h4>
                  <time data-test-we-datetime datetime="Jul 30, 2018" aria-label="July 30, 2018" class="version-history__item__release-date" >Jul 30, 2018</time>
                  <div id="ember32389224" title="Bug fixes and performance improvements." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389229" class="we-clamp ember-view"><span class="we-clamp__contents">
        Bug fixes and performance improvements.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">55.0</h4>
                  <time data-test-we-datetime datetime="Jul 23, 2018" aria-label="July 23, 2018" class="version-history__item__release-date" >Jul 23, 2018</time>
                  <div id="ember32389231" title="Bug fixes and performance improvements." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389236" class="we-clamp ember-view"><span class="we-clamp__contents">
        Bug fixes and performance improvements.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">54.0</h4>
                  <time data-test-we-datetime datetime="Jul 16, 2018" aria-label="July 16, 2018" class="version-history__item__release-date" >Jul 16, 2018</time>
                  <div id="ember32389238" title="Bug fixes and performance improvements." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389243" class="we-clamp ember-view"><span class="we-clamp__contents">
        Bug fixes and performance improvements.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">53.0</h4>
                  <time data-test-we-datetime datetime="Jul 9, 2018" aria-label="July 9, 2018" class="version-history__item__release-date" >Jul 9, 2018</time>
                  <div id="ember32389245" title="We're introducing three new features: * You can now video chat in Instagram Direct. Swipe into an existing thread and tap the video icon on the top right to video chat with up to four people. * At the top of Explore, you'll now see a tray of topic channels personalized to your interests. * With IGTV, you can now watch long-form, vertical video from your favorite Instagram creators. Tap the new icon at the top right of feed to get started." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389250" class="we-clamp ember-view"><span class="we-clamp__contents">
        We&#39;re introducing three new features:<br /><br />* You can now video chat in Instagram Direct. Swipe into an existing thread and tap the video icon on the top right to video chat with up to four people. <br />* At the top of Explore, you&#39;ll now see a tray of topic channels personalized to your interests. <br />* With IGTV, you can now watch long-form, vertical video from your favorite Instagram creators. Tap the new icon at the top right of feed to get started.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">52.0</h4>
                  <time data-test-we-datetime datetime="Jul 2, 2018" aria-label="July 2, 2018" class="version-history__item__release-date" >Jul 2, 2018</time>
                  <div id="ember32389252" title="Introducing IGTV, a new space for watching long-form, vertical video from your favorite Instagram creators. * It’s built for how you actually use your phone, so videos are full screen and vertical. * IGTV videos aren’t limited to one minute, which means you can see more of your favorite content. * Watch videos from creators you already follow and others you might like. * Discover new creators and follow them right from IGTV to see more." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389257" class="we-clamp ember-view"><span class="we-clamp__contents">
        Introducing IGTV, a new space for watching long-form, vertical video from your favorite Instagram creators.<br /><br />* It’s built for how you actually use your phone, so videos are full screen and vertical.<br />* IGTV videos aren’t limited to one minute, which means you can see more of your favorite content.<br />* Watch videos from creators you already follow and others you might like.<br />* Discover new creators and follow them right from IGTV to see more.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">51.0</h4>
                  <time data-test-we-datetime datetime="Jun 25, 2018" aria-label="June 25, 2018" class="version-history__item__release-date" >Jun 25, 2018</time>
                  <div id="ember32389259" title="Introducing IGTV, a new space for watching long-form, vertical video from your favorite Instagram creators. * It’s built for how you actually use your phone, so videos are full screen and vertical. * IGTV videos aren’t limited to one minute, which means you can see more of your favorite content. * Watch videos from creators you already follow and others you might like. * Discover new creators and follow them right from IGTV to see more." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389264" class="we-clamp ember-view"><span class="we-clamp__contents">
        Introducing IGTV, a new space for watching long-form, vertical video from your favorite Instagram creators.<br /><br />* It’s built for how you actually use your phone, so videos are full screen and vertical.<br />* IGTV videos aren’t limited to one minute, which means you can see more of your favorite content.<br />* Watch videos from creators you already follow and others you might like.<br />* Discover new creators and follow them right from IGTV to see more.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">50.0</h4>
                  <time data-test-we-datetime datetime="Jun 20, 2018" aria-label="June 20, 2018" class="version-history__item__release-date" >Jun 20, 2018</time>
                  <div id="ember32389266" title="Bug fixes and performance improvements." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389271" class="we-clamp ember-view"><span class="we-clamp__contents">
        Bug fixes and performance improvements.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">49.0</h4>
                  <time data-test-we-datetime datetime="Jun 11, 2018" aria-label="June 11, 2018" class="version-history__item__release-date" >Jun 11, 2018</time>
                  <div id="ember32389273" title="Bug fixes and performance improvements." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389278" class="we-clamp ember-view"><span class="we-clamp__contents">
        Bug fixes and performance improvements.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">46.0</h4>
                  <time data-test-we-datetime datetime="May 21, 2018" aria-label="May 21, 2018" class="version-history__item__release-date" >May 21, 2018</time>
                  <div id="ember32389280" title="Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389285" class="we-clamp ember-view"><span class="we-clamp__contents">
        Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">45.0</h4>
                  <time data-test-we-datetime datetime="May 16, 2018" aria-label="May 16, 2018" class="version-history__item__release-date" >May 16, 2018</time>
                  <div id="ember32389287" title="Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389292" class="we-clamp ember-view"><span class="we-clamp__contents">
        Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">44.0</h4>
                  <time data-test-we-datetime datetime="May 7, 2018" aria-label="May 7, 2018" class="version-history__item__release-date" >May 7, 2018</time>
                  <div id="ember32389294" title="Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices." class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389299" class="we-clamp ember-view"><span class="we-clamp__contents">
        Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices.

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">43.0</h4>
                  <time data-test-we-datetime datetime="Apr 30, 2018" aria-label="April 30, 2018" class="version-history__item__release-date" >Apr 30, 2018</time>
                  <div id="ember32389301" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389306" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">41.0</h4>
                  <time data-test-we-datetime datetime="Apr 21, 2018" aria-label="April 21, 2018" class="version-history__item__release-date" >Apr 21, 2018</time>
                  <div id="ember32389308" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389313" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">40.0</h4>
                  <time data-test-we-datetime datetime="Apr 9, 2018" aria-label="April 9, 2018" class="version-history__item__release-date" >Apr 9, 2018</time>
                  <div id="ember32389315" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389320" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">39.0</h4>
                  <time data-test-we-datetime datetime="Apr 2, 2018" aria-label="April 2, 2018" class="version-history__item__release-date" >Apr 2, 2018</time>
                  <div id="ember32389322" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389327" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">38.0</h4>
                  <time data-test-we-datetime datetime="Mar 26, 2018" aria-label="March 26, 2018" class="version-history__item__release-date" >Mar 26, 2018</time>
                  <div id="ember32389329" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389334" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">37.0</h4>
                  <time data-test-we-datetime datetime="Mar 19, 2018" aria-label="March 19, 2018" class="version-history__item__release-date" >Mar 19, 2018</time>
                  <div id="ember32389336" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389341" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">36.0</h4>
                  <time data-test-we-datetime datetime="Mar 12, 2018" aria-label="March 12, 2018" class="version-history__item__release-date" >Mar 12, 2018</time>
                  <div id="ember32389343" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389348" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">35.0</h4>
                  <time data-test-we-datetime datetime="Mar 5, 2018" aria-label="March 5, 2018" class="version-history__item__release-date" >Mar 5, 2018</time>
                  <div id="ember32389350" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389355" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">34.0</h4>
                  <time data-test-we-datetime datetime="Feb 26, 2018" aria-label="February 26, 2018" class="version-history__item__release-date" >Feb 26, 2018</time>
                  <div id="ember32389357" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389362" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">33.0</h4>
                  <time data-test-we-datetime datetime="Feb 20, 2018" aria-label="February 20, 2018" class="version-history__item__release-date" >Feb 20, 2018</time>
                  <div id="ember32389364" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389369" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
                <li class="version-history__item">
                  <h4 class="version-history__item__version-number">32.0</h4>
                  <time data-test-we-datetime datetime="Feb 13, 2018" aria-label="February 13, 2018" class="version-history__item__release-date" >Feb 13, 2018</time>
                  <div id="ember32389371" title="General bug fixes and performance improvements" class="version-history__item__release-notes we-truncate we-truncate--multi-line ember-view">  <span class="we-truncate__child">
<span id="ember32389376" class="we-clamp ember-view"><span class="we-clamp__contents">
        General bug fixes and performance improvements

</span>
</span>  </span>
<!----></div>
                </li>
            </ul>

    </div>

    <button class="we-modal__close" aria-label="Close"></button>
  </div>

  <button class="we-modal__close--overlay" tabindex="-1" aria-label="Close"></button>
</div>
</div>      </div>
      <div class="l-row whats-new__content">
          <div class="l-column small-12 medium-3 large-4 small-valign-top whats-new__latest">
            <div class="l-row">
              <time data-test-we-datetime datetime="Aug 20, 2018" aria-label="August 20, 2018" class="" >Aug 20, 2018</time>
              <p class="l-column small-6 medium-12 whats-new__latest__version">Version 59.0</p>
            </div>
          </div>
        <div class="l-column small-12 medium-9 large-8 small-valign-top">
          <p id="ember32389391" aria-label="We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu. * Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. * Daily Reminder: Set a daily reminder to give yourself an alert when you've reached the amount of time you want to spend for the day. * Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks." class="we-truncate we-truncate--multi-line we-truncate--interactive ember-view">  <span class="we-truncate__child">
<span id="ember32389396" class="we-clamp ember-view"><span class="we-clamp__contents">
        We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu.<br /><br />* Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day. <br />* Daily Reminder: Set a daily reminder to give yourself an alert when you&#39;ve reached the amount of time you want to spend for the day. <br />* Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications. <br /><br />Time on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks.

</span>
</span>  </span>
<!----></p>
        </div>
      </div>
    </section>

      <section class="l-content-width section section--bordered">
        <div class="section__nav">
          <h2 class="section__headline">Ratings and Reviews</h2>
        </div>
          <div id="ember32389401" class="we-customer-ratings lockup ember-view"><div class="l-row">
  <div class="we-customer-ratings__stats l-column small-4 medium-6 large-4">
    <h3 class="we-customer-ratings__averages"><span class="we-customer-ratings__averages__display">4.8</span> out of 5</h3>
      <h4 class="we-customer-ratings__count small-hide medium-show">6.2M Ratings</h4>
  </div>
  <div class=" l-column small-8 medium-6 large-4">
    <figure class="we-star-bar-graph">
        <div class="we-star-bar-graph__row">
          <span class="we-star-bar-graph__stars we-star-bar-graph__stars--5"></span>
          <div class="we-star-bar-graph__bar">
            <div class="we-star-bar-graph__bar__foreground-bar" style="width: 87%;"></div>
          </div>
        </div>
        <div class="we-star-bar-graph__row">
          <span class="we-star-bar-graph__stars we-star-bar-graph__stars--4"></span>
          <div class="we-star-bar-graph__bar">
            <div class="we-star-bar-graph__bar__foreground-bar" style="width: 9%;"></div>
          </div>
        </div>
        <div class="we-star-bar-graph__row">
          <span class="we-star-bar-graph__stars we-star-bar-graph__stars--3"></span>
          <div class="we-star-bar-graph__bar">
            <div class="we-star-bar-graph__bar__foreground-bar" style="width: 3%;"></div>
          </div>
        </div>
        <div class="we-star-bar-graph__row">
          <span class="we-star-bar-graph__stars we-star-bar-graph__stars--2"></span>
          <div class="we-star-bar-graph__bar">
            <div class="we-star-bar-graph__bar__foreground-bar" style="width: 1%;"></div>
          </div>
        </div>
        <div class="we-star-bar-graph__row">
          <span class="we-star-bar-graph__stars "></span>
          <div class="we-star-bar-graph__bar">
            <div class="we-star-bar-graph__bar__foreground-bar" style="width: 1%;"></div>
          </div>
        </div>
    </figure>
      <h5 class="we-customer-ratings__count medium-hide">6.2M Ratings</h5>
  </div>
</div></div>
        <div class="l-row l-row--peek">
            <div class="l-column small-4 medium-12 large-8 small-valign-top">
              <div id="ember32389419" class="we-editor-notes lockup ember-view"><div class="we-editor-notes__editor">
    <h3 class="we-editor-notes__editor__editor-notes">Editors’ Notes</h3>
</div>

    <p id="ember32389424" aria-label="In the great big crowd of social media apps, Instagram continues to stand out for a reason: it makes sharing moments with everyone in your world easy, speedy, and fun. Whether you’re posting breathtaking vacation photos tweaked with one of dozens of cool image filters or a video clip of an insane concert, Instagram’s uncluttered accessibility has kept it at the top of the social-sharing heap." class="we-truncate we-truncate--multi-line we-truncate--interactive ember-view">  <span class="we-truncate__child">
<span id="ember32389429" class="we-clamp ember-view"><span class="we-clamp__contents">
        In the great big crowd of social media apps, Instagram continues to stand out for a reason: it makes sharing moments with everyone in your world easy, speedy, and fun. Whether you’re posting breathtaking vacation photos tweaked with one of dozens of cool image filters or a video clip of an insane concert, Instagram’s uncluttered accessibility has kept it at the top of the social-sharing heap.

</span>
</span>  </span>
<!----></p>
</div>
            </div>
        </div>
      </section>

<!---->
<!---->
  <section class="l-content-width section section--bordered">
    <div class="l-row">
      <div class="l-column small-12">
        <h2 class="section__headline">Information</h2>
        <dl class="information-list information-list--app medium-columns">
          <div class="information-list__item l-row">
            <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Seller</dt>
            <dd class="information-list__item__definition l-column medium-9 large-6">
              Instagram, Inc.
            </dd>
          </div>
          <div class="information-list__item l-row">
            <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Size</dt>
            <dd class="information-list__item__definition l-column medium-9 large-6" aria-label="144.2 megabytes">144.2 MB</dd>
          </div>
            <div class="information-list__item l-row">
              <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Category</dt>
              <dd class="information-list__item__definition l-column medium-9 large-6">
                  <a href="https://itunes.apple.com/us/genre/id6008" class="link">Photo &amp; Video</a>
              </dd>
            </div>
          <div class="information-list__item l-row">
            <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Compatibility</dt>
            <dd id="ember32389450" aria-label="Requires iOS 9.0 or later. Compatible with iPhone, iPad, and iPod touch." class="information-list__item__definition l-column medium-9 large-6 we-truncate we-truncate--multi-line we-truncate--interactive ember-view">  <span class="we-truncate__child">
<span id="ember32389455" class="we-clamp ember-view"><span class="we-clamp__contents">
        Requires iOS 9.0 or later. Compatible with iPhone, iPad, and iPod touch.

</span>
</span>  </span>
<!----></dd>
          </div>
<!---->          <div class="information-list__item l-row">
            <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Languages</dt>
            <dd id="ember32389460" aria-label="English, Croatian, Czech, Danish, Dutch, Finnish, French, German, Greek, Indonesian, Italian, Japanese, Korean, Malay, Norwegian Bokmål, Polish, Portuguese, Romanian, Russian, Simplified Chinese, Slovak, Spanish, Swedish, Tagalog, Thai, Traditional Chinese, Turkish, Ukrainian, Vietnamese" class="information-list__item__definition l-column medium-9 large-6 we-truncate we-truncate--multi-line we-truncate--interactive ember-view">  <span class="we-truncate__child">
<span id="ember32389465" class="we-clamp ember-view"><span class="we-clamp__contents">
        English, Croatian, Czech, Danish, Dutch, Finnish, French, German, Greek, Indonesian, Italian, Japanese, Korean, Malay, Norwegian Bokmål, Polish, Portuguese, Romanian, Russian, Simplified Chinese, Slovak, Spanish, Swedish, Tagalog, Thai, Traditional Chinese, Turkish, Ukrainian, Vietnamese

</span>
</span>  </span>
<!----></dd>
          </div>
          <div class="information-list__item l-row">
            <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Age Rating</dt>
            <dd class="information-list__item__definition l-column medium-9 large-6">Rated 12+ for the following:</dd>
          </div>
              <div class="information-list__item l-row">
                <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2" aria-hidden="true"></dt>
                <dd class="information-list__item__definition l-column medium-9 large-6">Infrequent/Mild Alcohol, Tobacco, or Drug Use or References</dd>
              </div>
              <div class="information-list__item l-row">
                <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2" aria-hidden="true"></dt>
                <dd class="information-list__item__definition l-column medium-9 large-6">Infrequent/Mild Profanity or Crude Humor</dd>
              </div>
              <div class="information-list__item l-row">
                <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2" aria-hidden="true"></dt>
                <dd class="information-list__item__definition l-column medium-9 large-6">Infrequent/Mild Sexual Content and Nudity</dd>
              </div>
              <div class="information-list__item l-row">
                <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2" aria-hidden="true"></dt>
                <dd class="information-list__item__definition l-column medium-9 large-6">Infrequent/Mild Mature/Suggestive Themes</dd>
              </div>
<!---->          <div class="information-list__item l-row">
            <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Copyright</dt>
            <dd class="information-list__item__definition l-column medium-9 large-6">© 2015 Instagram, LLC.</dd>
          </div>
          <div class="information-list__item l-row">
            <dt class="information-list__item__term medium-valign-top l-column medium-3 large-2">Price</dt>
            <dd class="information-list__item__definition l-column medium-9 large-6">Free</dd>
          </div>
<!---->
        </dl>
      </div>
      <div class="l-column small-hide medium-show medium-9 medium-offset-3 large-10 large-offset-2">
        <ul class="inline-list inline-list--app-extensions">
            <li class="inline-list__item">
              <a class="link icon icon-after icon-external" href="http://instagram.com/">Developer Website</a>
            </li>
            <li class="inline-list__item inline-list__item--spaced">
              <a class="link icon icon-after icon-external" href="http://help.instagram.com/">App Support</a>
            </li>
<!---->            <li class="inline-list__item inline-list__item--spaced">
              <a class="link icon icon-after icon-external" href="http://instagram.com/legal/privacy/">Privacy Policy</a>
            </li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section l-content-width medium-hide">
    <ul class="link-list link-list--a">
        <li class="link-list__item link-list__item--a">
          <a class="link icon icon-after icon-external" href="http://instagram.com/">Developer Website</a>
        </li>
        <li class="link-list__item link-list__item--a">
          <a class="link icon icon-after icon-external" href="http://help.instagram.com/">App Support</a>
        </li>
<!---->        <li class="link-list__item link-list__item--a">
          <a class="link icon icon-after icon-external" href="http://instagram.com/legal/privacy/">Privacy Policy</a>
        </li>
    </ul>
  </section>

    <section class="l-content-width section section--bordered">
      <div class="section__nav">
        <h2 class="section__headline">Supports</h2>
      </div>
      <ul class="supports-list l-row">
          <li class="supports-list__item l-column l-column--grid small-12 medium-6 large-4">
            <img src="https://web-experience.itunes.apple.com/assets/images/supports/supports-FamilySharing@2x-f58f31bc78fe9fe7be3565abccbecb34.png" class="supports-list__item__artwork" alt>
            <div class="supports-list__item__copy">
              <h3 id="ember32389510" class="supports-list__item__copy__heading we-truncate we-truncate--single-line ember-view">  Family Sharing
</h3>
              <h4 id="ember32389515" aria-label="With Family Sharing set up, up to six family members can use this app." class="supports-list__item__copy__description we-truncate we-truncate--multi-line we-truncate--interactive ember-view">  <span class="we-truncate__child">
<span id="ember32389520" class="we-clamp ember-view"><span class="we-clamp__contents">
        With Family Sharing set up, up to six family members can use this app.

</span>
</span>  </span>
<!----></h4>
            </div>
          </li>
      </ul>
    </section>

      <section class="l-content-width section section--bordered">
        <div class="section__nav">
          <h2 class="section__headline">
            More By This Developer
          </h2>
          <a id="ember32389525" rel="nofollow" href="/us/app/true/id389801252/see-all/more-by-this-developer" style="display: none;" class="link section__nav__see-all-link ember-view">See All</a>
        </div>

        <div class="l-row l-row--peek">
    
                <a id="ember32389529" href="https://itunes.apple.com/us/app/hyperlapse-from-instagram/id740146917?mt=8" data-test-we-lockup-id="740146917" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389530" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/146x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/292x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/158x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/316x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/200x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/400x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/200x0w.jpg" style="background-color: #ffffff;" class="we-artwork__image ember32389530" alt>

  <style>
    .ember32389530, #ember32389530::before {
          width: 200px;
          height: 200px;
        }
        .ember32389530::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389530, #ember32389530::before {
          width: 158px;
          height: 158px;
        }
        .ember32389530::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389530, #ember32389530::before {
          width: 146px;
          height: 146px;
        }
        .ember32389530::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389534" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  Hyperlapse from Instagram
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389536" href="https://itunes.apple.com/us/app/layout-from-instagram/id967351793?mt=8" data-test-we-lockup-id="967351793" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389537" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/146x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/292x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/158x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/316x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/200x0w.jpg 1x,https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/400x0w.jpg 2x,https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/200x0w.jpg" style="background-color: #ffffff;" class="we-artwork__image ember32389537" alt>

  <style>
    .ember32389537, #ember32389537::before {
          width: 200px;
          height: 200px;
        }
        .ember32389537::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389537, #ember32389537::before {
          width: 158px;
          height: 158px;
        }
        .ember32389537::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389537, #ember32389537::before {
          width: 146px;
          height: 146px;
        }
        .ember32389537::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389541" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  Layout from Instagram
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389543" href="https://itunes.apple.com/us/app/boomerang-from-instagram/id1041596399?mt=8" data-test-we-lockup-id="1041596399" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389544" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/146x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/292x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/158x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/316x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/200x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/400x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/200x0w.jpg" style="background-color: #ffffff;" class="we-artwork__image ember32389544" alt>

  <style>
    .ember32389544, #ember32389544::before {
          width: 200px;
          height: 200px;
        }
        .ember32389544::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389544, #ember32389544::before {
          width: 158px;
          height: 158px;
        }
        .ember32389544::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389544, #ember32389544::before {
          width: 146px;
          height: 146px;
        }
        .ember32389544::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389548" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  Boomerang from Instagram
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389550" href="https://itunes.apple.com/us/app/igtv/id1394351700?mt=8" data-test-we-lockup-id="1394351700" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389551" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/146x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/292x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/158x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/316x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/200x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/400x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/200x0w.jpg" style="background-color: #ffbb11;" class="we-artwork__image ember32389551" alt>

  <style>
    .ember32389551, #ember32389551::before {
          width: 200px;
          height: 200px;
        }
        .ember32389551::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389551, #ember32389551::before {
          width: 158px;
          height: 158px;
        }
        .ember32389551::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389551, #ember32389551::before {
          width: 146px;
          height: 146px;
        }
        .ember32389551::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389555" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  IGTV
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


        </div>
      </section>

      <section class="l-content-width section section--bordered">
        <div class="section__nav">
          <h2 class="section__headline">
            You May Also Like
          </h2>
          <a id="ember32389560" rel="nofollow" href="/us/app/true/id389801252/see-all/customers-also-bought-apps" style="display: none;" class="link section__nav__see-all-link ember-view">See All</a>
        </div>

        <div class="l-row l-row--peek">
    
                <a id="ember32389564" href="https://itunes.apple.com/us/app/instasize-photo-editor-grid/id576649830?mt=8" data-test-we-lockup-id="576649830" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389565" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/146x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/292x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/158x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/316x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/200x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/400x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/200x0w.jpg" style="background-color: #ffffff;" class="we-artwork__image ember32389565" alt>

  <style>
    .ember32389565, #ember32389565::before {
          width: 200px;
          height: 200px;
        }
        .ember32389565::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389565, #ember32389565::before {
          width: 158px;
          height: 158px;
        }
        .ember32389565::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389565, #ember32389565::before {
          width: 146px;
          height: 146px;
        }
        .ember32389565::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389569" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  InstaSize Photo Editor &amp; Grid
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389571" href="https://itunes.apple.com/us/app/retrica/id577423493?mt=8" data-test-we-lockup-id="577423493" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389572" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/146x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/292x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/158x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/316x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/200x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/400x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/200x0w.jpg" style="background-color: #cc2800;" class="we-artwork__image ember32389572" alt>

  <style>
    .ember32389572, #ember32389572::before {
          width: 200px;
          height: 200px;
        }
        .ember32389572::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389572, #ember32389572::before {
          width: 158px;
          height: 158px;
        }
        .ember32389572::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389572, #ember32389572::before {
          width: 146px;
          height: 146px;
        }
        .ember32389572::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389576" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  Retrica
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389578" href="https://itunes.apple.com/us/app/candy-camera/id881267423?mt=8" data-test-we-lockup-id="881267423" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389579" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/146x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/292x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/158x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/316x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/200x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/400x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/200x0w.jpg" style="background-color: #506387;" class="we-artwork__image ember32389579" alt>

  <style>
    .ember32389579, #ember32389579::before {
          width: 200px;
          height: 200px;
        }
        .ember32389579::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389579, #ember32389579::before {
          width: 158px;
          height: 158px;
        }
        .ember32389579::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389579, #ember32389579::before {
          width: 146px;
          height: 146px;
        }
        .ember32389579::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389583" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  Candy Camera
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389585" href="https://itunes.apple.com/us/app/lomotif-music-video-editor/id884009993?mt=8" data-test-we-lockup-id="884009993" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389586" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/146x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/292x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/158x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/316x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/200x0w.jpg 1x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/400x0w.jpg 2x,https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/200x0w.jpg" style="background-color: #ffffff;" class="we-artwork__image ember32389586" alt>

  <style>
    .ember32389586, #ember32389586::before {
          width: 200px;
          height: 200px;
        }
        .ember32389586::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389586, #ember32389586::before {
          width: 158px;
          height: 158px;
        }
        .ember32389586::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389586, #ember32389586::before {
          width: 146px;
          height: 146px;
        }
        .ember32389586::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389590" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  Lomotif - Music Video Editor
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389592" href="https://itunes.apple.com/us/app/cymera/id553807264?mt=8" data-test-we-lockup-id="553807264" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389593" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/146x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/292x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/158x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/316x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/200x0w.jpg 1x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/400x0w.jpg 2x,https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/200x0w.jpg" style="background-color: #4ab8b2;" class="we-artwork__image ember32389593" alt>

  <style>
    .ember32389593, #ember32389593::before {
          width: 200px;
          height: 200px;
        }
        .ember32389593::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389593, #ember32389593::before {
          width: 158px;
          height: 158px;
        }
        .ember32389593::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389593, #ember32389593::before {
          width: 146px;
          height: 146px;
        }
        .ember32389593::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389597" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  Cymera
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


    
                <a id="ember32389599" href="https://itunes.apple.com/us/app/photogrid-video-pic-editor/id543577420?mt=8" data-test-we-lockup-id="543577420" data-test-we-lockup-kind="iosSoftware" class="we-lockup targeted-link l-column small-2 medium-3 large-2 ember-view">    <picture id="ember32389600" class="we-lockup__artwork we-artwork--lockup we-artwork--fullwidth we-artwork--ios-app-icon we-artwork ember-view">
        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/146x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/292x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/438x0w.jpg 3x" media="(min-width: 1069px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/158x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/316x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/474x0w.jpg 3x" media="(min-width: 736px)" class="we-artwork__source">
<!---->

        <source srcset="https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/200x0w.jpg 1x,https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/400x0w.jpg 2x,https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/600x0w.jpg 3x" class="we-artwork__source">
        <img src="https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/200x0w.jpg" style="background-color: #13c15d;" class="we-artwork__image ember32389600" alt>

  <style>
    .ember32389600, #ember32389600::before {
          width: 200px;
          height: 200px;
        }
        .ember32389600::before {
          padding-top: 100%;
        }
@media (min-width: 736px) {
          .ember32389600, #ember32389600::before {
          width: 158px;
          height: 158px;
        }
        .ember32389600::before {
          padding-top: 100%;
        }
        }
@media (min-width: 1069px) {
          .ember32389600, #ember32389600::before {
          width: 146px;
          height: 146px;
        }
        .ember32389600::before {
          padding-top: 100%;
        }
        }
  </style>
</picture>

<!---->
  <h3 class="we-lockup__title ">
      <div id="ember32389604" class="we-truncate targeted-link__target we-truncate--single-line ember-view">  PhotoGrid - Video &amp; Pic Editor
</div>
  </h3>

  <h4 class="truncate-single-line we-lockup__subtitle targeted-link__target">Photo &amp; Video</h4>
<!----></a>


        </div>
      </section>


<!----></div></div></div></div></div>
  <!---->
</main>
</div><footer id="ac-globalfooter" class="no-js" role="contentinfo" lang="en-US" dir="ltr"><div class="ac-gf-content"><link rel="stylesheet" type="text/css" href="https://www.apple.com/ac/globalfooter/3/en_US/styles/ac-globalfooter.built.css">
<section class="ac-gf-footer">
	<div class="ac-gf-footer-shop" x-ms-format-detection="none">
		More ways to shop: Visit an <a href="https://www.apple.com/retail/">Apple Store</a>, <span class="nowrap">call 1-800-MY-APPLE, or <a href="https://locate.apple.com/">find a reseller</a></span>.
	</div>
	<div class="ac-gf-footer-locale">
		<a class="ac-gf-footer-locale-link" href="//www.apple.com/choose-your-country/" title="Choose your country or region" aria-label="United States. Choose your country or region"><span class="ac-gf-footer-locale-flag" data-hires="false"></span>United States</a>
	</div>
	<div class="ac-gf-footer-legal">
		<div class="ac-gf-footer-legal-copyright">Copyright &#xA9; 2018 Apple Inc. All rights reserved.</div>
		<div class="ac-gf-footer-legal-links">
			<a class="ac-gf-footer-legal-link" href="//www.apple.com/privacy/privacy-policy/">Privacy Policy</a>
			<a class="ac-gf-footer-legal-link" href="//www.apple.com/legal/internet-services/terms/site.html">Terms of Use</a>
			<a class="ac-gf-footer-legal-link" href="//www.apple.com/us/shop/goto/help/sales_refunds">Sales and Refunds</a>
			<a class="ac-gf-footer-legal-link" href="//www.apple.com/legal/">Legal</a>
			<a class="ac-gf-footer-legal-link" href="//www.apple.com/sitemap/">Site Map</a>
		</div>
	</div>
</section>
<script type="text/javascript" src="https://www.apple.com/ac/globalfooter/3/en_US/scripts/ac-globalfooter.built.js" async></script>
</div></footer><script type="fastboot/shoebox" id="shoebox-language-tag">"en-us"</script><script type="fastboot/shoebox" id="shoebox-localizations">{"WEA.AppPages.Supports.FamilySharing.Description":"With Family Sharing set up, up to six family members can use this app.","WEA.ArtistPages.TV_Show.pageTitle":"@@tvShowName@@ on iTunes","WEA.ArtistPages.AppleMusic.Artist.PageDescription.TopListings.One":"Listen to songs and albums by @@artistName@@, including \"@@listing1@@.\"","WEA.EpisodePages.Meta.Description":"@@releaseDate@@ · @@runtimeInMinutes@@ — @@description@@","WEA.LocalNav.Store.MAS":"Mac App Store","WEA.ShowPages.Season":"Season @@seasonNumber@@","WEA.EditorialItemProductPages.Twitter.domain.iosSoftware":"AppStore","WEA.MoviePages.RottenTomatoes.Average":"Average","WEA.SportingEventPages.RelatedSportingEvents.DateFormat":"M/D [at] h:mm a","WEA.ShowPages.CastAndCrew.Director":"Director","WEA.Common.VideoSubType.short":"SHORT","WEA.MusicPages.Meta.Description.TopListings.Two.iTunes":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@,\" and \"@@listing2@@.\"","WEA.AppPages.Supports.Siri.Title":"Siri","WEA.ArtistPages.Twitter.domain.artist.iTunes":"iTunes","WEA.MusicPages.Website":"OFFICIAL WEBSITE","WEA.ArtistPages.Movie_Artist.PageKeywords":"download, @@artistName@@, movies, itunes","WEA.ArtistPages.Software_Artist.PageDescription.TopListings.One":"Download iPhone and iPad apps by @@artistName@@, including @@listing1@@.","WEA.ArtistPages.Contemporaries":"Contemporaries","WEA.LocalNav.Preview.iTunes":"Preview","WEA.MoviePages.ViewersAlsoBought":"Viewers Also Bought","WEA.ArtistPages.TopMusicVideos":"Music Videos","WEA.ArtistPages.Studio.PageDescription.TopListings.One":"Preview and download movies by @@studioName@@, including @@listing1@@.","WEA.ArtistPages.TopSongs":"Songs","WEA.EditorialItemProductPages.Social.title.GOTD":"Game of the Day: @@appName@@","WEA.AppPages.OffersAppleWatchApp":"Offers Apple Watch App","WEA.Common.Meta.Twitter.domain.AM":"Apple Music","WEA.ShowPages.CommonSenseMedia.Title":"COMMON SENSE","WEA.MusicVideoPages.AppleMusic.PageKeywords":"watch, @@songName@@, @@artistName@@, music video, songs, apple music","WEA.ShowPages.Accessibility.has4k":"UHD","WEA.MusicVideoPages.ListenersAlsoBought":"Listeners Also Bought","WEA.ArtistPages.Author.PageKeywords":"download, @@artistName@@, books, @@genreName@@, ebooks, audiobooks, ibooks","WEA.AppPages.RatingsReviews.Title":"Ratings and Reviews","WEA.AppPages.Supports.FamilySharing.Title":"Family Sharing","WEA.MoviePages.RottenTomatoes.Consensus":"Critics Consensus","WEA.AppPages.PrivacyPolicy":"Privacy Policy","WEA.MoviePages.Meta.Description.Social.TV":"@@genreName@@ · @@releaseYear@@","WEA.ArtistPages.Movie_Artist.PageDescription.TopListings.Two":"Preview and download movies by @@artistName@@, including @@listing1@@, and @@listing2@@.","WEA.MusicPages.AlsoAvailable.iTunes.AX":"View @@albumName@@ in iTunes","WEA.SportingEventPages.When.TimeFormat":"h:mm a zz","WEA.MusicPages.Meta.Title.Track.iTunes":"@@trackName@@ by @@artistName@@ on iTunes","WEA.Common.TrackList.TimeRemaining":"Time remaining","WEA.MusicPages.AppleMusic.PageDescriptionLine1.TopListings.One":"Listen to songs from the album @@albumName@@, including \"@@listing1@@\".","WEA.AppPages.Meta.tvOSAppPagetitle":"@@softwareName@@ on the App Store","WEA.MusicVideoPages.TopMusicVideosBy":"Music Videos by @@artistName@@","WEA.Common.Hours.one":"1 Hour","WEA.SportingEventPages.When.AX":"LLL zz","WEA.MusicPages.CTA.AM.App":"Apple Music","WEA.Common.Seconds.abbr.one":"1 sec","WEA.PlaylistPages.Meta.Keywords.Genre":"listen, @@playlistName@@, @@artistName@@, music, playlist, songs, @@genreName@@, streaming music, apple music","WEA.ArtistPages.TopTVSeasons":"TV Seasons","WEA.BookPages.Meta.PageMetaKeywords":"@@ebookName@@, @@authorName@@, @@categoryName@@, iBooks, iBook, books, ipad, itunes, iphone, ipod touch, itouch, synopsis, best sellers list","WEA.Common.SeeAll.Title.Item":"@@itemName@@ - @@productName@@ - @@sectionTitle@@","WEA.ArtistPages.TV_Show.PageKeywords":"download, @@tvShowName@@, @@genreName@@, tv show, itunes","WEA.Common.Languages.AudioTrack":"AudioTrack","WEA.ArtistPages.AppleMusic.Artist.PageDescription.TrackPrice":"Buy songs starting at @@cheapestTrackPrice@@.","WEA.MoviePages.MetaDescription.iTunes":"Watch trailers, read customer and critic reviews, and buy @@movieName@@ directed by @@directorName@@.","WEA.MusicVideoPages.ExpectedReleaseDate":"Expected @@expectedReleaseDate@@","WEA.MoviePages.MetaKeywords.iTunes":"@@movieName@@, @@genreName@@, @@directorName@@, movies, film, rent, buy, itunes, apple tv","WEA.AppPages.Seller":"Seller","WEA.MusicPages.PageDescriptionLine2.TrackPrice":"Songs start at @@cheapestTrackPrice@@.","WEA.Error.Generic.Subtitle.DownloadLink.Text":"download it for free","WEA.SocialProfilePages.Meta.PageDescription.zero":"No Playlists","WEA.SportingEventPages.Meta.Keywords.TV":"watch, @@sportingEventTitle@@, apple tv","WEA.ArtistPages.Author.PageDescription.TopListings.One":"Preview and download books by @@artistName@@, including @@listing1@@.","WEA.MusicVideoPages.CTA.iTunes":"View in","WEA.MusicPages.TopMusicVideosBy":"Music Videos by @@artistName@@","WEA.Error.NativeMissing.iTunes.TV.Subtitle":"Download iTunes below to start watching.","WEA.SocialProfilePages.AppleMusicLogo.Text":"Apple Music","WEA.SocialProfilePages.CTA":"Follow on","WEA.ShowPages.Information.Copyright":"Copyright","WEA.ArtistPages.iTunes_U_Artist.PageDescription.TopListings.One":"Preview and download courses and lectures from @@artistName@@, including \"@@listing1@@.\"","WEA.Error.NativeMissing.Other.AM":"Get Apple Music on iOS, Android, Mac, and Windows","WEA.MusicPages.CustomerReviews":"Ratings and Reviews","WEA.Common.Roles.Type.Voice":"Voice","WEA.AppPages.CTA.MacAppStore.AX":"View in Mac App Store","WEA.AppPages.Optional":"Optional","WEA.MusicVideoPages.Preview.All.AX":"Preview available tracks from @@albumName@@ by @@artistName@@","WEA.ShowPages.Meta.SocialMetaDescription.zero":"TV Show · @@genreName@@ · @@year@@","WEA.MusicVideoPages.SongsBy":"Songs by @@artistName@@","WEA.Common.Languages.languageDescriptor":"@@languageName@@ (@@languageMeta@@)","WEA.Common.OG.SiteName.TV":"Apple TV","WEA.ArtistPages.Podcast_Artist.PageDescription.TopListings.ManyMore":"Preview and download podcasts by @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" \"@@listing3@@,\" and many more.","WEA.Common.DateFormat":"ll","WEA.Common.LastUpdated.Thursday":"Updated Thursday","WEA.ArtistPages.TopMovies":"Movies","WEA.Common.Roles.Type.Advisor":"Advisor","WEA.EditorialItemProductPages.Meta.title":"@@storyTitle@@ : App Store Story","WEA.MusicPages.Twitter.site.preorderAlbum.AM":"@AppleMusic","WEA.MusicPages.PageDescriptionLine2.AlbumPrice":"Buy the album for @@formattedPrice@@.","WEA.SportingEventPages.When.ThisWeek":"Live @@weekday@@ at @@time@@","WEA.AppPages.Supports.Siri.Description":"Get things done within this app using just your voice.","WEA.ArtistPages.TV_Show.PageDescriptionLine":"Preview and download @@ tvShowName@@ on iTunes.","WEA.Common.Roles.Type.GuestStar":"Guest Star","WEA.ArtistPages.FB.siteName.artist.iTunes":"iTunes","WEA.Common.SeparatorDuration":"@@hours@@ @@minutes@@","WEA.Common.NowPlaying":"NOW PLAYING","WEA.MusicPages.AlbumsInGenre":"Albums in @@genreName@@","WEA.Common.Languages.Dolby71Plus":"Dolby Digital Plus 7.1","WEA.MusicPages.Preview.All.AX":"Preview available tracks from ‘@@albumName@@’ by @@artistName@@","WEA.BookPages.Twitter.domain.book":"iTunes","WEA.AppPages.Meta.MacAppStorePageTitle":"@@softwareName@@ on the Mac App Store","WEA.ArtistPages.Software_Artist.PageDescription.TopListings.ManyMore":"Download iPhone and iPad apps by @@artistName@@, including @@listing1@@, @@listing2@@, @@listing3@@, and many more.","WEA.AppPages.PreOrder":"Pre-Order","WEA.MusicPages.Upsell.Legal":"New subscribers only. Plan\u0026nbsp;automatically\u0026nbsp;renews\u0026nbsp;after\u0026nbsp;trial.","WEA.AppPages.AppleTV":"Apple TV","WEA.ArtistPages.AppleMusic.Artist.PageKeywords":"listen, @@artistName@@, music, songs, @@genreName@@, apple music","WEA.Common.DateFormat.AX":"LL","WEA.MusicPages.Meta.Title.Social.AM":"@@albumName@@ by @@artistName@@","WEA.Common.VideoSubType.specialty":"SPECIALTY","WEA.Common.Roles.Type.Actor":"Actor","WEA.AppPages.Subscriptions.PayUpFront":"@@price@@ Trial","WEA.ArtistPages.Author.PageDescription.TopListings.ManyMore":"Preview and download books by @@artistName@@, including @@listing1@@, @@listing2@@, @@listing3@@, and many more.","WEA.BookPages.Twitter.site.ibook":"@iBooks","WEA.MusicVideoPages.CTA.iTunes.Action":"View in","WEA.MoviePages.MetaKeywords.AM":"watch, @@movieName@@, music video, @@genre@@, streaming music, apple music","WEA.Common.Languages.DolbyAtmos":"Dolby Atmos","WEA.LocalNav.CTA.AppName.TV":"Apple TV App","WEA.AppPages.Information.Title":"Information","WEA.MusicVideoPages.Description":"Music video - @@year@@ - @@duration@@. Free with Apple Music subscription.","WEA.Common.Minutes.abbr.other":"@@count@@ min","WEA.LocalNav.Title.Preview.iBooks":"@@product@@ @@qualifier@@","WEA.MusicVideoPages.AppleMusic.PageDescriptionLine2.Subscription":"Free with Apple Music subscription.","WEA.ArtistPages.Twitter.site.artist":"@iTunes","WEA.MusicVideoPages.AlbumsBy":"Albums by @@artistNames@@","WEA.AppPages.MoreByThisDeveloper.Title":"More By This Developer","WEA.ArtistPages.TV_Show.PageKeywords.WithoutGenre":"download, @@tvShowName@@, tv show, itunes","WEA.ArtistPages.Podcast_Artist.PageDescription.TopListings.Three":"Preview and download podcasts by @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" and \"@@listing3@@.\"","WEA.Common.Roles.Type.Cast":"Cast","WEA.ShowPages.Twitter.domain.show":"Apple Music","WEA.LocalNav.Title.Preview":"**WEA.LocalNav.Title.Preview**","WEA.ArtistPages.Artist.PageDescription.TopListings.ManyMore":"Preview and download songs and albums by @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" \"@@listing3@@,\" and many more.","WEA.Common.Share.Social.AX":"Share the @@contentType@@ @@mediaTitle@@ by @@name@@ on @@network@@","WEA.EditorialItemProductPages.Twitter.site.iosSoftware":"@AppStore","WEA.MusicPages.AppleMusic.PageKeywords":"listen, @@albumName@@, @@artistName@@, music, singles, songs, @@genreName@@, streaming music, apple music","WEA.Error.Generic.Meta.PageDescription":"**WEA.Error.Generic.Meta.PageDescription**","WEA.ArtistPages.Movies":"Movies","WEA.AppPages.Updated":"Updated","WEA.AppPages.Meta.MacAppPageMetaDescriptionLine":"Read reviews, compare customer ratings, see screenshots, and learn more about @@softwareName@@. Download @@softwareName@@ for macOS @@minimumOSVersion@@ or later and enjoy it on your Mac.","WEA.Common.Languages.Dolby51Plus":"Dolby Digital Plus 5.1","WEA.ArtistPages.Podcast_Artist.PageKeywords.WithoutGenre":"download, @@artistName@@, podcasts, itunes","WEA.AppPages.Subscriptions.PayAsYouGo":"@@price@@ Trial","WEA.ArtistPages.Twitter.domain.artist.AM":"Apple Music","WEA.MoviePages.Twitter.site.show.AM":"@AppleMusic","WEA.Common.Meta.FB.siteName.AM":"Apple Music","WEA.Common.Meta.Twitter.domain.iTunes":"iTunes","WEA.SocialProfilePages.PlaylistCount.one":"1 Playlist","WEA.ShowPages.SeasonCount.one":"1 Season","WEA.BookPages.Meta.title":"@@ebookName@@ by @@authorName@@ on iBooks","WEA.MusicPages.CTA.iTunes.AX":"View in iTunes","WEA.AppPages.TopInAppPurchases.Title":"In-App Purchases","WEA.MusicVideoPages.AboutArtist":"About @@artistName@@","WEA.MusicPages.CTA.AM":"Listen On","WEA.ArtistPages.Author.PageKeywords.WithoutGenre":"download, @@artistName@@, books, ebooks, audiobooks, ibooks","WEA.BookPages.Twitter.site.book":"@iTunes","WEA.ArtistPages.Influencers":"Influencers","WEA.MoviePages.RottenTomatoes.Rotten":"Rotten","WEA.MusicPages.SongsBy":"Songs","WEA.AppPages.OnlyForAppleTV":"Only for Apple TV","WEA.Common.Hours.abbr.one":"1 hr","WEA.ShowPages.CastAndCrew.Guest":"Guest","WEA.AppPages.InAppPurchases.Title":"In-App Purchases","WEA.AppPages.Twitter.domain.desktopApp":"MacAppStore","WEA.AppPages.Price.Title":"Price","WEA.ArtistPages.PeopleAlsoSearchedFor":"People Also Searched For","WEA.Common.Roles.Type.Creator":"Creator","WEA.Common.FileSize.GB":"@@count@@ GB","WEA.MusicPages.Twitter.site.album.iTunes":"@iTunes","WEA.AppPages.ExpectedReleaseDate":"Expected @@expectedReleaseDate@@","WEA.Common.Seconds.one":"1 Second","WEA.Error.NotFound.general":"The page you're looking for cannot be found.","WEA.ArtistPages.FeaturedAlbum":"FEATURED ALBUM","WEA.EpisodePages.Error.NativeMissing.iTunes.Subtitle":"Download iTunes below to start watching.","WEA.EditorialItemProductPages.Meta.PageMetaDescription.Collection.One":"Learn about collection @@storyTitle@@ featuring @@featuredAppName1@@ and many more on App Store. Enjoy these apps on your iPhone, iPad, and iPod touch.","WEA.MusicPages.TotalSongs.one":"1 Song","WEA.Common.Related":"Related","WEA.EditorialItemProductPages.CTA.Text.AX":"VIEW @@appName@@","WEA.Common.VideoSubType.feature":"FEATURE","WEA.LocalNav.Preview.AppStore":"Preview","WEA.Common.DotSeparator":"@@string1@@ · @@string2@@","WEA.Error.Generic.Meta.PageKeywords.iTunes":"iTunes Store","WEA.AppPages.CTA.MacAppStore.Action":"View in","WEA.MoviePages.CommonSenseMedia.Title":"COMMON SENSE","WEA.MoviePages.RottenTomatoes.Summary.Average.Display":"@@rating@@/@@maxRating@@","WEA.MusicVideoPages.AppleMusic.title.social":"@@songName@@ by @@artistName@@","WEA.Common.LastUpdated.Friday":"Updated Friday","WEA.ArtistPages.Songs":"Songs","WEA.AppPages.Supports.Wallet.Description":"Get all of your passes, tickets, cards, and more in one place.","WEA.MusicPages.PageDescriptionLine1.TopListings.Three":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@\", \"@@listing2@@\", and \"@@listing3@@\".","WEA.MusicPages.TrackList.ByComposer":"By @@composerName@@","WEA.AppPages.CTA.AppleSchool.Action":"View in","WEA.ArtistPages.Author.PageDescription.TopListings.Three":"Preview and download books by @@artistName@@, including @@listing1@@, @@listing2@@, and @@listing3@@.","WEA.Common.Seconds.other":"@@count@@ Seconds","WEA.ArtistPages.Podcast_Artist.PageDescription.TopListings.Two":"Preview and download podcasts by @@artistName@@, including \"@@listing1@@,\" and \"@@listing2@@.\"","WEA.ShowPages.Meta.PageMetaDescription":"Watch @@showName@@ on Apple Music","WEA.ArtistPages.TopBooks":"Books","WEA.MusicPages.TopAlbumsBy":"Albums","WEA.MusicPages.Twitter.domain.album":"iTunes","WEA.Common.FileSize.byte.one":"1 byte","WEA.AppPages.Meta.tvOSAppPageMetaKeywords":"@@softwareName@@, @@developerName@@, @@categoryNames@@, tvos apps, app, appstore, app store, appletv, apple tv","WEA.MoviePages.iTunesExtras":"iTunes Extras","WEA.SportingEventPages.WatchOnBrands.other":"Watch on @@brandList@@","WEA.Common.LastUpdated.Tuesday":"Updated Tuesday","WEA.ShowPages.EpisodeNumber":"EPISODE @@episodeNumber@@","WEA.MoviePages.Trailers.Title":"Trailers","WEA.BookPages.Twitter.domain.ibookTextbook":"iBooks","WEA.Common.More":"more","WEA.MusicPages.CTA.AM.WatchOn":"Watch On","WEA.ArtistPages.Software_Artist.PageKeywords":"download, @@artistName@@, @@categoryNames@@, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes","WEA.ArtistPages.Prerelease.Coming":"COMING @@releaseDate@@","WEA.BookPages.Twitter.domain.epubBook":"iBooks","WEA.AppPages.Screenshots.appleWatch":"Apple Watch","WEA.SocialProfilePages.AppleMusicLogo.URL":"https://www.apple.com/music/","WEA.SocialProfilePages.Meta.PageDescription.Private":"Private Profile","WEA.MusicVideoPages.Preview.All":"Preview","WEA.EditorialItemProductPages.Meta.PageMetaKeywords.Collection.One":"@@storyTitle@@, @@featuredAppName1@@, @@featuredAppName2@@, @@applicationCategory@@, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes","WEA.MoviePages.Meta.PageTitle.iTunes":"@@movieName@@ on iTunes","WEA.AppPages.FB.siteName.iosSoftware":"App Store","WEA.MoviePages.SongsInThisMovie":"Songs in This Movie","WEA.AppPages.LicenseAgreement":"License Agreement","WEA.Common.Play":"Play","WEA.EditorialItemProductPages.Meta.PageMetaDescription.Collection.ManyMore":"Learn about collection @@storyTitle@@ featuring @@featuredAppName1@@, @@featuredAppName2@@, @@featuredAppName3@@, and many more on App Store. Enjoy these apps on your iPhone, iPad, and iPod touch.","WEA.BookPages.Meta.PageMetaDescription":"Read a free sample or buy @@ebookName@@ by @@authorName@@. You can read this book with iBooks on your iPhone, iPad, iPod touch, or Mac.","WEA.SportingEventPages.When.Now":"Live NOW","WEA.MusicPages.Riaa.Clean.AX":"Clean Lyrics","WEA.Common.Languages.hasSubtitles":"Subtitles","WEA.EditorialItemProductPages.InAppPurchase":"IN-APP PURCHASE","WEA.MoviePages.Meta.PageTitle.AM":"@@movieName@@ on Apple Music","WEA.MoviePages.Twitter.site.show.iTunes":"@iTunes","WEA.AppPages.OffersInAppPurchases":"Offers In-App Purchases","WEA.MoviePages.RottenTomatoes.Fresh":"Fresh","WEA.MusicVideoPages.TopAlbumsBy":"Albums by @@artistNames@@","WEA.AppPages.Screenshots.appleTV":"Apple TV","WEA.Common.TrackList.Artist":"ARTIST","WEA.ShowPages.Information.Rated.Description.WithAdvisories":"@@rating@@ @@advisories@@","WEA.EpisodePages.Meta.PageMetaDescription":"Watch “@@episodeName@@” from @@showName@@ on Apple Music","WEA.MoviePages.Meta.PageTitle":"@@movieName@@ on Apple Music","WEA.MusicVideoPages.ListenersAlsoPlayed":"Listeners Also Played","WEA.MusicPages.CTA.iTunes.Action":"View in","WEA.Common.Minutes.one":"1 Minute","WEA.EditorialItemProductPages.Meta.PageMetaKeywords.Collection.Three":"@@storyTitle@@, @@featuredAppName1@@, @@featuredAppName2@@, @@featuredAppName3@@, @@applicationCategory@@, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes","WEA.Common.Languages.hasStereo":"Stereo","WEA.Common.Roles.Type.Writer":"Writer","WEA.MusicPages.Twitter.site.album.AM":"@AppleMusic","WEA.AppPages.Twitter.domain.mobileSoftwareBundle":"AppStore","WEA.ArtistPages.CTA.iTunes.Action":"View in","WEA.Common.VideoSubType.tvinterview":"INTERVIEW","WEA.MusicPages.CTA.iTunes.App":"iTunes","WEA.Common.Meta.Twitter.site.AM":"@appleMusic","WEA.MusicPages.Meta.Description.TopListings.Three.iTunes":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@,\" \"@@listing2@@,\" and \"@@listing3@@.\"","WEA.MusicPages.Meta.Title.Track.AM":"@@trackName@@ by @@artistName@@ on Apple Music","WEA.ArtistPages.AudioBooks":"Audiobooks","WEA.ArtistPages.iTunes_U_Artist.PageKeywords":"download, @@artistName@@, courses, lectures, itunes","WEA.Common.LastUpdated.Saturday":"Updated Saturday","WEA.ShowPages.Information.Rated.Description.WithoutAdvisories":"@@rating@@","WEA.MusicPages.EditorsNotes":"EDITORS’ NOTES","WEA.Common.LastUpdated.Wednesday":"Updated Wednesday","WEA.ArtistPages.Album.Songs.one":"1 song","WEA.EpisodePages.Meta.Title":"@@showName@@: @@episodeName@@","WEA.Common.Duration":"Duration","WEA.Common.Authentication.Login":"Sign In","WEA.ArtistPages.Author.pageTitle":"@@artistName@@ on iBooks","WEA.MusicPages.PageDescriptionLine1.TopListings.Two":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@\", and \"@@listing2@@\".","WEA.EditorialItemProductPages.CTA.Link.Url":"https://www.apple.com/ios/app-store/","WEA.MusicPages.AppleMusic.PageDescriptionLine2.TrackPrice":"Songs start at @@cheapestTrackPrice@@.","WEA.ShowPages.Episodes.one":"1 Episode","WEA.ArtistPages.Artist.PageDescription.TopListings.Two":"Preview and download songs and albums by @@artistName@@, including \"@@listing1@@,\" and \"@@listing2@@.\"","WEA.ShowPages.Preview.Episode.AX":"Preview “@@episodeName@@” of @@showName@@","WEA.Common.Roles.Type.Director":"Director","WEA.AppPages.RankInGenre":"#@@rank@@ in @@genreName@@","WEA.MoviePages.CTA.iTunes.Action":"View in","WEA.ShowPages.FB.siteName.show":"Apple Music","WEA.MoviePages.InGenre":"Movies in @@genreName@@","WEA.MusicVideoPages.AlsoAvailable.iTunes":"Also Available in iTunes","WEA.Error.NotFound.Meta.Title":"This content can’t be found.","WEA.MusicPages.Twitter.site.album":"@iTunes","WEA.MusicPages.ListenersAlsoBought":"Listeners Also Bought","WEA.AppPages.Location.Description":"This app may use your location even when it isn't open, which can decrease battery life.","WEA.MusicPages.Meta.Title.Social.iTunes":"@@albumName@@ by @@artistName@@ on iTunes","WEA.Common.LastUpdated.TwoWeeksAgo":"Updated 2 Weeks Ago","WEA.PlaylistPages.Meta.Description.None.other":"Playlist · @@count@@ Songs · ","WEA.Common.VideoSubType.episodebonus":"EPISODE BONUS","WEA.Common.TimeFormat.HourOrMore":"h:mm:ss","WEA.MusicVideoPages.Preview.Resume.AX":"Continue playing current preview","WEA.SocialProfilePages.Meta.PageDescription.other":"@@count@@ Playlists","WEA.MusicPages.Twitter.domain.preorderAlbum":"iTunes","WEA.Common.Ratings.other":"@@count@@ Ratings","WEA.SocialProfilePages.CTA.App":"Apple Music","WEA.AppPages.AgeRating":"Age Rating","WEA.MusicPages.Meta.Title.iTunes":"@@albumName@@ by @@artistName@@ on iTunes","WEA.AppPages.AppStore.Header":"App Store","WEA.MusicPages.Play.Album.AX":"Play ‘@@albumName@@’ by @@artistName@@","WEA.Common.Hours.abbr.other":"@@count@@ hr","WEA.MusicVideoPages.TopSongsBy":"Songs by @@artistName@@","WEA.MusicVideoPages.AppleMusic.PageDescriptionLine2WithPrice":"Buy it for @@formattedPrice@@.","WEA.SportingEventPages.When.Tomorrow":"Live Tomorrow at @@time@@","WEA.LocalNav.CTA.FreeTrial":"Try It Now","WEA.MusicPages.Shuffle.Album.AX":"Shuffle ‘@@albumName@@’ by @@artistName@@","WEA.Common.Shuffle":"Shuffle","WEA.AppPages.DeveloperWebsite":"Developer Website","WEA.MusicPages.AppleMusic.PageDescriptionLine1.TopListings.ManyMore":"Listen to songs from the album @@albumName@@, including \"@@listing1@@\", \"@@listing2@@\", \"@@listing3@@\", and many more.","WEA.MoviePages.Twitter.site.show":"@appleMusic","WEA.Error.NativeMissing.iTunes.Download.link":"https://www.apple.com/itunes/download/","WEA.SocialProfilePages.PrivateProfile":"Private Profile","WEA.ShowPages.CTA.AM.Action":"Watch on","WEA.MoviePages.Meta.Title.TV":"@@movieName@@ on Apple TV","WEA.AppPages.Supports.GameCenter.Title":"Game Center","WEA.MusicPages.Upsell.Intro":"Listen to your favorite music ad-free on all your devices, online or off. Start streaming today with a\u0026nbsp;free trial, cancel\u0026nbsp;anytime.","WEA.Common.SeeAll.Button":"See All","WEA.AppPages.AppleWatch":"Apple Watch","WEA.MusicPages.Songs":"Songs","WEA.MusicPages.ExpectedReleaseDate":"Expected @@expectedReleaseDate@@","WEA.SportingEventPages.Meta.TimeFormat":"LT","WEA.MusicVideoPages.AlsoAvailable.iTunes.AX":"View @@albumName@@ in iTunes","WEA.ShowPages.MoreFromThisShow":"More from This Show","WEA.LocalNav.Preview.AT":"Preview","WEA.MusicPages.CTA.AM.WatchOn.AX":"Watch on Apple Music","WEA.ArtistPages.Studio.PageKeywords.WithoutGenre":"@@studioName@@, studio, itunes","WEA.Error.Generic.Install.AM":"If this link does not work, you might need to @@installLink@@.","WEA.MusicPages.CTA.AM.AX":"Listen on Apple Music","WEA.AppPages.EditorsChoice":"Editors’ Choice","WEA.ShowPages.CastAndCrew.Producers":"Producers","WEA.MusicVideoPages.PageDescriptionLine1":"Preview and buy the music video \"@@songName@@\" by @@artistName@@","WEA.MusicPages.Upsell.Headline.Line2":"Zero ads.","WEA.PlaylistPages.Meta.Description.UpdateTime":"@@updateTime@@, @@SongCount@@ Songs. Free with Apple Music Subscription.","WEA.Error.NotFound.movie":"This movie isn't available anymore.","WEA.MusicPages.Upsell.Headline.Line1":"Millions of songs.","WEA.ShowPages.TrailersBonusContent":"Trailers and Bonus Content","WEA.Error.Generic.Title.iTunes":"Connecting to the iTunes Store.","WEA.LocalNav.CTA.FreeTrial.url":"https://itunes.apple.com/subscribe?app=music","WEA.MusicPages.ArtistLink.AX":"View page for artist @@artistName@@","WEA.LocalNav.Preview.AM":"Preview","WEA.ShowPages.Meta.SocialMetaDescription.other":"TV Show · @@genreName@@ · @@year@@ · @@count@@ episodes","WEA.Common.TrackList.Album":"ALBUM","WEA.MusicPages.Twitter.domain.preorderAlbum.iTunes":"iTunes","WEA.SportingEventPages.Meta.Title.TV":"@@sportingEventTitle@@ on Apple TV","WEA.Common.Languages.AD":"AD","WEA.MusicPages.Twitter":"TWITTER","WEA.ShowPages.SeasonPicker.SeasonDisplay":"Season @@seasonNumber@@","WEA.Error.Generic.AppleMusicLogo.Text":"Apple Music","WEA.Error.NotFound.show":"This TV show isn't available anymore.","WEA.ArtistPages.CTA.AM":"View On","WEA.MusicPages.Upsell.CTA":"Try It Now","WEA.PlaylistPages.Meta.Description.Social.one":"Playlist · 1 Song","WEA.EditorialItemProductPages.CTA.Text":"This story can only be viewed in the App Store on iOS 11 with your iPhone or iPad.","WEA.LocalNav.Store.iBooks":"iBooks Store","WEA.ArtistPages.iTunes_U_Artist.PageDescription.TopListings.ManyMore":"Preview and download courses and lectures from @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" \"@@listing3@@,\" and many more.","WEA.AppPages.Supports.Title":"Supports","WEA.MusicPages.TopSongs":"Songs","WEA.AppPages.Subscriptions.FreeTrial":"Free Trial","WEA.MoviePages.Meta.Description.AM":"Movie · @@genre@@ · @@releaseYear@@ · @@runtimeInMinutes@@ — @@description@@","WEA.SocialProfilePages.CTA.AX":"Follow @@fullName@@ on Apple Music","WEA.ArtistPages.Meta.Author.Title.iTunes":"@@artistName@@ Books on iBooks","WEA.SportingEventPages.RelatedSportingEvents.DateFormat.AX":"LL","WEA.MoviePages.MoviesInBundle":"@@movieCount@@ Movies In This Bundle","WEA.MusicPages.Twitter.site.preorderAlbum.iTunes":"@iTunes","WEA.Common.Languages.hasDolby71":"Dolby 7.1","WEA.SportingEventPages.When.Today":"Live Today at @@time@@","WEA.ShowPages.Accessibility.Title":"Accessibility","WEA.MusicPages.TopSongsBy":"Songs by @@artistName@@","WEA.MusicPages.Track.Social.PageDescriptionLine1":"Preview, buy, and download the song \"@@trackName@@.\" from the album @@albumName@@","WEA.Common.Yes":"Yes","WEA.ShowPages.CastAndCrew.Performers":"Performers","WEA.Common.Languages.CC":"CC","WEA.MoviePages.ExpectedReleaseDate":"Expected @@expectedReleaseDate@@","WEA.MusicVideoPages.PageDescriptionLine2WithPrice":" for @@formattedPrice@@.","WEA.Common.FileSize.GB.AX.one":"1 gigabyte","WEA.MoviePages.Twitter.domain.show":"Apple Music","WEA.AppPages.OnlyForiMessage":"Only for iMessage","WEA.MoviePages.Meta.Description.Social.AM":"Movie · @@genre@@ · @@releaseYear@@ · @@runtimeInMinutes@@","WEA.MusicPages.FB.siteName.preorderAlbum.iTunes":"iTunes","WEA.AppBundlePages.NumberAppsInBundle.Many":"@@count@@ Apps in This Bundle","WEA.Common.Share.LinkCopied":"Link Copied","WEA.AppPages.FB.siteName.desktopApp":"Mac App Store","WEA.SocialProfilePages.Copyright":"© @@year@@ Apple Inc.","WEA.MoviePages.ArtistsInThisMovie":"Artists in This Movie","WEA.ArtistPages.CTA.AM.App":"Apple Music","WEA.Common.View":"VIEW","WEA.MusicVideoPages.Preview.Pause.AX":"Pause current preview","WEA.Common.FileSize.MB.AX.other":"@@count@@ megabytes","WEA.AppPages.Meta.PageMetaDescriptionLine":"Read reviews, compare customer ratings, see screenshots, and learn more about @@softwareName@@. Download @@softwareName@@ and enjoy it on your iPhone, iPad, and iPod touch.","WEA.MusicPages.Instagram":"INSTAGRAM","WEA.Error.Carrier.Open.Action":"Get it on @@appname@@","WEA.AppPages.CustomerReviews.Title":"Ratings and Reviews","WEA.MusicVideoPages.Preview.Song.AX":"Preview \"@@songName@@\" by @@artistName@@","WEA.MusicPages.AlsoAvailable.iTunes":"Also Available in iTunes","WEA.PlaylistPages.Meta.Title":"@@playlistName@@ by @@artistName@@ on Apple Music","WEA.MoviePages.Meta.PageKeywords":"Watch, @@movieName@@, music, singles, songs, @@genreName@@, streaming music, apple music","WEA.EditorialItemProductPages.AppOfTheDay":"APP OF THE DAY","WEA.ArtistPages.InfluencedBy":"Influenced By This Artist","WEA.ArtistPages.Software_Artist.PageDescription.TopListings.Two":"Download iPhone and iPad apps by @@artistName@@, including @@listing1@@, and @@listing2@@.","WEA.ArtistPages.TopAudioBooks":"Audiobooks","WEA.Error.NotFound.episode":"This TV episode isn't available anymore.","WEA.DeepLinkPages.Social.Subscribe.Description.AM":"Play and download all the music you want.","WEA.ArtistPages.Meta.Title.Artist.AM":"@@artistName@@ on Apple Music","WEA.Common.Twitter.Domain.TV":"Apple TV","WEA.ArtistPages.Twitter.site.artist.AM":"@AppleMusic","WEA.BookPages.Twitter.site.ibookTextbook":"@iBooks","WEA.Common.VideoSubType.episode":"EPISODE","WEA.AppPages.FamilySharing":"Family Sharing","WEA.ArtistPages.Studio.PageDescription.TopListings.Three":"Preview and download movies by @@studioName@@, including @@listing1@@, @@listing2@@, and @@listing3@@.","WEA.AppPages.Ratings.Title":"Ratings","WEA.AppPages.PreOrderDisclaimer":"This content may change without notice and the final product may be different.","WEA.Common.FileSize.KB.AX.other":"@@count@@ kilobytes","WEA.ArtistPages.AppleMusic.Artist.PageDescription.TopListings.Two":"Listen to songs and albums by @@artistName@@, including \"@@listing1@@,\" and \"@@listing2@@.\"","WEA.ArtistPages.Album.Songs.other":"@@count@@ songs","WEA.MusicPages.AboutArtist":"About @@artistName@@","WEA.EpisodePages.Meta.Title.TV":"@@episodeName@@: @@showName@@ on Apple TV","WEA.MusicPages.CTA.AM.Action":"Listen on","WEA.Common.Preview":"PREVIEW","WEA.MusicPages.Preview.Video.AX":"Preview ‘@@videoName@@’ by @@artistName@@","WEA.AppPages.Copyright":"Copyright","WEA.PlaylistPages.Meta.Keywords.NoGenre":"listen, @@playlistName@@, @@artistName@@, music, playlist, songs, streaming music, apple music","WEA.SocialProfilePages.Meta.PageKeywords":"**WEA.SocialProfilePages.Meta.PageKeywords**","WEA.Common.VideoSubType.concert":"CONCERT","WEA.MusicPages.ListenersAlsoPlayed":"Listeners Also Played","WEA.EditorialItemProductPages.Meta.PageMetaDescription.Collection.Three":"Learn about collection @@storyTitle@@ featuring @@featuredAppName1@@, @@featuredAppName2@@, and @@featuredAppName3@@ on App Store. Enjoy these apps on your iPhone, iPad, and iPod touch.","WEA.Common.Share.CloseMenu.AX":"Close sharing menu","WEA.ShowPages.CastAndCrew.Screenwriters":"Screenwriter","WEA.MoviePages.RottenTomatoes.Summary.Reviews.Rotten.Title":"Rotten","WEA.MusicVideoPages.AppleMusic.title":"@@songName@@ by @@artistName@@ on Apple Music","WEA.Common.Meta.Twitter.site.iTunes":"@iTunes","WEA.MusicVideoPages.MusicVideosBy":"Music Videos by @@artistName@@","WEA.AppPages.DeveloperResponse":"Developer Response","WEA.ShowPages.CastAndCrew.Title":"Cast \u0026 Crew","WEA.MusicPages.Twitter.domain.preorderAlbum.AM":"Apple Music","WEA.LocalNav.Preview.iBooks":"Preview","WEA.ShowPages.Information.Studio":"Studio","WEA.AppPages.Required":"Required","WEA.ShowPages.SeasonPicker.ShowMoreEpisodes.Title":"Show More Episodes","WEA.Common.Roles.Type.Producer":"Producer","WEA.Common.LearnMore":"Learn More","WEA.Common.VideoSubType.tvtrailer":"TRAILER","WEA.EditorialItemProductPages.Meta.PageMetaKeywords":"@@storyTitle@@, @@applicationCategory@@, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes","WEA.MusicPages.AppleMusic.PageDescriptionLine1.TopListings.Two":"Listen to songs from the album @@albumName@@, including \"@@listing1@@\", and \"@@listing2@@\".","WEA.MoviePages.FB.siteName.show":"Apple Music","WEA.MoviePages.Meta.PageMetaDescription":"Watch @@movieName@@ on Apple Music","WEA.MusicPages.MoreByArtist":"More By @@artistName@@","WEA.MusicVideoPages.AlsoAvailable.AM.AX":"View @@albumName@@ in Apple Music","WEA.MusicPages.TopMusicVideos":"Music Videos","WEA.ArtistPages.Artist.pageTitle":"@@artistName@@ on iTunes","WEA.AppPages.Meta.tvOSAppPageMetaDescriptionLine":"Read reviews, compare customer ratings, see screenshots, and learn more about @@softwareName@@. Download @@softwareName@@ and enjoy it on your Apple TV.","WEA.MusicVideoPages.CTA.AM":"View On","WEA.ArtistPages.AppleMusic.Artist.PageKeywords.WithoutGenre":"listen, @@artistName@@, music, songs, apple music","WEA.ArtistPages.Podcast_Artist.pageTitle":"@@artistName@@ Podcasts on iTunes","WEA.MoviePages.RottenTomatoes.Tomatometer":"TOMATOMETER","WEA.AppPages.EditorsNotes.Header":"Editors’ Notes","WEA.ArtistPages.Movie_Artist.PageDescription.TopListings.One":"Preview and download movies by @@artistName@@, including @@listing1@@.","WEA.Common.Share.OpenMenu.AX":"Open sharing menu","WEA.MusicPages.Formed":"FORMED","WEA.SocialProfilePages.CTA.AM.Action":"Follow on","WEA.SocialProfilePages.Meta.PageTitle":"@@fullName@@ on Apple Music","WEA.Error.Generic.Subtitle":"If you don’t have iTunes, @@downloadLink@@. If you have iTunes and it doesn’t open automatically, try opening it from your dock or Windows task bar.","WEA.Common.Hours.other":"@@count@@ Hours","WEA.ArtistPages.AppleMusic.Artist.pageTitle":"@@artistName@@ on Apple Music","WEA.AppPages.Screenshots.appleTVScreenshots":"Apple TV Screenshots","WEA.PlaylistPages.Meta.Description.Social.other":"Playlist · @@count@@ Songs","WEA.ShowPages.Playlists":"Playlists","WEA.MoviePages.MetaKeywords.iTunes.noDirector":"@@movieName@@, @@genreName@@, movies, film, rent, buy, itunes, apple tv","WEA.MusicVideoPages.TopMusicVideoInGenre":"Music Videos in @@genreName@@","WEA.AppPages.Meta.title":"@@softwareName@@ on the App Store","WEA.SportingEventPages.Meta.Description.Social.TV":"@@eventDate@@ · @@eventTime@@ · @@leagueName@@","WEA.MusicPages.Meta.Description.Social.AM.one":"Album · @@year@@ · 1 Song","WEA.ArtistPages.Meta.Artist.Title.AM":"@@artistName@@ on Apple Music","WEA.Common.Released":"Released: @@releaseDate@@","WEA.MusicPages.Meta.Title.Track.Social.iTunes":"\"@@trackName@@\" from @@albumName@@ by @@artistName@@ on iTunes","WEA.MoviePages.Information.Format.Standard":"Standard","WEA.AppPages.OffersiMessageAppForiOS":"Offers iMessage App for iOS","WEA.Error.Carrier.Installed":"Already have the app?","WEA.ArtistPages.Studio.pageTitle":"@@studioName@@ on iTunes","WEA.MoviePages.FB.siteName.show.AM":"Apple Music","WEA.ShowPages.Meta.Keywords.TV":"**WEA.ShowPages.Meta.Keywords.TV**","WEA.AppPages.Meta.PageMetaKeywords":"@@softwareName@@, @@developerName@@, @@categoryNames@@, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes","WEA.AppPages.Description.Header":"Description","WEA.AppPages.Supports.GameCenter.Description":"Challenge friends and check leaderboards and achievements.","WEA.MusicPages.Website.AX":"Go to official website for @@artistName@@.","WEA.Common.TimeFormat.UnderHour":"m:ss","WEA.MoviePages.TopInGenre":"Movies in @@genreName@@","WEA.MusicPages.AppleMusic.PageDescriptionLine1.TopListings.Three":"Listen to songs from the album @@albumName@@, including \"@@listing1@@\", \"@@listing2@@\", and \"@@listing3@@\".","WEA.AudiobookPages.Meta.title":"@@audiobookName@@ by @@authorName@@ on iTunes","WEA.Common.SeeAll.Title.Product":"@@artistName@@ — @@sectionTitle@@","WEA.MusicPages.TrackList.Separator":"@@string1@@ - @@string2@@","WEA.Common.Minutes.other":"@@count@@ Minutes","WEA.MusicPages.Meta.ExtraInfo":"Available with an Apple Music subscription.","WEA.Common.Authentication.Logout":"Sign Out","WEA.LocalNav.Store.AT":"Apple TV","WEA.MusicPages.Origin":"ORIGIN","WEA.ArtistPages.Author.PageDescription.TopListings.Two":"Preview and download books by @@artistName@@, including @@listing1@@, and @@listing2@@.","WEA.LocalNav.Store.AM":"Apple Music","WEA.ShowPages.SeasonCount.other":"@@count@@ Seasons","WEA.ArtistPages.iTunes_U_Artist.PageDescription.TopListings.Two":"Preview and download courses and lectures from @@artistName@@, including \"@@listing1@@,\" and \"@@listing2@@.\"","WEA.AppPages.Screenshots.appleWatchScreenshots":"Apple Watch Screenshots","WEA.Common.LastUpdated.Sunday":"Updated Sunday","WEA.MusicVideoPages.title":"\"@@songName@@\" on iTunes","WEA.AppPages.OffersiMessageApp":"Offers iMessage App","WEA.MusicPages.AlsoAvailable.AM":"Also Available on Apple Music","WEA.MusicPages.Riaa.Explicit.AX":"Parental Advisory: Explicit Lyrics.","WEA.AppPages.Availability.iOS.Bundle":"This app bundle is only available on the App Store for iOS devices.","WEA.AppPages.Twitter.site.mobileSoftwareBundle":"@AppStore","WEA.ArtistPages.TopAlbums":"Albums","WEA.MusicPages.MasteredForiTunes.AX":"Mastered for iTunes","WEA.Common.Roles.Type.Guest":"Guest","WEA.MoviePages.CTA.AM.Action":"Watch on","WEA.Common.Share.Embed.AX":"Copy the embed code for the @@contentType@@ @@mediaTitle@@ by @@name@@","WEA.ArtistPages.Artist.PageKeywords.WithoutGenre":"download, @@artistName@@, music, songs, itunes","WEA.PlaylistPages.Meta.Description.None.one":"Playlist · 1 Song · ","WEA.Common.Seconds.abbr.other":"@@count@@ sec","WEA.EpisodePages.CTA.iTunes.Action":"Watch on","WEA.Common.Meta.Description.Subscription.AM":"Available with an Apple Music subscription. Try it free.","WEA.MusicPages.Meta.Title.Track.Social.AM":"@@trackName@@ by @@artistName@@","WEA.ArtistPages.Artist.PageKeywords":"download, @@artistName@@, music, songs, @@genreName@@, itunes","WEA.ArtistPages.Twitter.site.artist.iTunes":"@iTunes","WEA.MoviePages.RelatedMovies":"Related Movies","WEA.BookPages.FB.siteName.ibook":"iBooks","WEA.MusicPages.Meta.Description.Track.Social.AM":"Song · @@duration@@ · @@year@@","WEA.ShowPages.Accessibility.hasHDR":"HDR","WEA.MoviePages.RottenTomatoes.AudienceScore ":"**WEA.MoviePages.RottenTomatoes.AudienceScore **","WEA.MoviePages.RottenTomatoes.Critic.DateFormat":"(l)","WEA.Common.SeeAll.Title.Generic":"@@parentName@@ - @@sectionTitle@@","WEA.LocalNav.CTA.DownloadAppleTv.url":"https://www.apple.com/tv-app/","WEA.AppPages.Compatibility":"Compatibility","WEA.ShowPages.Accessibility.SDH":"Subtitles for the deaf and hard of hearing refer to subtitles in the original language with the addition of relevant nondialogue information.","WEA.AppPages.Screenshots.messagesScreenshots":"iMessage Screenshots","WEA.Error.Carrier.Install.AM":"To Start listening, install Apple Music on your device","WEA.MusicVideoPages.CTA.iTunes.AX":"View in iTunes","WEA.MoviePages.Information.Format":"Format","WEA.PlaylistPages.Meta.Description.NoUpdateTime":"@@SongCount@@ Songs. Free with Apple Music Subscription.","WEA.MusicPages.Twitter.domain.album.AM":"Apple Music","WEA.MusicVideoPages.CTA.AM.AX":"View on Apple Music","WEA.Common.Share.Link.AX":"Copy a link to the @@contentType@@ @@mediaTitle@@ by @@name@@","WEA.AppPages.AdditionalScreenshots":"Additional Screenshots","WEA.MoviePages.Twitter.domain.show.iTunes":"iTunes","WEA.ShowPages.Information.Rated":"Rated","WEA.MoviePages.Trailers":"Trailers","WEA.ArtistPages.TVSeasons":"TV Seasons","WEA.AppPages.Twitter.site.iosSoftware":"@AppStore","WEA.MusicPages.Meta.Description.Social.AM.other":"Album · @@year@@ · @@count@@ Songs","WEA.AppPages.Subscriptions.Title":"Subscriptions","WEA.AppBundlePages.AppBundle":"App Bundle @@appPrice@@","WEA.AppPages.Rating":"Rating","WEA.AppPages.AppSupport":"App Support","WEA.MusicPages.FB.siteName.album.AM":"Apple Music","WEA.AppPages.TopInCategory.Title":"Top Apps In @@categoryName@@","WEA.ArtistPages.Albums":"Albums","WEA.Common.AverageRating":"@@rating@@ out of @@ratingTotal@@","WEA.ArtistPages.Movie_Artist.pageTitle":"@@artistName@@ Movies on iTunes","WEA.EpisodePages.FB.siteName.episode":"Apple Music","WEA.EpisodePages.title":"@@episodeName@@ on Apple Music","WEA.Common.TogglePlay":"Play/Pause","WEA.MusicPages.Videos":"Videos","WEA.LocalNav.Title.Preview.AppStore":"@@product@@ @@qualifier@@","WEA.ArtistPages.FB.siteName.artist":"iTunes","WEA.Common.LastUpdated.Yesterday":"Updated Yesterday","WEA.MusicPages.Meta.Title.AM":"@@albumName@@ by @@artistName@@ on Apple Music","WEA.Common.YearFormat":"YYYY","WEA.Common.TrackList.Time":"TIME","WEA.ArtistPages.Meta.Artist.Title.iTunes":"@@artistName@@ on iTunes","WEA.SocialProfilePages.CTA.Eyebrow":"Follow on","WEA.Error.Generic.Title":"Connecting to Apple Music","WEA.AppPages.Availability.tvOS":"This app is only available on the App Store for Apple TV devices.","WEA.Common.Languages.Dolby51":"Dolby Digital 5.1","WEA.AppPages.ViewIn":"View On:","WEA.MusicPages.Twitter.AX":"Go to Twitter user @@handle@@.","WEA.AppPages.Location.Title":"Location","WEA.Common.Preview.VideoName":"Preview @@videoName@@","WEA.ArtistPages.iTunes_U_Artist.PageKeywords.WithoutGenre":"download, @@artistName@@, courses, lectures, itunes","WEA.MusicPages.FB.siteName.preorderAlbum":"iTunes","WEA.MusicPages.SimilarArtists":"Similar Artists","WEA.Common.SeparatorGeneric":"@@string1@@, @@string2@@","WEA.EditorialItemProductPages.Meta.PageMetaDescription.Collection.Two":"Learn about collection @@storyTitle@@ featuring @@featuredAppName1@@, @@featuredAppName2@@, and many more on App Store. Enjoy these apps on your iPhone, iPad, and iPod touch.","WEA.LocalNav.Preview.Podcasts":"Preview","WEA.ArtistPages.Studio.PageDescription.TopListings.ManyMore":"Preview and download movies by @@studioName@@, including @@listing1@@, @@listing2@@, @@listing3@@, and many more.","WEA.AppPages.Availability.iOS":"This app is only available on the App Store for iOS devices.","WEA.ArtistPages.AppleMusic.Artist.PageDescription.Subscription":"Free with Apple Music","WEA.Error.Generic.Install.AM.Link.Text":"install Apple Music","WEA.MusicPages.Genre":"GENRE","WEA.Common.Twitter.Site.TV":"@AppleTV","WEA.AppPages.Screenshots.messages":"iMessage","WEA.MoviePages.MetaDescription.iTunes.noDirector":"Watch trailers, read customer and critic reviews, and buy @@movieName@@.","WEA.ShowPages.Episodes.other":"@@count@@ Episodes","WEA.EditorialItemProductPages.FB.siteName.iosSoftware":"App Store","WEA.AppPages.Category":"Category","WEA.MusicPages.Meta.Description.TopListings.One.iTunes":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@.\"","WEA.ShowPages.Episode.abbr":"Ep @@episodeNumber@@","WEA.MusicPages.Preview.Pause.AX":"Pause current preview","WEA.ArtistPages.Studio.PageDescription.TopListings.Two":"Preview and download movies by @@studioName@@, including @@listing1@@, and @@listing2@@.","WEA.MusicVideoPages.CTA.AM.Action":"View on","WEA.Error.Generic.GooglePlay":"Google Play","WEA.LocalNav.Store.iTunes":"iTunes","WEA.ShowPages.ArtistsOnThisShow":"Artists in This Show","WEA.ShowPages.Meta.Title.TV":"@@showName@@ on Apple TV","WEA.Error.NativeMissing.AM.Subtitle":"You need iTunes to use Apple Music","WEA.MoviePages.ReviewsAndRatings":"Ratings and Reviews","WEA.MusicPages.Meta.Description.AM.other":"Album · @@year@@ · @@count@@ Songs.","WEA.Common.Roles.AsCharacter":"as @@characterName@@","WEA.EpisodePages.CTA.iTunes.AX":"Watch on iTunes","WEA.BookPages.Twitter.site.epubBook":"@iBooks","WEA.BookPages.Availability.Windows":"This book can be downloaded and read in iBooks on your Mac or iOS device.","WEA.MusicVideoPages.Social.Description":"Music video - @@year@@ - @@duration@@","WEA.Common.FileSize.GB.AX.other":"@@count@@ gigabytes","WEA.MusicPages.PageDescriptionLine1.TopListings.ManyMore":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@\", \"@@listing2@@\", \"@@listing3@@\", and many more.","WEA.MusicVideoPages.Social.Title":"@@songName@@ by @@artistName@@","WEA.AppPages.EditReview":"To edit your review of this app, use an iPhone or iPad to view the app on the App Store.","WEA.BookPages.Twitter.domain.ibook":"iBooks","WEA.SocialProfilePages.PrivacyLink.URL":"https://support.apple.com/kb/HT204881","WEA.ShowPages.CastAndCrew.Host":"Hosts","WEA.ArtistPages.Movie_Artist.PageDescription.TopListings.Three":"Preview and download movies by @@artistName@@, including @@listing1@@, @@listing2@@, and @@listing3@@.","WEA.ArtistPages.Artist.PageDescription.TopListings.One":"Preview and download songs and albums by @@artistName@@, including \"@@listing1@@.\"","WEA.BookPages.FB.siteName.epubBook":"iBooks","WEA.MusicPages.TopVideos":"Videos","WEA.MusicVideoPages.AlsoAvailable.AM":"Also Available on Apple Music","WEA.Common.LastUpdated.Monday":"Updated Monday","WEA.MusicVideoPages.CTA.AM.App":"Apple Music","WEA.EditorialItemProductPages.Social.title.AOTD":"App of the Day: @@appName@@","WEA.Error.Generic.Meta.PageTitle":"Connecting to Apple Music.","WEA.MoviePages.MoreByDirector":"More By This Director","WEA.MusicPages.CTA.iTunes":"View in","WEA.EpisodePages.Meta.Keywords.TV":"watch, @@episodeName@@, @@showName@@, @@genreName@@, tv shows, apple tv","WEA.LocalNav.CTA.iTunesStore.TV":"Learn More","WEA.MusicPages.title":"@@albumName@@ by @@artistName@@ on iTunes","WEA.AppPages.MacAppStore.Header":"Mac App Store","WEA.ArtistPages.Meta.iTunes_U_Artist.Title.iTunes":"@@artistName@@ Courses on iTunes","WEA.Error.Generic.Open.AM":"Open in Apple Music","WEA.SocialProfilePages.PlaylistCount.zero":"No Playlists","WEA.MusicPages.Born":"BORN","WEA.ArtistPages.Podcast_Artist.PageDescription.TopListings.One":"Preview and download podcasts by @@artistName@@, including \"@@listing1@@.\"","WEA.MusicPages.Preview.All":"Preview","WEA.Common.LastUpdated.LastWeek":"Updated Last Week","WEA.Error.NativeMissing.iTunes.Download.text":"Download iTunes","WEA.MusicPages.Meta.Description.TrackPrice.Social.iTunes":"for @@trackPrice@@.","WEA.ArtistPages.Movie_Artist.PageDescription.TopListings.ManyMore":"Preview and download movies by @@artistName@@, including @@listing1@@, @@listing2@@, @@listing3@@, and many more.","WEA.AppPages.Version":"Version","WEA.LocalNav.Title.Preview.AT":"@@product@@ @@qualifier@@","WEA.MusicPages.MusicVideos":"Music Videos","WEA.EditorialItemProductPages.Meta.PageMetaKeywords.Collection.Two":"@@storyTitle@@, @@featuredAppName1@@, @@featuredAppName2@@, @@applicationCategory@@, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes","WEA.MusicPages.TopAlbumsInGenre":"Albums in @@genreName@@","WEA.LocalNav.Title.Preview.AM":"@@product@@ @@qualifier@@","WEA.MoviePages.MoreByDirectors":"More By These Directors","WEA.Common.VideoSubType.seasonbonus":"SEASON BONUS","WEA.ShowPages.Accessibility.hasSDH":"SDH","WEA.ArtistPages.Software_Artist.PageKeywords.WithoutGenre":"download, @@artistName@@, ios apps, app, appstore, app store, iphone, ipad, ipod touch, itouch, itunes","WEA.Common.Ratings.zero":"No Ratings","WEA.SportingEventPages.RelatedSportingEvents":"Other Games","WEA.MusicPages.TopAlbums":"Albums","WEA.Common.FileSize.KB":"@@count@@ KB","WEA.Error.Generic.Meta.PageKeywords":"Apple Music","WEA.MusicPages.AlbumsBy":"Albums by @@artistNames@@","WEA.ShowPages.CastAndCrew.Cast":"Cast","WEA.AppPages.InAppPurchase.Title":"In-App Purchases","WEA.MusicPages.PageKeywords":"download, @@albumName@@, @@artistName@@, music, singles, songs, @@genreName@@, itunes music.","WEA.MusicPages.TotalSongs.other":"@@count@@ Songs","WEA.ShowPages.Meta.SocialMetaDescription.one":"TV Show · @@genreName@@ · @@year@@ · 1 episode","WEA.Error.NativeMissing.Other.LearnMore.link":"https://www.apple.com/itunes/download/","WEA.SocialProfilePages.PlaylistCount.other":"@@count@@ Playlists","WEA.ArtistPages.Artist.PageDescription.TrackPrice":"Songs by @@artistName@@ start at @@cheapestTrackPrice@@.","WEA.PlaylistPages.Meta.Description.other":"Playlist · @@count@@ Songs — @@description@@","WEA.MusicPages.Meta.Description.Track.AM":"Song · @@duration@@ · @@year@@.","WEA.MusicPages.AlsoAvailable.AM.AX":"View @@albumName@@ in Apple Music","WEA.MusicPages.Track.Social.PageDescriptionLine2.TrackPrice":"for @@trackPrice@@.","WEA.MusicPages.Meta.Description.AlbumPrice.iTunes":"Buy the album for @@formattedPrice@@.","WEA.AppPages.WhatsNew.Header":"What's New","WEA.MusicPages.FeaturedArtists":"Featured Artists","WEA.MoviePages.MetaDescription.AM":"Movie · @@genre@@ · @@releaseYear@@ · @@runtimeInMinutes@@","WEA.ShowPages.Languages.Title":"Languages","WEA.AudiobookPages.Meta.PageKeywords":"@@audiobookName@@, @@authorName@@, @@categoryName@@, audiobooks, books, itunes","WEA.BookPages.FB.siteName.ibookTextbook":"iBooks","WEA.EpisodePages.Twitter.site.episode":"@appleMusic","WEA.ArtistPages.Meta.Movie_Artist.Title.iTunes":"@@artistName@@ Movies on iTunes","WEA.ArtistPages.Artist.PageDescription.TopListings.Three":"Preview and download songs and albums by @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" and \"@@listing3@@.\"","WEA.ShowPages.Information.Title":"Information","WEA.LocalNav.Title.Preview.Podcasts":"@@product@@ @@qualifier@@","WEA.ShowPages.ArtistsOnThisEpisode":"Artists in This Episode","WEA.AppPages.Size":"Size","WEA.Common.Minutes.abbr.one":"1 min","WEA.ShowPages.Description":"DESCRIPTION","WEA.AppPages.Screenshots.iphone":"iPhone","WEA.Error.Generic.Open.Action.AM":"Open in","WEA.ShowPages.Accessibility.hasAD":"AD","WEA.ShowPages.Accessibility.AD":"Audio description refers to a narration track describing what is happening on screen to provide context for those who are blind or have low vision.","WEA.EpisodePages.Twitter.domain.episode":"Apple Music","WEA.ArtistPages.Meta.Software_Artist.Title.iTunes":"@@artistName@@ Apps on the App Store","WEA.Common.FileSize.MB":"@@count@@ MB","WEA.AppPages.Availability.macOS":"Open the Mac App Store to buy and download apps.","WEA.MusicPages.FB.siteName.preorderAlbum.AM":"Apple Music","WEA.ShowPages.Twitter.site.show":"@appleMusic","WEA.ArtistPages.Movie_Artist.PageKeywords.WithoutGenre":"download, @@artistName@@, movies, itunes","WEA.ArtistPages.CTA.AM.AX":"View on Apple Music","WEA.Common.Languages.SDH":"SDH","WEA.Common.Ratings.one":"1 Rating","WEA.Common.Languages.hasDolby":"Dolby 5.1","WEA.Error.NativeMissing.iTunes.Title":"We could not find iTunes on your computer.","WEA.LocalNav.Title.Preview.iTunes":"@@product@@ @@qualifier@@","WEA.MusicPages.Meta.Description.TrackPrice.iTunes":"Songs start at @@cheapestTrackPrice@@.","WEA.Common.LastUpdated.Today":"Updated Today","WEA.ArtistPages.Meta.Podcasts_Artist.Title.iTunes":"@@artistName@@ Podcasts on iTunes","WEA.ShowPages.title":"@@showName@@ on Apple Music","WEA.Common.Roles.Type.Host":"Host","WEA.ArtistPages.LatestRelease":"Latest Release","WEA.AppPages.GameController":"Game Controller","WEA.Common.FileSize.KB.AX.one":"1 kilobyte","WEA.MusicPages.Preview.Resume.AX":"Continue playing current preview","WEA.SocialProfilePages.Meta.PageDescription.one":"1 Playlist","WEA.MusicPages.Upsell.LearnMore":"Learn more about Apple\u0026nbsp;Music","WEA.EditorialItemProductPages.Meta.PageMetaDescription":"Learn about @@storyTitle@@ on App Store. ","WEA.ShowPages.Information.Genre":"Genre","WEA.AppPages.MoreAppsByDeveloperName":"More Apps by @@developerName@@","WEA.ShowPages.Accessibility.hasCC":"CC","WEA.AppPages.OffersAppleWatchAppForiPhone":"Offers Apple Watch App for iPhone","WEA.MusicPages.MusicVideosBy":"Music Videos by @@artistName@@","WEA.AppPages.Twitter.site.desktopApp":"@MacAppStore","WEA.ArtistPages.AppleMusic.Artist.PageDescription.TopListings.ManyMore":"Listen to songs and albums by @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" \"@@listing3@@,\" and many more.","WEA.MusicPages.FB.siteName.album.iTunes":"iTunes","WEA.MusicPages.AppleMusic.PageDescriptionLine2.AlbumPrice":"Buy the album for @@formattedPrice@@.","WEA.SportingEventPages.WatchOnBrands.one":"Watch on @@brandList@@","WEA.MusicPages.FB.siteName.album":"iTunes","WEA.AppPages.Screenshots.ipad":"iPad","WEA.DeepLinkPages.Social.Invite.Title.AM":"Start Sharing on Apple Music","WEA.Error.Generic.Subtitle.DownloadLink.URL":"http://www.apple.com/itunes/download/","WEA.MusicVideoPages.AppleMusic.PageDescriptionLine1":"Music video · @@year@@ · @@duration@@","WEA.ArtistPages.Prerelease.Title":"Pre-Release","WEA.ArtistPages.Studio.PageKeywords":"@@studioName@@, studio, itunes","WEA.MusicPages.PageDescriptionLine1.TopListings.One":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@\".","WEA.AppPages.CTA.MacAppStore.App":"Mac App Store","WEA.MusicPages.AppleMusic.PageDescriptionLine2.Subscription":"Free with Apple Music subscription.","WEA.ArtistPages.FB.siteName.artist.AM":"Apple Music","WEA.ShowPages.SeasonNumber":"SEASON @@seasonNumber@@","WEA.MusicPages.AppleMusic.title":"@@albumName@@ by @@artistName@@","WEA.LocalNav.Title.Preview.MAS":"@@product@@ @@qualifier@@","WEA.PlaylistPages.Meta.Title.Social":"@@playlistName@@ by @@artistName@@","WEA.Common.TrackList.Price":"PRICE","WEA.AppPages.Supports.Wallet.Title":"Wallet","WEA.ArtistPages.Software_Artist.PageDescription.TopListings.Three":"Download iPhone and iPad apps by @@artistName@@, including @@listing1@@, @@listing2@@, and @@listing3@@.","WEA.AudiobookPages.Meta.PageMetaDescription":"Listen to a free sample or buy @@audiobookName@@ by @@authorName@@ on iTunes on your iPhone, iPad, iPod touch, or Mac.","WEA.MusicPages.Twitter.site.preorderAlbum":"@iTunes","WEA.MusicPages.Instagram.AX":"Go to instagram profile for user @@handle@@.","WEA.AppPages.CTA.AppleSchool.App":"Apple School","WEA.Common.Free":"Free","WEA.Common.YearFormat.AX":"YYYY","WEA.EditorialItemProductPages.GameOfTheDay":"GAME OF THE DAY","WEA.MusicPages.Meta.Description.AM.one":"Album · @@year@@ · 1 Song.","WEA.Common.Languages.hasAudioDescription":"Audio Description","WEA.MusicPages.Track.Social.title":"\"@@trackName@@\" from @@albumName@@ by @@artistName@@ on iTunes","WEA.Common.Languages.Subtitled":"Subtitled","WEA.ShowPages.Languages.Primary":"Primary","WEA.EditorialItemProductPages.CTA.Headline":"Get the Full Experience","WEA.MusicPages.AppleMusic.Track.Social.PageDescriptionLine2.Subscription":"Free with Apple Music subscription.","WEA.LocalNav.CTA.DownloadiTunes.url":"https://www.apple.com/itunes/download/","WEA.Common.Percentage":"@@percentage@@%","WEA.MusicVideoPages.PageKeywords":"buy, download, @@songName@@, @@artistName@@, music video, songs, itunes","WEA.PlaylistPages.Meta.Description.one":"Playlist · 1 Song — @@description@@","WEA.MoviePages.Twitter.domain.show.AM":"Apple Music","WEA.Common.FileSize.MB.AX.one":"1 megabyte","WEA.ArtistPages.AppleMusic.Artist.PageDescription.TopListings.Three":"Listen to songs and albums by @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" and \"@@listing3@@.\"","WEA.MusicPages.Albums":"Albums","WEA.MusicVideoPages.CTA.iTunes.App":"iTunes","WEA.DeepLinkPages.Social.Invite.Description.AM":"Discover music with friends","WEA.Error.NotFound.sporting-event":"This content is no longer available","WEA.SocialProfilePages.User.ListensTo":"See what @@fullName@@ listens to","WEA.AppPages.FB.siteName.mobileSoftwareBundle":"App Store","WEA.ArtistPages.iTunes_U_Artist.pageTitle":"@@artistName@@ Courses on iTunes","WEA.ShowPages.PageKeywords":"Watch, @@showName@@, music, singles, songs, @@genreName@@, streaming music, apple music","WEA.LocalNav.CTA.DownloadiTunes":"Download iTunes","WEA.Common.TrackList.Track":"TITLE","WEA.AppPages.CTA.AppleSchool.AX":"View in Apple School","WEA.AppPages.VersionHistory.Title":"Version History","WEA.Common.VideoSubType.tvextra":"EXTRA","WEA.ArtistPages.CTA.AM.Action":"View on","WEA.BookPages.FB.siteName.book":"iTunes","WEA.LocalNav.Store.AppStore":"App Store","WEA.ShowPages.Accessibility.CC":"Closed captions refer to subtitles in the available language with addition of relevant nondialogue information.","WEA.AppPages.Twitter.domain.iosSoftware":"AppStore","WEA.ArtistPages.MusicVideos":"Music Videos","WEA.Common.FileSize.byte.other":"@@count@@ bytes","WEA.MoviePages.RottenTomatoes.Summary.Reviews.Total.Title":"Reviews","WEA.ShowPages.RelatedShows":"Related TV Shows","WEA.AppBundlePages.PurchasedSeparately":"Purchased Separately","WEA.AppPages.Languages":"Languages","WEA.EpisodePages.Meta.Description.Social":"@@releaseDate@@ · @@runtimeInMinutes@@","WEA.Common.Roles.Type.Performer":"Performer","WEA.EpisodePages.PageKeywords":"Watch, “@@episodeName@@”, music, singles, songs, @@genreName@@, streaming music, apple music","WEA.Common.Close":"Close","WEA.MusicPages.Twitter.domain.album.iTunes":"iTunes","WEA.MoviePages.MoreByActors":"More By These Actors","WEA.ShowPages.Information.Released":"Released","WEA.Error.NativeMissing.Other.iTunes":"Get iTunes on iOS, Android, Mac, and Windows","WEA.ShowPages.Accessibility.hasHD":"HD","WEA.AppPages.Screenshots.iphoneScreenshots":"iPhone Screenshots","WEA.LocalNav.Preview.MAS":"Preview","WEA.EditorialItemProductPages.Social.title.IAP":"In-App Purchase: @@appName@@","WEA.LocalNav.Store.Podcasts":"Podcasts","WEA.ShowPages.SongsInThisEpisode":"Songs in This Episode","WEA.MusicVideoPages.MusicVideoInGenre":"Music Videos in @@genreName@@","WEA.AppPages.CustomersAlsoBought.Title":"You May Also Like","WEA.Common.Roles.Type.Music":"Music","WEA.ShowPages.Languages.Additional":"Additional","WEA.MusicVideoPages.ArtistLink.AX":"View page for artist @@artistName@@","WEA.AppPages.Meta.MacAppPageMetaKeywords":"@@softwareName@@, @@developerName@@, @@categoryNames@@, mac apps, app store, appstore, applications, itunes","WEA.ArtistPages.Books":"Books","WEA.Common.Meta.FB.siteName.iTunes":"iTunes","WEA.SocialProfilePages.PrivacyLink.Text":"Apple Music and Privacy","WEA.MoviePages.Information.Format.Widescreen":"Widescreen","WEA.MusicPages.Preview.Song.AX":"Preview \"@@songName@@\" by @@artistName@@","WEA.MoviePages.FB.siteName.show.iTunes":"iTunes","WEA.MusicPages.Hometown":"HOMETOWN","WEA.MoviePages.MetaDescription.iTunes.buy.noDirector":"Watch trailers, read customer and critic reviews, and buy @@movieName@@ for @@buyPrice@@.","WEA.MusicPages.Meta.Description.TopListings.ManyMore.iTunes":"Preview, buy, and download songs from the album @@albumName@@, including \"@@listing1@@,\" \"@@listing2@@,\" \"@@listing3@@,\" and many more.","WEA.ArtistPages.Software_Artist.pageTitle":"@@artistName@@ Apps on the App Store","WEA.AppPages.AX.ViewIn":"View On","WEA.ArtistPages.Podcast_Artist.PageKeywords":"download, @@artistName@@, podcasts, itunes","WEA.Common.Share.EmbedCopied":"Embed Code Copied","WEA.ArtistPages.Twitter.domain.artist":"iTunes","WEA.MoviePages.Information.Format.Square":"Square","WEA.AppPages.Screenshots.ipadScreenshots":"iPad Screenshots","WEA.ArtistPages.iTunes_U_Artist.PageDescription.TopListings.Three":"Preview and download courses and lectures from @@artistName@@, including \"@@listing1@@,\" \"@@listing2@@,\" and \"@@listing3@@.\"","WEA.MoviePages.MetaDescription.iTunes.buy":"Watch trailers, read customer and critic reviews, and buy @@movieName@@ directed by @@directorName@@ for @@buyPrice@@.","WEA.DeepLinkPages.Social.Subscribe.Title.AM":"Try Apple Music","WEA.ShowPages.Meta.PageMetaDescription.other":"TV Show · @@genreName@@ · @@year@@ · @@count@@ episodes — @@description@@","WEA.AppPages.Screenshots":"Screenshots"}</script><script type="fastboot/shoebox" id="shoebox-ember-data-store">{"data":{"type":"product/app","id":"389801252","attributes":{"userRating":{"value":4.8,"ratingCount":6193151,"ratingCountList":[87627,43416,157429,533804,5370875],"ariaLabelForRatings":"4.8 stars"},"deviceFamilies":["iphone","ipod"],"metricsBase":{"pageType":"Software","pageId":"389801252","pageDetails":"Instagram, Inc._Instagram","page":"Software_389801252","serverInstance":"3006304","storeFrontHeader":"","language":"1","platformId":"8","platformName":"ItunesPreview","storeFront":"143441","environmentDataCenter":"MR22"},"contentRating":{"name":"12+","value":300,"rank":3,"advisories":["Infrequent/Mild Alcohol, Tobacco, or Drug Use or References","Infrequent/Mild Profanity or Crude Humor","Infrequent/Mild Sexual Content and Nudity","Infrequent/Mild Mature/Suggestive Themes"]},"copyright":"© 2015 Instagram, LLC.","description":"Instagram is a simple way to capture and share the world’s moments. Follow your friends and family to see what they’re up to, and discover accounts from all over the world that are sharing things you love. Join the community of over 1 billion people and express yourself by sharing all the moments of your day — the highlights and everything in between, too.\n\nUse Instagram to:\n\n* Post photos and videos you want to keep on your profile grid. Edit them with filters and creative tools and combine multiple clips into one video.\n* Browse photos and videos from people you follow in your feed. Interact with posts you care about with likes and comments.\n* Share multiple photos and videos (as many as you want!) to your story. Bring them to life with text, drawing tools and other creative effects. . They disappear after 24 hours and won’t appear on your profile grid or in feed.\n* Go live to connect with your friends in the moment. Try going live with a friend and sharing a replay to your story when you’re done.\n* Message your friends privately in Direct. Send them photos and videos that disappear and share content you see on Instagram.\n* Watch stories and live videos from the people you follow in a bar at the top of your feed.\n* Discover photos, videos and stories you might like and follow new accounts on the Explore tab.","familyShareEnabledDate":"0001-04-23T00:00:00Z","itunesNotes":{"standard":"In the great big crowd of social media apps, Instagram continues to stand out for a reason: it makes sharing moments with everyone in your world easy, speedy, and fun. Whether you’re posting breathtaking vacation photos tweaked with one of dozens of cool image filters or a video clip of an insane concert, Instagram’s uncluttered accessibility has kept it at the top of the social-sharing heap."},"kind":"iosSoftware","name":"Instagram","ratingText":"Rated 12+ for the following:","advisories":["Infrequent/Mild Alcohol, Tobacco, or Drug Use or References","Infrequent/Mild Profanity or Crude Humor","Infrequent/Mild Sexual Content and Nudity","Infrequent/Mild Mature/Suggestive Themes"],"releaseDate":"2010-10-06","softwareInfo":{"seller":"Instagram, Inc.","languagesDisplayString":"English, Croatian, Czech, Danish, Dutch, Finnish, French, German, Greek, Indonesian, Italian, Japanese, Korean, Malay, Norwegian Bokmål, Polish, Portuguese, Romanian, Russian, Simplified Chinese, Slovak, Spanish, Swedish, Tagalog, Thai, Traditional Chinese, Turkish, Ukrainian, Vietnamese","requirementsString":"Requires iOS 9.0 or later. Compatible with iPhone, iPad, and iPod touch.","eulaUrl":null,"supportUrl":"http://help.instagram.com/","websiteUrl":"http://instagram.com/","privacyPolicyUrl":"http://instagram.com/legal/privacy/","privacyPolicyTextUrl":null},"url":"https://itunes.apple.com/us/app/instagram/id389801252?mt=8","versionHistory":[{"releaseNotes":"We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu.\n\n* Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day.\u2028\n* Daily Reminder: Set a daily reminder to give yourself an alert when you've reached the amount of time you want to spend for the day.\u2028\n* Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications.\u2028\n\nTime on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks.","versionString":"59.0","releaseDate":"2018-08-20T14:26:48Z"},{"releaseNotes":"We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu.\n\n* Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day.\u2028\n* Daily Reminder: Set a daily reminder to give yourself an alert when you've reached the amount of time you want to spend for the day.\u2028\n* Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications.\u2028\n\nTime on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks.","versionString":"58.0","releaseDate":"2018-08-13T15:11:36Z"},{"releaseNotes":"We have begun to roll out new tools to help you manage your time on Instagram. Go to profile and tap “Your Activity” in the settings menu.\n\n* Your Activity: See your average time for Instagram on a device. Tap any bar to see your total time for that day.\u2028\n* Daily Reminder: Set a daily reminder to give yourself an alert when you've reached the amount of time you want to spend for the day.\u2028\n* Mute Push Notifications: Tap “Notification Settings” and turn on “Mute Push Notifications” to limit your Instagram notifications.\u2028\n\nTime on Instagram should be positive, intentional and inspiring. These tools will be available globally in the coming weeks.","versionString":"57.0","releaseDate":"2018-08-06T20:17:45Z"},{"releaseNotes":"Bug fixes and performance improvements.","versionString":"56.0","releaseDate":"2018-07-30T14:02:38Z"},{"releaseNotes":"Bug fixes and performance improvements.","versionString":"55.0","releaseDate":"2018-07-23T15:01:21Z"},{"releaseNotes":"Bug fixes and performance improvements.","versionString":"54.0","releaseDate":"2018-07-16T14:59:25Z"},{"releaseNotes":"We're introducing three new features:\n\n* You can now video chat in Instagram Direct. Swipe into an existing thread and tap the video icon on the top right to video chat with up to four people.\u2028\n* At the top of Explore, you'll now see a tray of topic channels personalized to your interests.\u2028\n* With IGTV, you can now watch long-form, vertical video from your favorite Instagram creators. Tap the new icon at the top right of feed to get started.","versionString":"53.0","releaseDate":"2018-07-09T13:10:28Z"},{"releaseNotes":"Introducing IGTV, a new space for watching long-form, vertical video from your favorite Instagram creators.\n\n* It’s built for how you actually use your phone, so videos are full screen and vertical.\n* IGTV videos aren’t limited to one minute, which means you can see more of your favorite content.\n* Watch videos from creators you already follow and others you might like.\n* Discover new creators and follow them right from IGTV to see more.","versionString":"52.0","releaseDate":"2018-07-02T14:11:06Z"},{"releaseNotes":"Introducing IGTV, a new space for watching long-form, vertical video from your favorite Instagram creators.\n\n* It’s built for how you actually use your phone, so videos are full screen and vertical.\n* IGTV videos aren’t limited to one minute, which means you can see more of your favorite content.\n* Watch videos from creators you already follow and others you might like.\n* Discover new creators and follow them right from IGTV to see more.","versionString":"51.0","releaseDate":"2018-06-25T13:06:32Z"},{"releaseNotes":"Bug fixes and performance improvements.","versionString":"50.0","releaseDate":"2018-06-20T16:03:09Z"},{"releaseNotes":"Bug fixes and performance improvements.","versionString":"49.0","releaseDate":"2018-06-11T13:18:30Z"},{"releaseNotes":"Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices.","versionString":"46.0","releaseDate":"2018-05-21T15:06:05Z"},{"releaseNotes":"Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices.","versionString":"45.0","releaseDate":"2018-05-16T16:51:12Z"},{"releaseNotes":"Instagram now filters out bullying comments intended to harass or upset people in our community. Our Community Guidelines have always prohibited bullying on our platform, and this is the next step in our ongoing commitment to keeping Instagram an inclusive, supportive place for all voices.","versionString":"44.0","releaseDate":"2018-05-07T16:23:22Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"43.0","releaseDate":"2018-04-30T15:25:57Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"41.0","releaseDate":"2018-04-22T00:54:03Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"40.0","releaseDate":"2018-04-09T16:22:44Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"39.0","releaseDate":"2018-04-02T14:44:19Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"38.0","releaseDate":"2018-03-26T13:23:31Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"37.0","releaseDate":"2018-03-19T13:08:31Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"36.0","releaseDate":"2018-03-12T14:12:00Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"35.0","releaseDate":"2018-03-05T16:19:01Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"34.0","releaseDate":"2018-02-26T22:25:30Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"33.0","releaseDate":"2018-02-20T13:26:24Z"},{"releaseNotes":"General bug fixes and performance improvements","versionString":"32.0","releaseDate":"2018-02-14T00:22:19Z"}],"size":144156672,"chartPositionForStore":{"appStore":{"position":2,"genreName":"Photo \u0026 Video","chartUrl":"https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=us\u0026genreId=6008\u0026popId=96"}},"minimumOSVersion":"9.0","iphoneScreenshotsVersion":"iphone6+"},"relationships":{"offers":{"data":[{"type":"offer","id":"st1045583"}]},"developer":{"data":{"type":"lockup/developer","id":"389801255"}},"artwork":{"data":{"type":"image","id":"st1045584"}},"iphoneScreenshots":{"data":[{"type":"image","id":"st1045585"},{"type":"image","id":"st1045586"},{"type":"image","id":"st1045587"},{"type":"image","id":"st1045588"},{"type":"image","id":"st1045589"}]},"subscriptions":{"data":[]},"inAppPurchases":{"data":[]},"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"moreByThisDeveloper":{"data":[{"type":"lockup/app","id":"740146917"},{"type":"lockup/app","id":"967351793"},{"type":"lockup/app","id":"1041596399"},{"type":"lockup/app","id":"1394351700"}]},"customersAlsoBoughtApps":{"data":[{"type":"lockup/app","id":"576649830"},{"type":"lockup/app","id":"577423493"},{"type":"lockup/app","id":"881267423"},{"type":"lockup/app","id":"884009993"},{"type":"lockup/app","id":"553807264"},{"type":"lockup/app","id":"543577420"},{"type":"lockup/app","id":"438596432"},{"type":"lockup/app","id":"587366035"},{"type":"lockup/app","id":"1338605092"},{"type":"lockup/app","id":"516561342"},{"type":"lockup/app","id":"835599320"},{"type":"lockup/app","id":"583555212"},{"type":"lockup/app","id":"1216590966"},{"type":"lockup/app","id":"768469908"},{"type":"lockup/app","id":"510873505"}]},"reviews":{"data":[]}}},"included":[{"type":"offer","id":"st1045583","attributes":{"actionText":{"short":"Get","medium":"Get","long":"Get App","downloaded":"Installed","downloading":"Installing"},"assets":[{"flavor":"iosSoftware","size":144156672}],"buyParams":"productType=C\u0026price=0\u0026salableAdamId=389801252\u0026pricingParameters=STDQ\u0026pg=default\u0026appExtVrsId=828215808","price":0,"priceFormatted":"$0.00","type":"get"},"relationships":{}},{"type":"lockup/developer","id":"389801255","attributes":{"name":"Instagram, Inc.","url":"https://itunes.apple.com/us/developer/instagram-inc/id389801255?mt=8"},"relationships":{}},{"type":"image","id":"st1045584","attributes":{"bgColor":"ec5e43","height":1024,"supportsLayeredImage":false,"textColor1":"161616","textColor2":"161616","textColor3":"41251f","textColor4":"41251f","url":"https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8e/ec/f4/8eecf4fb-bb33-4bec-1b88-62290eed7b60/Prod-1x_U007emarketing-85-220-0-5.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045585","attributes":{"bgColor":"f9f9f9","height":2208,"supportsLayeredImage":false,"textColor1":"502015","textColor2":"0a3559","textColor3":"714b43","textColor4":"3a5d79","url":"https://is1-ssl.mzstatic.com/image/thumb/Purple125/v4/aa/30/5f/aa305f59-acc6-29fc-4d30-2d7d792fff6f/mzl.vaqjklrx.jpg/{w}x{h}bb.{f}","width":1242,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045586","attributes":{"bgColor":"bd8a6b","height":2208,"supportsLayeredImage":false,"textColor1":"0e0c0b","textColor2":"2a1c14","textColor3":"31251e","textColor4":"473225","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/c9/8a/13/c98a1303-bb95-434d-4417-4187bd3ff1d4/pr_source.jpg/{w}x{h}bb.{f}","width":1242,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045587","attributes":{"bgColor":"f9f9f9","height":2208,"supportsLayeredImage":false,"textColor1":"000000","textColor2":"181818","textColor3":"313131","textColor4":"454545","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/bc/9b/74/bc9b74fe-2efc-61c7-4c26-4590612886e4/mzl.eislmasw.jpg/{w}x{h}bb.{f}","width":1242,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045588","attributes":{"bgColor":"3b0f00","height":2208,"supportsLayeredImage":false,"textColor1":"cac8d1","textColor2":"d2aa92","textColor3":"ada3a7","textColor4":"b38b75","url":"https://is1-ssl.mzstatic.com/image/thumb/Purple115/v4/57/fd/7a/57fd7a93-2433-4422-7137-d4304a861630/mzl.ovaynfwc.jpg/{w}x{h}bb.{f}","width":1242,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045589","attributes":{"bgColor":"ffffff","height":2208,"supportsLayeredImage":false,"textColor1":"000000","textColor2":"26221c","textColor3":"333333","textColor4":"514e4a","url":"https://is4-ssl.mzstatic.com/image/thumb/Purple115/v4/98/44/ee/9844eecd-56b9-41d5-9e38-39577ce2cacb/mzl.wmzfxyon.png/{w}x{h}bb.{f}","width":1242,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st77071","attributes":{"bgColor":"1fdcff","height":1024,"supportsLayeredImage":false,"textColor1":"11020b","textColor2":"12050d","textColor3":"142d3c","textColor4":"15303d","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple128/v4/9a/4f/53/9a4f530f-df2e-0917-f5bd-10dbebcba21a/AppIconVS-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1575737","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"180b3d","textColor2":"083166","textColor3":"463c64","textColor4":"3a5a84","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple128/v4/34/8e/ad/348ead4e-379f-bf1d-b6fd-984e0b4fcff6/AppIcon-AppStore-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045595","attributes":{"bgColor":"f4f4f4","height":1024,"supportsLayeredImage":false,"textColor1":"090909","textColor2":"301e18","textColor3":"383838","textColor4":"574944","url":"https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/ee/5a/16/ee5a16da-a552-eeaa-ae29-a2b91e377b6c/AppIcon-1x_U007emarketing-85-220-3.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045596","attributes":{"bgColor":"13c15d","height":1024,"supportsLayeredImage":false,"textColor1":"0a0502","textColor2":"161616","textColor3":"0c2b14","textColor4":"163825","url":"https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/31/c5/4e/31c54e8d-1f57-3a86-ae40-0f0b674c15fd/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-5.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045597","attributes":{"bgColor":"4ab8b2","height":1024,"supportsLayeredImage":false,"textColor1":"040404","textColor2":"121414","textColor3":"122827","textColor4":"1d3533","url":"https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/de/f0/30/def03079-20ea-f43c-2dbd-fb9a014b60be/mzl.ztlfvllh.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045598","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"000000","textColor2":"000072","textColor3":"333333","textColor4":"33338e","url":"https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/be/f8/cd/bef8cdf6-f3c7-7356-4306-01b3dea971f0/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-9.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045599","attributes":{"bgColor":"cc2800","height":1024,"supportsLayeredImage":false,"textColor1":"ffffff","textColor2":"ffd9d0","textColor3":"f4d4cb","textColor4":"f4b5a6","url":"https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/25/a6/70/25a6708f-ffeb-9089-1189-258fadf49dbf/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-4.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st73267","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"000000","textColor2":"323234","textColor3":"333333","textColor4":"5b5b5c","url":"https://is1-ssl.mzstatic.com/image/thumb/Purple62/v4/2f/86/e1/2f86e147-9e6c-1a6f-f99a-93407ad10a47/AppIcon-1x_U007emarketing-85-220-5.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st6577938","attributes":{"bgColor":"8881e9","height":1024,"supportsLayeredImage":false,"textColor1":"161516","textColor2":"161616","textColor3":"2d2b40","textColor4":"2d2c40","url":"https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/6c/52/67/6c526733-9d14-f6c0-725e-62371a5b2b6f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st73269","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"3f1548","textColor2":"551444","textColor3":"66446c","textColor4":"77436a","url":"https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/45/b2/70/45b27019-9eca-3c99-0a2e-8acc71752ba0/AppIcon-1x_U007emarketing-85-220-4.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st8236533","attributes":{"bgColor":"8e1eb3","height":1024,"supportsLayeredImage":false,"textColor1":"ffffff","textColor2":"cc9bfb","textColor3":"e8d2ef","textColor4":"bf82ed","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple128/v4/74/a9/04/74a904fa-19a3-00e9-a3c9-28448986008f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st77049","attributes":{"bgColor":"0b0b16","height":1024,"supportsLayeredImage":false,"textColor1":"ffffff","textColor2":"fe2c55","textColor3":"ceced0","textColor4":"cd2548","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/4a/ca/23/4aca232c-1223-7e65-c906-7fddfca7ba25/M_AppIcon-1x_U007emarketing-85-220-0-5.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045601","attributes":{"bgColor":"506387","height":1024,"supportsLayeredImage":false,"textColor1":"fcfcfc","textColor2":"cdee78","textColor3":"dadee5","textColor4":"b4d27b","url":"https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/b0/7d/db/b07ddb01-0aa9-dbf7-fbf5-ce1ec029926f/AppIcon-1x_U007emarketing-0-0-GLES2_U002c0-512MB-sRGB-0-0-0-85-220-0-0-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st73272","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"160005","textColor2":"160005","textColor3":"453337","textColor4":"453337","url":"https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/f9/03/a8/f903a807-16ea-710a-539a-8c880a096d4c/AppIcon-1x_U007emarketing-85-220-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045602","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"32144a","textColor2":"5b1333","textColor3":"5b436e","textColor4":"7c425c","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple118/v4/c0/7b/6b/c07b6bc2-4fb7-3d47-d07a-e88f6abdd925/AppIcon-1x_U007emarketing-85-220-3.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st727517","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"4e163e","textColor2":"5b153b","textColor3":"724565","textColor4":"7c4362","url":"https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/e2/10/33/e210337e-154a-f998-7269-d9fa9c0d9866/AppIcon-1x_U007emarketing-85-220-4.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st856390","attributes":{"bgColor":"a70083","height":1024,"supportsLayeredImage":false,"textColor1":"ffffff","textColor2":"fad9f6","textColor3":"edcbe6","textColor4":"e9aedf","url":"https://is5-ssl.mzstatic.com/image/thumb/Purple128/v4/5d/c1/1a/5dc11a0b-5ac9-6b82-58b4-cd3ae11de256/AppIcon-1x_U007emarketing-85-220-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st3507811","attributes":{"bgColor":"ffffff","height":1024,"supportsLayeredImage":false,"textColor1":"160c00","textColor2":"160c00","textColor3":"453d33","textColor4":"453d33","url":"https://is1-ssl.mzstatic.com/image/thumb/Purple128/v4/10/2f/fb/102ffbf1-db09-dfc4-3ac3-3df5c4baa271/AppIcon-global-1x_U007emarketing-85-220-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"image","id":"st1045605","attributes":{"bgColor":"ffbb11","height":1024,"supportsLayeredImage":false,"textColor1":"16010d","textColor2":"16030b","textColor3":"45260e","textColor4":"45280c","url":"https://is2-ssl.mzstatic.com/image/thumb/Purple128/v4/0c/b0/c3/0cb0c396-4ccf-75c3-f6e0-26667dc44383/AppIcon-1x_U007emarketing-85-220-0-6.png/{w}x{h}bb.{f}","width":1024,"hasAlpha":false},"relationships":{}},{"type":"genre","id":"st16883","attributes":{"mediaType":"8","name":"Photo \u0026 Video","url":"https://itunes.apple.com/us/genre/id6008"},"relationships":{}},{"type":"genre","id":"st15480","attributes":{"mediaType":"8","name":"Social Networking","url":"https://itunes.apple.com/us/genre/id6005"},"relationships":{}},{"type":"genre","id":"st15967","attributes":{"mediaType":"8","name":"Entertainment","url":"https://itunes.apple.com/us/genre/id6016"},"relationships":{}},{"type":"genre","id":"st5415","attributes":{"mediaType":"8","name":"Utilities","url":"https://itunes.apple.com/us/genre/id6002"},"relationships":{}},{"type":"genre","id":"st13741","attributes":{"mediaType":"8","name":"Lifestyle","url":"https://itunes.apple.com/us/genre/id6012"},"relationships":{}},{"type":"lockup/app","id":"740146917","attributes":{},"relationships":{}},{"type":"lockup/app","id":"967351793","attributes":{},"relationships":{}},{"type":"lockup/app","id":"1041596399","attributes":{},"relationships":{}},{"type":"lockup/app","id":"1394351700","attributes":{},"relationships":{}},{"type":"lockup/app","id":"576649830","attributes":{},"relationships":{}},{"type":"lockup/app","id":"577423493","attributes":{},"relationships":{}},{"type":"lockup/app","id":"881267423","attributes":{},"relationships":{}},{"type":"lockup/app","id":"884009993","attributes":{},"relationships":{}},{"type":"lockup/app","id":"553807264","attributes":{},"relationships":{}},{"type":"lockup/app","id":"543577420","attributes":{},"relationships":{}},{"type":"lockup/app","id":"438596432","attributes":{},"relationships":{}},{"type":"lockup/app","id":"587366035","attributes":{},"relationships":{}},{"type":"lockup/app","id":"1338605092","attributes":{},"relationships":{}},{"type":"lockup/app","id":"516561342","attributes":{},"relationships":{}},{"type":"lockup/app","id":"835599320","attributes":{},"relationships":{}},{"type":"lockup/app","id":"583555212","attributes":{},"relationships":{}},{"type":"lockup/app","id":"1216590966","attributes":{},"relationships":{}},{"type":"lockup/app","id":"768469908","attributes":{},"relationships":{}},{"type":"lockup/app","id":"510873505","attributes":{},"relationships":{}},{"type":"lockup/app","id":"438596432","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"286083972","artistName":"Frontier Design Group","artistUrl":"https://itunes.apple.com/us/developer/frontier-design-group/id286083972?mt=8","kind":"iosSoftware","name":"Video Star","url":"https://itunes.apple.com/us/app/video-star/id438596432?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15967"}]},"artwork":{"data":{"type":"image","id":"st77071"}}}},{"type":"lockup/app","id":"510873505","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"510873769","artistName":"KeepSafe Software, Inc.","artistUrl":"https://itunes.apple.com/us/developer/keepsafe-software-inc/id510873769?mt=8","kind":"iosSoftware","name":"Secret Photo Vault - Keepsafe","url":"https://itunes.apple.com/us/app/secret-photo-vault-keepsafe/id510873505?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st5415"}]},"artwork":{"data":{"type":"image","id":"st1575737"}}}},{"type":"lockup/app","id":"516561342","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"359067226","artistName":"LINE Corporation","artistUrl":"https://itunes.apple.com/us/developer/line-corporation/id359067226?mt=8","kind":"iosSoftware","name":"LINE Camera - Photo editor","url":"https://itunes.apple.com/us/app/line-camera-photo-editor/id516561342?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"}]},"artwork":{"data":{"type":"image","id":"st1045595"}}}},{"type":"lockup/app","id":"543577420","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"615987923","artistName":"KS Mobile, Inc.","artistUrl":"https://itunes.apple.com/us/developer/ks-mobile-inc/id615987923?mt=8","kind":"iosSoftware","name":"PhotoGrid - Video \u0026 Pic Editor","url":"https://itunes.apple.com/us/app/photogrid-video-pic-editor/id543577420?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st13741"}]},"artwork":{"data":{"type":"image","id":"st1045596"}}}},{"type":"lockup/app","id":"553807264","attributes":{"deviceFamilies":["iphone","ipod"],"artistId":"346128080","artistName":"SK COMMUNICATIONS Co.,LTD","artistUrl":"https://itunes.apple.com/us/developer/sk-communications-co-ltd/id346128080?mt=8","kind":"iosSoftware","name":"Cymera","url":"https://itunes.apple.com/us/app/cymera/id553807264?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st1045597"}}}},{"type":"lockup/app","id":"576649830","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"576649833","artistName":"Munkee Apps L.L.C.","artistUrl":"https://itunes.apple.com/us/developer/munkee-apps-l-l-c/id576649833?mt=8","kind":"iosSoftware","name":"InstaSize Photo Editor \u0026 Grid","url":"https://itunes.apple.com/us/app/instasize-photo-editor-grid/id576649830?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st1045598"}}}},{"type":"lockup/app","id":"577423493","attributes":{"hasMessagesExtension":true,"deviceFamilies":["iphone","ipod"],"artistId":"958446752","artistName":"Retrica, Inc.","artistUrl":"https://itunes.apple.com/us/developer/retrica-inc/id958446752?mt=8","kind":"iosSoftware","name":"Retrica","url":"https://itunes.apple.com/us/app/retrica/id577423493?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st13741"}]},"artwork":{"data":{"type":"image","id":"st1045599"}}}},{"type":"lockup/app","id":"583555212","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"583555215","artistName":"YU BO","artistUrl":"https://itunes.apple.com/us/developer/yu-bo/id583555215?mt=8","kind":"iosSoftware","name":"Cute CUT","url":"https://itunes.apple.com/us/app/cute-cut/id583555212?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15967"}]},"artwork":{"data":{"type":"image","id":"st73267"}}}},{"type":"lockup/app","id":"587366035","attributes":{"hasMessagesExtension":true,"deviceFamilies":["iphone","ipad","ipod"],"artistId":"587366038","artistName":"PicsArt, Inc.","artistUrl":"https://itunes.apple.com/us/developer/picsart-inc/id587366038?mt=8","kind":"iosSoftware","name":"PicsArt Photo Editor \u0026 Collage","url":"https://itunes.apple.com/us/app/picsart-photo-editor-collage/id587366035?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st6577938"}}}},{"type":"lockup/app","id":"740146917","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"389801255","artistName":"Instagram, Inc.","artistUrl":"https://itunes.apple.com/us/developer/instagram-inc/id389801255?mt=8","kind":"iosSoftware","name":"Hyperlapse from Instagram","url":"https://itunes.apple.com/us/app/hyperlapse-from-instagram/id740146917?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st73269"}}}},{"type":"lockup/app","id":"768469908","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"1018779369","artistName":"Perfect Corp.","artistUrl":"https://itunes.apple.com/us/developer/perfect-corp/id1018779369?mt=8","kind":"iosSoftware","name":"YouCam Perfect - Photo Editor","url":"https://itunes.apple.com/us/app/youcam-perfect-photo-editor/id768469908?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15967"}]},"artwork":{"data":{"type":"image","id":"st8236533"}}}},{"type":"lockup/app","id":"835599320","attributes":{"deviceFamilies":["iphone","ipod"],"artistId":"1039610913","artistName":"musical.ly Inc.","artistUrl":"https://itunes.apple.com/us/developer/musical-ly-inc/id1039610913?mt=8","kind":"iosSoftware","name":"TikTok - including musical.ly","url":"https://itunes.apple.com/us/app/tiktok-including-musical-ly/id835599320?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st77049"}}}},{"type":"lockup/app","id":"881267423","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"940917968","artistName":"JP Brothers, Inc.","artistUrl":"https://itunes.apple.com/us/developer/jp-brothers-inc/id940917968?mt=8","kind":"iosSoftware","name":"Candy Camera","url":"https://itunes.apple.com/us/app/candy-camera/id881267423?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15967"}]},"artwork":{"data":{"type":"image","id":"st1045601"}}}},{"type":"lockup/app","id":"884009993","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"884009996","artistName":"Lomotif Private Limited","artistUrl":"https://itunes.apple.com/us/developer/lomotif-private-limited/id884009996?mt=8","kind":"iosSoftware","name":"Lomotif - Music Video Editor","url":"https://itunes.apple.com/us/app/lomotif-music-video-editor/id884009993?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st73272"}}}},{"type":"lockup/app","id":"967351793","attributes":{"deviceFamilies":["iphone","ipod"],"artistId":"389801255","artistName":"Instagram, Inc.","artistUrl":"https://itunes.apple.com/us/developer/instagram-inc/id389801255?mt=8","kind":"iosSoftware","name":"Layout from Instagram","url":"https://itunes.apple.com/us/app/layout-from-instagram/id967351793?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"}]},"artwork":{"data":{"type":"image","id":"st1045602"}}}},{"type":"lockup/app","id":"1041596399","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"389801255","artistName":"Instagram, Inc.","artistUrl":"https://itunes.apple.com/us/developer/instagram-inc/id389801255?mt=8","kind":"iosSoftware","name":"Boomerang from Instagram","url":"https://itunes.apple.com/us/app/boomerang-from-instagram/id1041596399?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st727517"}}}},{"type":"lockup/app","id":"1216590966","attributes":{"deviceFamilies":["iphone","ipod"],"artistId":"1216139452","artistName":"Alpha Mobile (Hong Kong) Limited","artistUrl":"https://itunes.apple.com/us/developer/alpha-mobile-hong-kong-limited/id1216139452?mt=8","kind":"iosSoftware","name":"Photable - Photo Editor Pro","url":"https://itunes.apple.com/us/app/photable-photo-editor-pro/id1216590966?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15967"}]},"artwork":{"data":{"type":"image","id":"st856390"}}}},{"type":"lockup/app","id":"1338605092","attributes":{"deviceFamilies":["iphone","ipad","ipod"],"artistId":"1417178575","artistName":"KWAI INC","artistUrl":"https://itunes.apple.com/us/developer/kwai-inc/id1417178575?mt=8","kind":"iosSoftware","name":"Kwai - Video Social Network","url":"https://itunes.apple.com/us/app/kwai-video-social-network/id1338605092?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st3507811"}}}},{"type":"lockup/app","id":"1394351700","attributes":{"deviceFamilies":["iphone","ipod"],"artistId":"389801255","artistName":"Instagram, Inc.","artistUrl":"https://itunes.apple.com/us/developer/instagram-inc/id389801255?mt=8","kind":"iosSoftware","name":"IGTV","url":"https://itunes.apple.com/us/app/igtv/id1394351700?mt=8"},"relationships":{"genres":{"data":[{"type":"genre","id":"st16883"},{"type":"genre","id":"st15480"}]},"artwork":{"data":{"type":"image","id":"st1045605"}}}}]}</script><script type="fastboot/shoebox" id="shoebox-ember-locale-store">{"priceCurrency":"USD","storefrontId":"143441","languageCode":"en-us","storefront":"US"}</script><script type="fastboot/shoebox" id="shoebox-metrics-base">{"pageType":"Software","pageId":"389801252","pageDetails":"Instagram, Inc._Instagram","page":"Software_389801252","serverInstance":"3006304","storeFrontHeader":"","language":"1","platformId":"8","platformName":"ItunesPreview","storeFront":"143441","environmentDataCenter":"MR22"}</script><script type="fastboot/shoebox" id="shoebox-global-elements">{"isLoaded":true}</script><script type="x/boundary" id="fastboot-body-end"></script>

    <script src="https://web-experience.itunes.apple.com/assets/vendor-464a9623b4c031f64356fa1e8fae0ada.js"></script>
    <script src="https://web-experience.itunes.apple.com/assets/web-experience-app-106bce7bac4e399b3429e7e03193f36d.js"></script>

    <div id="ember-basic-dropdown-wormhole"></div>
  </body>
</html>
        ''']

        data = [
            {
                'app_store_url': u'https://itunes.apple.com/us/app/id389801252',
                'app_name': u'Instagram'
            }
        ]

        fetched_data = gather_data(data)

        valid_data = [
            {
                'name': u'Instagram',
                'app_identifier': 389801252,
                'minimum_version': u'9.0',
                'languages': [u'English', u'Croatian', u'Czech', u'Danish', u'Dutch', u'Finnish', u'French', u'German', u'Greek', u'Indonesian', u'Italian', u'Japanese', u'Korean', u'Malay', u'Norwegian Bokmål', u'Polish', u'Portuguese', u'Romanian', u'Russian', u'Simplified Chinese', u'Slovak', u'Spanish', u'Swedish', u'Tagalog', u'Thai', u'Traditional Chinese', u'Turkish', u'Ukrainian', u'Vietnamese']
            }
        ]

        self.assertEqual(self._compare_list(fetched_data, valid_data), True)

if __name__ == '__main__':
    unittest.main()