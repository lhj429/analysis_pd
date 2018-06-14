import analysis_pd.collect.api.api as pdapi
# test for pd_gen_url
'''
url = pdapi.pd_gen_url(
    'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList',
    YM='{0:04d}{1:02d}'.format(2017, 1),
    SIDO='서울특별시',
    GUNGU='',
    RES_NM='',
    numOfRows=10,
    _type='json',
    pageNo=1)

print(url)
'''

for items in pdapi.pd_fetch_tourspot_visitor(district1='서울특별시', year=2012, month=7):
    print(items)

