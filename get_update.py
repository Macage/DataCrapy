#coding:utf-8
import math
import urllib
import urllib.request
import os
from threading import Thread
from multiprocessing import Process
from bs4 import BeautifulSoup
import time


def downloadURL(urls, dirpath):
    for url in urls:
        if len(url) > 0:
            content = urllib.request.urlopen(url).read()
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            filename = url.split('&')[0].split('id=')[-1] + '_' + url.split('offset=')[-1].split('&')[0] + '.txt'
            open(dirpath + '/' + filename, 'w').write(str(content))
            time.sleep(5)

def thread_process_job(n, Thread_or_Process, url_list, job):
    """
    n: 多线程或多进程数
    Thread_Process: Thread／Process类 
    job: countdown任务
    """
    local_time = time.time()
    threads_or_processes = [Thread_or_Process(target=job, args=(url_list[i], str(n) + Thread_or_Process.__name__)) for i
                            in range(n)]
    for t in threads_or_processes:
        t.start()
    for t in threads_or_processes:
        t.join()

    print(n, Thread_or_Process.__name__, " run job need ", time.time() - local_time)

if __name__ == "__main__":
    f = open('id_list.txt', 'r+')
    id_list = [_id.strip() for _id in f.readlines()]
    urls = []
    for id in id_list:
        if int(id.split('\t')[-1]) // 10 == 0:
            url = "http://www.zhongchou.com/deal-march_list?id=%s&offset=0&page_size=10" % id.split('\t')[0]
            urls.append(url)
        else:
            url1 = "http://www.zhongchou.com/deal-march_list?id=%s&offset=0&page_size=10" % id.split('\t')[0]
            url2 = "http://www.zhongchou.com/deal-march_list?id=%s&offset=%d&page_size=10" % (id.split('\t')[0], math.ceil(int(id.split('\t')[-1]) / 10) * 10)
            urls.append(url1)
            urls.append(url2)

    print(len(urls))

    for n in [8]:
        url_list = []
        url_len = len(urls)
        url_split_len = url_len // n
        for i in range(n):
            if i == n - 1:
                url_list.append(urls[i * url_split_len:url_len])
            else:
                url_list.append(urls[i * url_split_len:(i + 1) * url_split_len])
        thread_process_job(n, Thread, url_list, downloadURL)