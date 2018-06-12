import os
import json
from datetime import datetime, timedelta
from .api import api

#- api.py 의  pd_fetch_tourspot_visitor  함수를 활용한다.
#시도 지역과 기간(시작 년 ~ 끝 년)으로 데이터를 수집하도록 crawlling 함수를  작성하도록 한다.(10점)
#다음 포맷의 파일 이름으로 저장될 수 있도록 결과를 파일로 저장한다.(10점)
#                   서울특별시_tourinstspot_2017_2017.json

'''
"response":{
"header":{
"resultCode":"0000",
"resultMsg":"OK"
},
"body":{
"items":{
"item":[
{
"addrCd":1111,
"csForCnt":38179,
"csNatCnt":56789,
"gungu":"종로구",
"resNm":"창덕궁",
"rnum":1,
"sido":"서울특별시",
"ym":201701
},
'''

#count_locals=56789 (csNatCnt)
#count_forigner=38179 (csForCnt)
#tourist_spot=창덕궁 (resNm)
#date=201701 (ym)
#restrict1=서울특별시 (sido)
#restrict2=종로구 (gungu)

def preprocess_post(data):
    if 'csNatCnt' not in data:
        data['count_locals'] = 0
    else:
        data['count_locals'] = data['csNatCnt']

    if 'csForCnt' not in data:
        data['count_forigner'] = 0
    else:
        data['count_forigner'] = data['csForCnt']

    if 'resNm' not in data:
         data['tourist_spot'] = 0
    else:
        data['tourist_spot'] = data['resNm']

    if 'ym' not in data:
        data['date'] = 0
    else:
        data['date'] = data['ym']



def crawlling_tourspot_visitor(district, start_year, end_year):
    pass
