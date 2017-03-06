import requests
import re
from collections import OrderedDict
from urllib.parse import urlencode
from urllib.request import urlopen
from lxml import html

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Client (object):


    def __init__ (self, cse_id, api_key):
        if not cse_id:
            #throw error without CSE
            raise ValueError("Expected a Custom Search Engine ID")
        if not api_key:
            #throw error with API Key
            raise ValueError("Expected an API Key")

        self.endpoint = 'https://www.googleapis.com'
        self.cse_id = cse_id
        self.api_key = api_key

    def search(self, query, method, options={}, limit=10):

        """
        gsc stands for: Google Custom Search Engine

        :param query: Pass what to search
        :param options: search params for custom search engine (optional)
        :param method: how to get the links, be aware that with crawler, you get the links directly
        :return: list with found elements
        """
        items = []

        if method == 'gcse':
            if not query :
                raise ValueError("Expected a query!")

            if not options:
                raise ValueError("Expected options dict")

            __url = "{0}/customsearch/v1?{1}".format(self.endpoint, self.buildQuery(query, options))
            items = requests.get(__url).json()['items']

            response = requests.get(__url).json()['items']
            for item in response:
                items.append({
                    'type': item['mime'],
                    'width': item['image']['width'],
                    'height': item['image']['height'],
                    'size': item['image']['byteSize'],
                    'url': item['link'],
                    'thumbnail': {
                        'url': item['image']['thumbnailLink'],
                        'width': item['image']['thumbnailWidth'],
                        'height': item['image']['thumbnailHeight']
                    },
                    'description': item['snippet'],
                    'parentPage': item['image']['contextLink']
                })
        elif method == 'crawler':
            #do crawler stuff to get the images json
            #create the url to search
            # make get request
            # get the content of the request
            # store in items
            __url = 'https://disneyworld.disney.go.com/pt/attractions/magic-kingdom/'

            browser = webdriver.PhantomJS('/usr/local/bin/phantomjs')  # can be webdriver.PhantomJS()
            browser.get(__url)

            # wait for the select element to become visible
            browser.implicitly_wait(20)
            # EC.visibility_of_element_located((By.CSS_SELECTOR, "picture.thumbnail img"))
            elements = browser.find_element_by_xpath('//*[@id="hasSchedules-alpha-default"]/li/div[1]/div[1]/picture/img')
            for element in elements:
                print(element.get_attribute('src'))
            # )


            browser.quit()

            # print(parseHTML);
            #images = tree.xpath('//*[@id="hasSchedules-alpha-default"]/ul/li[6]/div[1]/div[1]/picture/img')

            # print("URL: %s Found: %d images" % (__url, len(images)))

        # return items
        # print(items)

    def buildQuery(self, query, options={}):
        key = ""
        __options = options or {key:""}

        __result = OrderedDict([
                                ('q', re.sub(str('\/\s/g'),'+',str(query))),
                                ('searchType', 'image'),
                                ('cx',self.cse_id),
                                ('key',self.api_key)
                                ])


        if len(__options['page']) > 0:
            __result['start'] = __options['page']

        if len(__options['size']) > 0:
            __result['imgSize'] = __options['size']

        if len(__options['type']) > 0:
            __result['imgType'] = __options['type']

        if len(__options['dominantColor']) > 0:
            __result['imgDominantColor'] = __options['dominantColor']

        if len(__options['colorType']) > 0:
            __result['imgColorType'] = __options['colorType']

        if len(__options['safe']) > 0:
            __result['safe'] = __options['safe']

        # print(urlencode(__result))
        return str(urlencode(__result))
