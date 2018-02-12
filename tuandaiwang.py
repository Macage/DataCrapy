#coding:utf-8

import requests
import time
import urllib
import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def get_content():
    url = "https://www.tuandai.com/ajaxCross/Login.ashx?Cmd=NewUserLogin"
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    header = {'User-agent':UA,
              "Referer":"https://www.tuandai.com/user/login.aspx?ReturnUrl=https://www.tuandai.com/pages/invest/invest_list.aspx?keydj=e5b868d6e6&expiredj=1491047511"}
    demo_session = requests.Session()

    post_data = {"Cmd": "NewUserLogin",
                 "sUserName": "862a78401d905c5db906dccfc85447ab3384b9f42334fdca",
                 "sPassword": "6e54168f874a97c3e93873cb68fed9060a85cdec89b50d59",
                 "sVerCode": "",
                 "isRember": True
                 }

    response = demo_session.post(url, data=post_data, headers=header)
    print(response.status_code)
    #print(response.cookies['TDLastLoginDate'])
    #print(response.content)
    #cookies = demo_session.cookies
    #print(cookies)
    #header.update({'X-CSRFToken': "sba13ercxsrmzufceh1xt0jv"})
    #header.update({'content-type': "application/json"})
    posturl = "https://www.tuandai.com/pages/ajax/newinvest_list.ashx"
    heade = {
    "authority":"www.tuandai.com",
    "method":"POST",
    "path":"/pages/ajax/newinvest_list.ashx",
    "scheme":"https",
    "accept":"application/json, text/javascript, */*; q=0.01",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.8",
    "content-length":"152",
    "content-type":"application/x-www-form-urlencoded; charset=UTF-8"
    }
    #heade.update({"ASP.NET_SessionId": "sba13ercxsrmzufceh1xt0jv"})
    data = {"Cmd": "GetInvest_List",
            "RepaymentTypeId": 0,
            "pagesize": 5,
            "pageindex": 1,
            "type": 1,
            "status": 2,
            "beginDeadLine": 0,
            "endDeadLine": 0,
            "rate": 0,
            "beginRate": 0,
            "endRate": 0,
            "strkey": "",
            "orderby": 0
            }
    for page in range(1, 109):
        data.update({'pageindex':page})
        time.sleep(2)
    values = urllib.parse.urlencode(data)
    content = demo_session.post(posturl, data=values, headers=heade)
    print(content.status_code)
    print(content.text)
    #f = open('tuandai.txt','w')
    #f.write(content.text)
    #f.close()
    #content = content.json()
    #print(content['projectListHtml'])

    demo_session.get(url, header=header)
#get_content()

def get_url(filename):
    f = open(filename, 'r+')
    content = json.load(f)
    html = content['projectListHtml']
    soup = BeautifulSoup(html, 'lxml')
    f = open('url.txt', 'w')
    for inv_list in soup.findAll('dl',{'class':'inv-list'}):
        url = inv_list.find('dt',{'class':'l'}).a.get('href')
        title = inv_list.find('div',{'class':'inv-title'}).a.text
        tip = inv_list.find('div',{'class':'jing-tip-box'}).text
        inv_data = inv_list.find('div',{'class':'inv-data'})
        inv_data_info = inv_data.findAll('li')
        lendMoney = inv_data_info[0].text
        unit = inv_data_info[1].text
        surplus = inv_data.find('li',{'class':'surplus'}).text
        percent = inv_data.find('li',{'class':'percent'}).text
        ml1 = inv_data.find('li',{'class':'ml1'}).text
        progress = inv_list.find('dd',{'class':'l inv-progress'}).text
        f.write(url)
        print(url)
    f.close()
#get_url('tuandai.txt')

#url.txt
def get_html(filename):
    result = open(filename, 'r+').readlines()
    results = [ul.strip() for ul in result]
    for url in results:
        id0 = results.index(url)
        html = urllib.request.urlopen(url1).read()
        filena = '%d.txt' % id0
        fw = open(filena, 'w')
        fw.write(html)
        fw.close()

def get_info(filename):
    import re
    f = open(filename, 'r+', encoding='utf-8')
    content = f.read()
    user_info = re.findall(r'getBorrowUserInfo(.*?);', content)
    print(user_info)
    user_id = user_info[0].split("'")[1])

get_info('project_0.txt')





