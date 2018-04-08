# -*- coding: utf-8 -*-
"""
这是一个老系统的仪器预约爬虫，最近化学网站换的飞起，有钱任性啊。好不容易写了一个脚本，又给挂了

"""
import csv
import requests
from bs4 import BeautifulSoup
import re



def write_data(data, path):
    with open(path, 'wb') as f:
            f.write(data)
def get_data(html):
    apply_info=[]
    tr=html.findAll('table',{'class':'STYLE1'})[1].findAll('tr')
    for item in tr:
         temp=[]
         element=item.findAll('td')
         for td in element:
                temp.append(td.get_text())
         apply_info.append(temp)
    return apply_info
def f_csv(data,path):
    with open(path, 'w', errors='ignore', newline='') as f:
        writer = csv.writer(f)
        for n in data:
             writer.writerow(n)
def Apply_Xrd(samplename,samplequantity):
    sample_info = {'name23':'胡涛'.encode('gb2312'),
                   'Submit':'追加提交'.encode('gb2312'),
                   'scan':'normal',
                   'yjfs':'自测'.encode('gb2312'),
                   'csmd':'物相分析'.encode('gb2312'),
                   'yplx':'固体粉末'.encode('gb2312'),
                   'ypmc': '',
                   'num': '',
                   'start': '',
                   'end': '',
                   'smsd':'',
                   'xq': '',
                   'xs': '',
                   'fz': '',
                   'endxs': '',
                   'endfz': '',
                   'tstj': '无'.encode('gb2312')

                   }
    sample_info['ypmc'] = samplename
    sample_info['num'] = samplequantity
    sample_info['start'] = input('起始角度：')
    sample_info['end'] = input('结束角度：')
    sample_info['smsd'] = input('扫描速度：')
    sample_info['xq'] = input('周几：').encode('gb2312')
    sample_info['xs'] = input('起始时间（小时）：')
    sample_info['fz'] = input('起始时间（分钟）：')
    sample_info['endxs'] = input('结束时间（小时）：')
    sample_info['endfz'] = input('结束时间（分钟）：')
    url='http://cia.xmu.edu.cn/booking/public_instruments/x-ray/xarigaku_xrd/xabzzj_sendlx.asp'
    applyAction=session.post(url,headers=head,data=sample_info)

session=requests.session()
head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
     }
system_instrument=session.get('http://cia.xmu.edu.cn/booking/',headers=head)
system_obj=BeautifulSoup(system_instrument.content,'html.parser')
system_url=system_obj.findAll('a',href=re.compile('.*/Login\.asp'))[0]
XRD_loginUrl='http://cia.xmu.edu.cn/booking/'+system_url.attrs['href']
Login_info=session.get(XRD_loginUrl,headers=head)
check_asp=BeautifulSoup(Login_info.content,'html.parser').find('form',{'method':'post'}).attrs['action']
Check_url='http://cia.xmu.edu.cn/booking/public_instruments/'+check_asp
info={'username':'胡涛'.encode('gb2312'),
      'password':'037019',
      'Submit':'提交'.encode('gb2312')
}
'''info['username']=str(input('name:')).encode('gb2312')
info['password']=str(input('password:'))'''
Login=session.post(Check_url,data=info,headers=head)
info_loginXRD={
    'name':'B1',
    'value':'Rigaku Ultima IV X射线衍射仪(翔安)'.encode('gb2312')
}
Login=BeautifulSoup(Login.content,'html.parser')
XRD_chooseUrl=Login.findAll('form')[4].attrs['action']
rigaku_XrdUrl='http://cia.xmu.edu.cn/booking/public_instruments/'+XRD_chooseUrl
subscribe=session.post(rigaku_XrdUrl,headers=head,data=info_loginXRD)
subscribe=BeautifulSoup(subscribe.content,'html.parser').findAll('form')[1]
benzhouzhuijia_info={
    'name':'B1',
    'value':'本周追加'.encode('gb2312')
    }
benzhouzhuijia_url='http://cia.xmu.edu.cn/booking/public_instruments/x-ray/xarigaku_xrd/'+subscribe.attrs['action']
apply=session.post(benzhouzhuijia_url,headers=head,data=benzhouzhuijia_info)
apply_info=get_data(BeautifulSoup(apply.content,'html.parser'))
path='C:\\Users\\ASUS\\Desktop\\python study\\yqyy.csv'
f_csv(apply_info,path)
add_applyUrl=BeautifulSoup(apply.content,'html.parser').find('form').attrs['action']
add_applyUrl='http://cia.xmu.edu.cn/booking/public_instruments/x-ray/xarigaku_xrd/'+add_applyUrl
add_applyInfo={
    'name':'B1',
    'value':'追加申请'.encode('gb2312')
}
add_apply=session.post(add_applyUrl,headers=head,data=add_applyInfo)
print(add_apply.content.decode('gb2312'))
#Apply_Xrd('mor',1)




