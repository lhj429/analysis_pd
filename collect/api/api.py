from urllib.parse import urlencode
from .web_request import json_request
import math

SERVICE_KEY = '%2FfZdR%2Bue1CSxLEnMkZXa9iDYontLTMTIteD5%2BzYCiMYpDKUZNUh2FHGDQ04zazSEmLl34FClDQk8a7flFCIQKA%3D%3D'
END_POINT = 'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList'

def pd_gen_url(endpoint, **params):
    url = '%s?%s&serviceKey=%s' % (endpoint, urlencode(params), SERVICE_KEY)
    return url

def pd_fetch_tourspot_visitor(district1='', district2='', tourspot='', year=0, month=0):
    pageNo = 1
    hasnext = True

    while hasnext:
        url = pd_gen_url(END_POINT, service_key=SERVICE_KEY, YM='{0:04d}{1:02d}'.format(year, month), SIDO=district1, GUNGU=district2, _type='json', RES_NM=tourspot, numOfRows=10, pageNo=pageNo)
        json_result = json_request(url=url)

        json_body = json_result.get('response').get('body')
        numOfRows = json_body.get('numOfRows')
        totalCount = json_body.get('totalCount')

        if totalCount == 0:
            break

        last_page = math.ceil(totalCount/numOfRows)

        if pageNo == last_page:
            hasnext = False
        else:
            pageNo += 1

        yield json_body.get('items').get('item')


    # json_result = json_request(url=url)
    # data = None if json_result is None else json_result.get('response').get('body').get('items').get('item')
    #
    # yield data