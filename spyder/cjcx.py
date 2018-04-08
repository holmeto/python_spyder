# -*- coding: utf-8 -*-
"""
这是一个实现XMU教务成绩爬取的一个爬虫，没有模块化
"""
import csv
import requests
from bs4 import BeautifulSoup
import re
import getpass

def write_data(data, path):
    with open(path, 'wb') as f:
            f.write(data)

def get_data(html):
    score_graph=[]
    temp1=[]
    title=html.findAll('th')
    for text in title:
        temp1.append(text.get_text())
    score_graph.append(temp1)
    cell=html.findAll('tr')
    for item in cell[3:]:
         temp2=[]
         element=item.findAll('td')
         for td in element:
                temp2.append(td.get_text())
         score_graph.append(temp2)
    return score_graph

head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
     }
session=requests.session()
r=session.get('http://ids.xmu.edu.cn/authserver/login?service=http%3A%2F%2Fi.xmu.edu.cn%2F')
soup=BeautifulSoup(r.content,'lxml')                #获取登陆表单的一些默认信息
info={
'username':'',
'password':'',
'lt':'',
'dllt':'',
'execution':'',
'_eventId':'',
'rmShown':''
     }
info['username']=str(input("请输入学号："))
info['password']=str(getpass.getpass())


index=soup.find_all('input',{'type':'hidden'})
for i in range(5):
   info[index[i]['name']]=index[i]['value']
#print(info)                                       #将登陆表单的一些默认value写进字典
html=session.post('http://ids.xmu.edu.cn/authserver/login?service=http%3A%2F%2Fi.xmu.edu.cn%2F',headers=head1,data=info)    #登陆信息门户
#print(html.status_code)
res=html.content
bs=BeautifulSoup(res,'lxml')
body=bs.body                                                                                                                #获取body部分
message= body.find('div',{'id':'pf611'}).findAll('a',href=re.compile('^http://.*'))
'''for link in message:
        print(link.attrs['href'])'''
#print(message[1].attrs['href'])
response=session.post(message[1].attrs['href'],headers=head)
bs4=BeautifulSoup(response.content,'lxml')
bs4=bs4.body
login={'name':'userName',
       'value':''
       }
login['userName']=bs4.find('input').attrs['value']
#print(response.content.decode('utf-8'))

html2=session.post('http://yjsy.xmu.edu.cn/office/asp/loginTrans.aspx',data=login)
#print(html2.content.decode('gb2312'))
path='C:\\Users\\ASUS\\Desktop\\python study\\chengjichaxun'
write_data(html2.content, path)
Frame=BeautifulSoup(html2.content,'lxml')
link=(i for i in Frame.find('frameset',{'name':'topwin'}).findAll('frame'))
url=next(link).attrs['src']
final_url='http://yjsy.xmu.edu.cn/office/asp/'+url
final_data=session.get(final_url)
final_html=BeautifulSoup(final_data.content,'lxml')
href=final_html.body.findAll('a',{'target':"mainContent"})[19]['href']
#print(href)
score_url='http://yjsy.xmu.edu.cn/office/asp/'+href[6:]
score=session.get(score_url)
grade='C:\\Users\\ASUS\\Desktop\\python study\\chengjidan'
#print(score.content.decode('gb2312'))
action=session.post(score_url,data={'name':'kcbs','value':''})
graph=BeautifulSoup(action.content,'html.parser')
score_data=get_data(graph)
with open('C:\\Users\\ASUS\\Desktop\\python study\\grade.csv', 'w', errors='ignore', newline='') as f:
    writer = csv.writer(f)
    for n in score_data:
       writer.writerow(n)







