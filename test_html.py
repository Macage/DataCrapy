#coding:utf-8

from bs4 import BeautifulSoup

def get_content(filename):
    f = open(filename, 'r+', encoding='utf-8')
    results = f.read()
    f.close()
    print(len(results))
    soup = BeautifulSoup(results, 'lxml')
    print(soup)
    print(len(soup))
    base_info = soup.find_all('link')
    print(base_info)

get_content('html0.txt')