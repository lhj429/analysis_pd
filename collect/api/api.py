from urllib.parse import urlencode
from .web_request import json_request
from datetime import datetime, timedelta
import math

SERVICE_KEY = 'kglFus9rQiSwGqFYcuHmr87yibNi7qlvrcMbHW1JBvzsbgfwovIZpBJsQ0tDK0osX9ySfBxiPrqY%2BrnoEoYvKQ%3D%3D'
TOURSPOT_VISITOR_END_POINT = 'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList'
FOREIGN_VISITOR_END_POINT = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'

def pd_gen_url(endpoint, **params):
    url = '%s?%s&serviceKey=%s' % (endpoint, urlencode(params), SERVICE_KEY)
    return url

def pd_fetch_tourspot_visitor(district1='', district2='', tourspot='', year=0, month=0):
    pageNo = 1
    hasnext = True

    while hasnext:
        url = pd_gen_url(TOURSPOT_VISITOR_END_POINT, service_key=SERVICE_KEY, YM='{0:04d}{1:02d}'.format(year, month), SIDO=district1, GUNGU=district2, _type='json', RES_NM=tourspot, numOfRows=10, pageNo=pageNo)
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

def pd_fetch_foreign_visitor(country_code, year, month):
    url = pd_gen_url(FOREIGN_VISITOR_END_POINT,
                     YM = '{0:04d}{1:02d}'.format(year, month),
                     NAT_CD = country_code,
                     ED_CD = 'E',
                     _type = 'json')

    json_result = json_request(url=url)
    json_header = json_result.get('response').get('header')
    result_message = json_header.get('resultMsg')
    if 'OK' != result_message:
        print('%s Error[%s] for request %s' % (datetime.now(), result_message, url))
        return None

    json_body = json_result.get('response').get('body')
    json_items = json_body.get('items')

    return json_items.get('item') if isinstance(json_items, dict) else None