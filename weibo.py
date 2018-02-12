#coding:utf-8

import requests
import time
import urllib
import json
import urllib.request
import urllib.parse

"""url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=1491206789617"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
header = {'User-agent':UA,
        "Referer":"http://weibo.com/"
        }
demo_session = requests.Session()
post_data = {
            "entry":"weibo",
            "gateway":1,
            "from":"",
            "savestate":7,
            "useticket":1,
            "pagerefer":"http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F",
            "vsnf":1,
            "su":"MTc3OTcyNjgyNyU0MHFxLmNvbQ==",
            "service":"miniblog",
            "servertime":"1491206806",
            "nonce":"BNDH6A",
            "pwencode":"rsa2",
            "rsakv":"1330428213",
            "sp":"ba518a7f9a945d1e83a117a64e1a0f51bdfdb434b103a22d6ad8c1b036ea45129827013e868a65d753bb955cfe4c1f5bdcd911ef5503569b0c8aede367fa53693c7bf79b6de9fb69e2818de19e804d2baa987c5614704683de2d2cc786c117316866c502e582cfaa0751e4340104df3db413a0990a1b2c77b77f488f663ea9f7",
            "sr":1280*720,
            "encoding":"UTF-8",
            "cdult":2,
            "domain":"weibo.com",
            "prelt":47,
            "returntype":"TEXT"
            }
response = demo_session.post(url, data=post_data, headers=header)
print(response.status_code)
#print(response.text)
#print(response.headers)

post_url = "http://weibo.com/aj/onoff/setstatus?ajwvr=6"
data = {
        "sid":0,
        "state":0
        }
resp = demo_session.post(post_url, data=data, headers=header)

url1 = "http://weibo.com/p/1008084f910f866128c5be26260d6914c6ecb8?current_page=0&since_id=2399999909&page=1#1490943336900"
content = demo_session.get(url1)
print(content.content)"""
f1 = open('url1.txt', 'w')
f2 = open('url2.txt', 'w')
first_url = "http://weibo.com/p/1008084f910f866128c5be26260d6914c6ecb8?current_page=0&since_id=2399999909&page=1"
first_json_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100808&current_page=1&since_id=2399999984&page=1&pagebar=0&tab=home&pl_name=Pl_Third_App__11&id=1008084f910f866128c5be26260d6914c6ecb8&script_uri=/p/1008084f910f866128c5be26260d6914c6ecb8&feed_type=1&pre_page=1&domain_op=100808"
count = 1
current_page = 0
for page in range(1, 24):
    page_url = "http://weibo.com/p/1008084f910f866128c5be26260d6914c6ecb8?current_page=%d&since_id=2399999909&page=%d" %(current_page, page)
    count += 1
    current_page += 3
    if count % 3 == 0:
        page += 1
    f1.write(page_url)
    f1.write('\n')
f1.close()

page = 1
#count = 1
page_list = list(range(0, 69))[1::3]
page_list1 = list(range(0, 69))[2::3]
print(page_list)
print(page_list1)
p_list = page_list + page_list1
p_list.sort()
print(p_list)
for current in p_list:
    url2 = "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100808&current_page=%d&since_id=2399999984&page=%d&pagebar=0&tab=home&pl_name=Pl_Third_App__11&id=1008084f910f866128c5be26260d6914c6ecb8&script_uri=/p/1008084f910f866128c5be26260d6914c6ecb8&feed_type=1&pre_page=1&domain_op=100808" %(current, page)
    count += 1
    if count % 2 == 0:
        page += 1
    f2.write(url2)
    f2.write('\n')
f2.close()