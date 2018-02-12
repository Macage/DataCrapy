#coding:utf-8
from bs4 import BeautifulSoup
import json
import sys
import imp
imp.reload(sys)
sys.getdefaultencoding()


f = open('json.txt', 'r+', encoding='utf-8')
content = json.load(f)
print(content)
print(content['htmlTitle'])
print(content['htmlContent'])
