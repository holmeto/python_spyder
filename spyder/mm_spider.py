# -*- coding: utf-8 -*-
"""
这是一个实现多线程爬取妹子图的爬虫，有些是参考网上的教程
"""
from bs4 import BeautifulSoup
import requests
import os
import threading
import queue
import time
import random



class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        self.head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                    }
        self.save_dir='F:\\mzt_threading\\'
    def run(self):
        print ("开启线程：" + self.name)
        self.process_scrapy(self.name, self.q)
        print ("退出线程：" + self.name)

    def process_scrapy(self,threadName,q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                url = q.get()
                self.save_img(url)
                queueLock.release()
            else:
                queueLock.release()

    def save_img(self, src):
        src_text= src[47:58].replace('/', '')
        save_path = self.save_dir + src_text + '.jpg'
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        res = requests.get(src, headers=self.head)
        with open(save_path, 'wb') as f:
            f.write(res.content)

class MM_Spider():
    def __init__(self):
        self.head={
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate, sdch',
                   'Accept-Language':'zh-CN,zh;q=0.8',
                   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                  }
        self.UrlList = []
        self.url = 'http://www.meizitu.com/a/more_%d.html'
    def get_url(self,num):
        for i in range(1,num):
           url=self.url%i
           html = requests.get(url, headers=self.head)
           html = BeautifulSoup(html.content, 'html.parser')
           img_url = html.findAll('img')
           for img in img_url:
               self.UrlList.append(img.attrs['src'])
        return self.UrlList
start_time=time.time()
exitFlag=0
Mzt=MM_Spider()
Url_List=Mzt.get_url(20)
threadList = ["Thread-1", "Thread-2", "Thread-3"]
queueLock = threading.Lock()
workQueue = queue.Queue()
threads = []

# 创建新线程
for tName in threadList:
    thread = myThread(tName, workQueue)
    thread.start()
    threads.append(thread)


# 填充队列
'''
l_url=len(Url_List)
i=0
while(i<l_url):
    queueLock.acquire()
    Rand_int=random.randint(30,40)
    if (i+Rand_int)<l_url:
        for j in range(i,i+Rand_int):
           workQueue.put(Url_List[j])
    else:
        for j in range(i,l_url):
           workQueue.put(Url_List[j])
    i+=Rand_int
    queueLock.release()

'''
with queueLock:
   for url in Url_List:
       workQueue.put(url)




# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")
end_time=time.time()
print("本次开车耗费时长：%s"%(end_time-start_time))


'''

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bs4 import BeautifulSoup
import requests
import os
class MM_Spider():
    def __init__(self):
        self.head={
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate, sdch',
                   'Accept-Language':'zh-CN,zh;q=0.8',
                   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                  }
        self.save_dir = 'F:\\mzt\\'
        self.url = 'http://www.meizitu.com/a/more_%d.html'
    def get_url(self,num):
        for i in range(1,num):
           url=self.url%i
           self.catch_img_html(url)
    def catch_img_html(self,url):
           html=requests.get(url,headers=self.head)
           html=BeautifulSoup(html.content,'html.parser')
           img_url=html.findAll('img')
           for img in img_url:
               self.save_img(img.attrs['src'],img.attrs['src'][47:58].replace('/',''))

    def save_img(self,src,src_text):
        save_path = self.save_dir+src_text+'.jpg'
        if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
        res = requests.get(src, headers=self.head)
        with open(save_path, 'wb') as f:
            f.write(res.content)

start_time=time.time()
Mzt=MM_Spider()
Mzt.get_url(20)
end_time=time.time()
print("本次开车耗费时长：%s"%(end_time-start_time))'''























