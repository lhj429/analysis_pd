from urllib.parse import urlencode
from .web_request import json_request

SERVICE_KEY = 'kglFus9rQiSwGqFYcuHmr87yibNi7qlvrcMbHW1JBvzsbgfwovIZpBJsQ0tDK0osX9ySfBxiPrqY%2BrnoEoYvKQ%3D%3D'
END_POINT = 'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList'

def pd_gen_url(endpoint, service_key=SERVICE_KEY, **params):
    url = '%s?serviceKey=%s&%s' % (endpoint, service_key, urlencode(params))
    return url

def pd_fetch_tourspot_visitor(district1='', district2='', tourspot='', year=0, month=0):
    url = pd_gen_url(END_POINT,
                     service_key=SERVICE_KEY,
                     YM = '{0:04d}{1:02d}'.format(year, month),
                     SIDO = district1,
                     GUNGU = district2,
                     _type='json',
                     RES_NM=tourspot)

    isnext = True
    while isnext is True:
        json_result = json_request(url=url)

        response = None if json_result is None else json_result.get('response')

        url = None if response is None else response.get('next')
        isnext = url is not None

        yield response
