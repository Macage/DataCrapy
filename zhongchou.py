#coding:utf-8

import requests
import urllib.parse
import json
import math
import time
import random

def post_url():
    posturl = "http://www.zhongchou.com/sso-getAuthenticateParams"
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
        ]
    header = {
        "host": "www.zhongchou.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.8",
        "content-length": "40",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    random_headers = random.choice(my_headers)
    header.update({'User-Agent':random_headers})
    data = {
        "username":"18205623438",
        "password":"lj19920402"
            }
    values = urllib.parse.urlencode(data)
    demo_session = requests.Session()
    response = demo_session.post(posturl, data=values, headers=header)
    print(response.status_code)

    geturl = "http://www.zhongchou.com/deal-march_list"
    f1 = open('id_list.txt', 'r+')
    id_list = [up.strip() for up in f1.readlines()]
    f1.close()
    for info in id_list:
        payload = {'id':int(info.split('\t')[0]), 'offset':0, 'page_size':10}
        content = demo_session.get(geturl, params=payload)
        print(content.status_code)
        time.sleep(random.randint(1, 5))
        filename = info.split('\t')[0] + '.txt'
        f2 = open(filename, 'w')
        json.dump(content.json(), f2)
        """if int(info.split('\t')[-1]) // 10 > 0:
            offset = math.ceil(int(info.split('\t')[-1]) / 10) * 10
            payload1 = {'id':int(info.split('\t')[0]), 'offset':0, 'page_size':10}
            content1 = demo_session.get(geturl, params=payload1)
            print(content1.status_code)
            time.sleep(2)
            json.dump(content1.json(), f2)"""

    #content = demo_session.get(geturl, params=payload)
    #f = open('354511.txt', 'w')
    #json.dump(content.json(), f)
post_url()
