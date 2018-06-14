import os
import json
from datetime import datetime, timedelta
from .api import api

RESULT_DIRECTORY = '__results__/crawling'
#data_dict = {}

#- api.py 의  pd_fetch_tourspot_visitor  함수를 활용한다.
#시도 지역과 기간(시작 년 ~ 끝 년)으로 데이터를 수집하도록 crawlling 함수를  작성하도록 한다.(10점)

#count_locals=56789 (csNatCnt)
#count_forigner=38179 (csForCnt)
#tourist_spot=창덕궁 (resNm)
#date=201701 (ym)
#restrict1=서울특별시 (sido)
#restrict2=종로구 (gungu)

def preprocess_post(datum):
    rm = ['gungu', 'sido', 'addrCd', 'ym', 'rnum', 'resNm', 'csForCnt', 'csNatCnt']
    if 'csNatCnt' not in datum:
        datum['count_locals'] = 0
    else:
        datum['count_locals'] = datum['csNatCnt']

    if 'csForCnt' not in datum:
        datum['count_forigner'] = 0
    else:
        datum['count_forigner'] = datum['csForCnt']

    if 'resNm' not in datum:
        datum['tourist_spot'] = 0
    else:
        datum['tourist_spot'] = datum['resNm']

    if 'ym' not in datum:
        datum['date'] = 0
    else:
        datum['date'] = datum['ym']

    if 'sido' not in datum:
        datum['restrict1'] = 0
    else:
        datum['restrict1'] = datum['sido']

    if 'gungu' not in datum:
        datum['restrict2'] = 0
    else:
        datum['restrict2'] = datum['gungu']
    for delete in rm:
        del datum[delete]



# def pd_fetch_tourspot_visitor(district1='', district2='', tourspot='', year=0, month=0):

def crawlling_tourspot_visitor(district, start_year, end_year):
    results = []
    #                   서울특별시_tourinstspot_2017_2017.json
    filename = '%s/%s_touristspot_%s_%s.json' % (RESULT_DIRECTORY, district, start_year, end_year)

    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            for data in api.pd_fetch_tourspot_visitor(district1=district, district2='', tourspot='', year=year, month=month):
                for datum in data:
                    preprocess_post(datum)

        results += data

    with open(filename, 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

if os.path.exists(RESULT_DIRECTORY) is False:
    os.makedirs(RESULT_DIRECTORY)