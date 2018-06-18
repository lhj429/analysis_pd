import os
import json
from datetime import datetime, timedelta
from .api import api

RESULT_DIRECTORY = '__results__/crawling'

def preprocess_tourspot_visitor(datum):
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
        if delete in datum:
            del datum[delete]

def preprocess_foreign_visitor(data):
    rm = ['ed', 'edCd', 'rnum', 'natCd', 'natKorNm', 'num', 'ym']

    data['country_code'] = data['natCd']
    data['country_name'] = data['natKorNm'].replace(' ', '')
    data['visit_count'] = data['num']
    data['date'] = data['ym']

    for delete in rm:
        if delete in data:
            del data[delete]

def crawlling_tourspot_visitor(district, start_year, end_year, fetch=True):
    results = []
    filename = '%s/%s_touristspot_%s_%s.json' % (RESULT_DIRECTORY, district, start_year, end_year)

    if fetch:
        for year in range(start_year, end_year+1):
            for month in range(1, 13):
                for data in api.pd_fetch_tourspot_visitor(district1=district, district2='', tourspot='', year=year, month=month):
                    for datum in data:
                        preprocess_tourspot_visitor(datum)

                    results += data

        with open(filename, 'w', encoding='utf-8') as outfile:
            json_string = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(json_string)

    return filename

def crawlling_foreign_visitor(country, start_year, end_year, fetch=True):
    results = []
    filename = '%s/%s(%s)_foreignvisitor_%s_%s.json' % (RESULT_DIRECTORY, country[0], country[1], start_year, end_year)

    if fetch:
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                data = api.pd_fetch_foreign_visitor(country[1], year, month)
                if data is None:
                    continue

                preprocess_foreign_visitor(data)
                results.append(data)

        with open(filename, 'w', encoding='utf-8') as outfile:
            json_string = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(json_string)

if not os.path.exists(RESULT_DIRECTORY):
    os.makedirs(RESULT_DIRECTORY)