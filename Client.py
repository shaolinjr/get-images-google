import requests
import re
from collections import OrderedDict
from urllib.parse import urlencode

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

    def search(self, query, options):

        if not query :
            raise ValueError("Expected a query!")

        __url = "{0}/customsearch/v1?{1}".format(self.endpoint, self.buildQuery(query, options))
        items = requests.get(__url).json()['items'] or []

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
        return items
        # print(items)

    def buildQuery(self, query, options):
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
