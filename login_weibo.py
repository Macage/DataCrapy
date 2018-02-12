#coding:utf-8

import sys
import urllib
import urllib
import urllib.request
import urllib.parse
import http.cookiejar
import base64
import re
import json
import rsa
import binascii
import requests


# import requests
# from bs4 import BeautifulSoup

# 新浪微博的模拟登陆
class weiboLogin:
    def enableCookies(self):
        # 获取一个保存cookies的对象
        cj = http.cookiejar.CookieJar()
        #cj = cookielib.CookieJar()
        # 将一个保存cookies对象和一个HTTP的cookie的处理器绑定
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        #cookie_support = urllib2.HTTPCookieProcessor(cj)
        # 创建一个opener,设置一个handler用于处理http的url打开
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        #opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        # 安装opener，此后调用urlopen()时会使用安装过的opener对象
        urllib.request.install_opener(opener)
        #urllib2.install_opener(opener)

    # 预登陆获得 servertime, nonce, pubkey, rsakv
    def getServerData(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=ZW5nbGFuZHNldSU0MDE2My5jb20%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1442991685270'
        data = urllib.request.urlopen(url).read()
        p = re.compile('(.*)')
        json_data = str(data).split('(')[-1].split(')')[0].strip()
        json_data = json.loads(json_data)
        servertime = json_data['servertime']
        nonce = json_data['nonce']
        pubkey = json_data['pubkey']
        rsakv = json_data['rsakv']
        return servertime, nonce, pubkey, rsakv
        """try:
            print("------")
            json_data = p.search(data).group(1)
            print(json_data)
            data = json.loads(json_data)
            print(data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print('Get severtime error!')
            return None"""

    # 获取加密的密码
    def getPassword(self, password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
        passwd = rsa.encrypt(message.encode(), key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    # 获取加密的用户名
    def getUsername(self, username):
        username_ = urllib.parse.quote(username)
        username = base64.encodestring(username_.encode())[:-1]
        return username

    # 获取需要提交的表单数据
    def getFormData(self, userName, password, servertime, nonce, pubkey, rsakv):
        userName = self.getUsername(userName)
        psw = self.getPassword(password, servertime, nonce, pubkey)

        form_data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': 'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',
            'vsnf': '1',
            'su': userName,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': psw,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        formData = urllib.parse.urlencode(form_data)
        return formData

    # 登陆函数
    def login(self, username, psw):
        self.enableCookies()
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        #url = "https://login.sina.com.cn/signup/signin.php?entry=sso"
        servertime, nonce, pubkey, rsakv = self.getServerData()
        formData = self.getFormData(username, psw, servertime, nonce, pubkey, rsakv)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'}
        #req = urllib.request.Request(url=url, data=formData, headers=headers)        print(req)
        #result = urllib.request.urlopen(req)
        demo_session = requests.session()
        res = demo_session.post(url=url, data=formData, headers=headers)
        #text = result.read()
        print(res.status_code)
        #print(res.text)
        text = res.text
        login_url = re.findall(r'location.replace(.*?);', str(text))[0].split('"')[1]
        print(login_url)
        con = demo_session.post(url=login_url, data=formData, headers=headers)
        print(con.status_code)
        #print(con.text)
        print("Login success!")
        # 还没完！！！这边有一个重定位网址，包含在脚本中，获取到之后才能真正地登陆
        """p = re.compile('location\.replace[\'"](.*?)[\'"]')
        try:
            login_url = p.search(text).group(1)
            print(login_url)
            # 由于之前的绑定，cookies信息会直接写入
            urllib.request.urlopen(login_url)
            print("Login success!")
        except:
            print('Login error!')
            return 0"""

        # 访问主页，把主页写入到文件中
        #url = 'http://weibo.com/u/2679342531/home?topnav=1&wvr=6'
        home_url = "http://weibo.com/u/3570327503/home?wvr=5"
        content = demo_session.get(home_url)
        print(content.status_code)
        print(demo_session.cookies)
        print(content.text)
        #request = urllib.request.Request(url)
        #response = urllib.request.urlopen(request)
        #text = response.read()
        #fp_raw = open("weibo.txt", "w", encoding='utf-8')
        #fp_raw.write(content.text)
        #fp_raw.close()
        print("End!")


wblogin = weiboLogin()
print('新浪微博模拟登陆:')
#username = input(u'用户名：')
#password = input(u'密码：')
wblogin.login('1779726827@qq.com', 'lj20120518')