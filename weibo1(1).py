#coding:utf-8

# 这种登陆方式是参考别的网友的，虽然效率很高，但我觉得普适性不强
import time
import base64
import rsa
import binascii
import requests
import re
import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote_plus

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"

def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


# 预登陆获得 servertime, nonce, pubkey, rsakv
def get_server_data(su):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    prelogin_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(prelogin_url, headers=headers)

    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

    return sever_data

# 这一段用户加密密码，需要参考加密文件
def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥,
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def login(username, password):
    # su 是加密后的用户名
    su = get_su(username)
    sever_data = get_server_data(su)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    password_secret = get_password(password, servertime, nonce, pubkey)

    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    login_page = session.post(login_url, data=postdata, headers=headers)
    login_loop = (login_page.content.decode("GBK"))
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    loop_url = re.findall(pa, login_loop)[0]
    login_index = session.get(loop_url, headers=headers)
    uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers)
    weibo_pa = r'<title>(.*?)</title>'
    userName = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    #print('登陆成功，你的用户名为：'+userName)
    return session

def get_info(url):
    from bs4 import BeautifulSoup
    from lxml import etree
    import sys
    import chardet
    session = login(username, password)
    response = session.get(url)
    print(response.status_code)
    '''
    #对于字典格式的文件
    content = response.json()
    #print(content['data'])
    
    data = content['data']
'''
    #对于html格式的文件
    content = response.text
    typeEncode = sys.getfilesystemencoding()
    infoencode = chardet.detect(content).get('encoding', 'utf-8')
    html = content.decode(infoencode, 'ignore').encode(typeEncode)
    print(len(html))
'''
    base_info = soup.find('div',{'id':'Pl_Third_App__11'})#所有评论
    print (base_info)

    item_info = base_info.find_all('div',{'class':'WB_cardwrap WB_feed_type S_bg2'})#每一个评论
    first_info = item_info.find_all('div',{'class':'WB_from S_txt2'})

    for href in first_info.find_all('a',{'target':'_blank'}):#每一个微博的链接
        url3=href.get('href').strip()#每个微博的网址 #.strip()把空格去了
        id0=url3.split('/')[-1]#切割，得到每个微博的ID
        html1=urllib.request.urlopen(url3).read()#获得每个微博页面的内容
        soup1 = BeautifulSoup(html, 'lxml')#解析每个微博
        weibo_info=soup1.find('div',{'class':'WB_detail'})#找到包含微博用户、发表时间等信息的模块；
        user_name=weibo_info.find('div',{' class':'WB_info'}).text.strip()#获取微博用户名，
        user_id= weibo_info.find('a',{'class':'W_f14 W_fb S_txt1'}).get('id')#用户id
        time_info=weibo_info.find('div',{'class':'WB_from S_txt2'})#找到发布时间和日期
        time=time_info.find('a').get('title')
        cont_info=weibo_info.find('div',{'class':'WB_text W_f14'})#获取微博内容
        cont=cont_info.text #获取内容（ ）
        number_info=weibo.find('div',{'class':'WB_row_line WB_row_r4 clearfix S_line2'})#评论等信息
        li_info=number_info.fin_all('li')
        transmit_num=li_info[1].find('em').text()[-1].strip()#转发数
        comment_num=li_info[2].find('em').text()[-1].strip()#评论数
        praise_num=li_info[3].find('em').text()[-1].strip()#点赞数
        comment_info=weibo_info.find('div',{'class':'list_ul'})#评论列表
        com_id=comment_info.get('div',{'comment_id'})#评论者ID
        com_info=comment_info.find('div',{'class':'list_con'})
        com_name= com_info.get('div',{'clss':'WB_text'}).text()[0].strip()  #评论者用户名
        com_content= com_info.get('div',{'class':'WB_text'}).text()[1].strip()#评论内容
        com_time= com_info.get('div',{'class':'WB_from S_txt2'}).text().strip()#评论时间
        web_info=user_id+'\t'+user_name+'\t'+time+'\t'+cont+'\t'+transmit_num+'\t'+comment_num+'\t'+praise_num+'\t'+com_id+'\t'+com_name+'\t'+com_content+'\t'+com_time

f4=open('weibo1.txt','w')
f4.write(web_info)
f4.write('\n')
f4.close()
'''


if __name__ == "__main__":
    username = '18817355707'
    password = 'wang1554514'
    login('18817355707', 'wang1554514')
    url = "http://weibo.com/p/10080833540d28f197ce43022f8a12e2bad4a5?current_page=0&page=1"
    get_info(url)
