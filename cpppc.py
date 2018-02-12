#coding:utf-8

import requests
import urllib.parse
import time
def post_url():
    posturl = "http://www.cpppc.org:8082/efmisweb/ppp/projectLibrary/getPPPList.do?tokenid=null"
    heade = {
        "host": "www.cpppc.org:8082",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.8",
        "content-length": "77",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    data = {
        "distStr":"",
        "induStr":"",
        "investStr":"",
        "projName":"",
        "sortby":"",
        "orderby":"",
        "stageArr":""
            }
    for page in range(1, 94):
        print(page)
        data.update({'queryPage': page})
        #time.sleep(2)
        values = urllib.parse.urlencode(data)
        content = requests.post(posturl, data=values, headers=heade)
        print(content.status_code)
        proj_list = content.json()
        for