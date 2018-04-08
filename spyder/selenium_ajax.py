'''这是一个预约化学仪器的爬虫，因为网页有ajax，所以需要无头浏览器来模拟执行js，之后才能爬取想要的内容。
但是现在账号可能被学院封了...想不通，估计是找了一个不错的前端'''



import time
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



def write_data(data, path):
    with open(path, 'wb') as f:
            f.write(data)

def f_csv(data,path):
    with open(path, 'w', errors='ignore', newline='') as f:
        writer = csv.writer(f)
        for n in data:
             writer.writerow(n)

def get_data(html):
    apply_info=[]
    tr=html.find('div',{'class':'fc-row fc-widget-header'}).findAll('a')
    for item in tr:
         temp=[]
         temp.append(item.get_text())
         apply_info.append(temp)
    return apply_info


head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Referer':'http://121.192.177.40/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
     }
#driver=webdriver.PhantomJS(executable_path='D:\\phantomjs-2.1.1-windows\\bin\\phantomjs')
driver=webdriver.Chrome()
driver.get('http://121.192.177.40/')
time.sleep(1)
driver.find_element_by_name('username').send_keys('20620161151557')
driver.find_element_by_name('passwd').send_keys('037019')
driver.find_element_by_xpath("//button[@style='padding-left:2px;']").click()
cookie=driver.get_cookies()                                                 #保存cookie
time.sleep(1)
driver.get('http://121.192.177.40/index.php?r=userpanel/index')
driver.switch_to.frame('iframe')                                    #frame标签有frameset、frame、iframe三种，frameset跟其他普通标签没有区别，不会影响到正常的定位，而frame与iframe对selenium定位而言是一样的，selenium有一组方法对frame进行操作
driver.switch_to.frame('top')
userpanel_pageSource = driver.page_source
userpanel_bsObj=BeautifulSoup(userpanel_pageSource,'html.parser')
framemain_link=userpanel_bsObj.body.findAll('a',{'target':'left'})[0].attrs['href']
framemain_link='http://121.192.177.40/'+framemain_link
driver.get(framemain_link)
#driver.switch_to.frame('iframe')
#driver.switch_to.frame('left')
framemain_pageSource= driver.page_source
framemain_pageSource=BeautifulSoup(framemain_pageSource,'html.parser')
individual_link=framemain_pageSource.findAll('a',{'target':'main'})[4].attrs['href']
individual_link='http://121.192.177.40/'+individual_link
driver.get(individual_link)                                                         #进入预约仪器列表
time.sleep(1)
individual_pageSource=driver.page_source
subscribe_page=BeautifulSoup(individual_pageSource,'html.parser')
#subscribe_link=subscribe_page.find('a',{'id':'65609'}).attrs['href']
time.sleep(1)
driver.find_element_by_id('65609').click()
time.sleep(1)
#driver.find_element_by_xpath("//a[@href='index.php?r=order/require/insid/65609']").click()
#instruments_list=driver.page_source
#instruments_list=BeautifulSoup(instruments_list,'html.parser')
#terminal_link='http://121.192.177.40/'+instruments_list.findAll('a')[-1].attrs['href']
#driver.get(terminal_link)
driver.find_element_by_xpath("//img[@src='images/id_01.gif']").click()
time.sleep(1)
cookie2=driver.get_cookies()
dict_cookie1=cookie2[0]
dict_cookie2=cookie2[1]
cookie_map={}
cookie_map[dict_cookie1['name']]=dict_cookie1['value']
cookie_map[dict_cookie2['name']]=dict_cookie2['value']
#print (cookie_list)
cookies = requests.utils.cookiejar_from_dict(cookie_map, cookiejar=None, overwrite=True)
Terminal_page=driver.page_source
Terminal_page=BeautifulSoup(Terminal_page,'html.parser')
#print(Terminal_page.find('input',{'name':'starttime'}),Terminal_page.find('input',{'name':'endtime'}))
excel_List=get_data(Terminal_page)
subscribe_info=Terminal_page.findAll('div',{'class':'fc-content-col'})
i=0
Conbine_info=[]
for info in subscribe_info:
    temp=excel_List[i]
    a_tag=info.findAll('a')
    for a in a_tag:
        temp.append(a.get_text())
    Conbine_info.append(temp)
    i+=1
f_csv(excel_List,'C:\\Users\\ASUS\\Desktop\\python study\\new_yqyy.csv')
'''
js = "document.getElementsByName('id')[0].style.display='block'" #编写JS语句
driver.execute_script(js)
js = "document.getElementById('starttime').style.display='block'" #编写JS语句
driver.execute_script(js)
js = "document.getElementById('endtime').style.display='block'" #编写JS语句
driver.execute_script(js)
'''
driver.find_element_by_xpath("//th[@data-date='2018-03-10']").find_element_by_tag_name('a').click()
dragger=driver.find_element_by_xpath("//tr[@data-time='22:30:00']")
release_button=driver.find_element_by_xpath("//tr[@data-time='22:30:00']")
action=ActionChains(driver)
action.click_and_hold(dragger).move_to_element(release_button).release().perform()
time.sleep(1)
button=driver.find_element_by_xpath("//span[@class='ui-button-text']")
action.click(button).perform()
driver.find_element_by_name('Remark').send_keys('')
driver.find_element_by_name('SampleName').send_keys('MOR')
driver.find_element_by_name('SampleCount').send_keys('1')
time.sleep(1)
driver.find_element_by_id("submit_button").click()
'''
以下是直接用requests爬取的，简单暴力
#checkpage = driver.page_source
#checkpage=BeautifulSoup(checkpage,'html.parser')
#write_data(Terminal_page.encode('utf-8'), 'C:\\Users\\ASUS\\Desktop\\python study\\checkpage.txt')
#driver.get('http://121.192.177.40/index.php?r=order/edit')

#driver.find_element_by_xpath("//button[@class='pui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']").click()

#driver.find_element_by_xpath("//button[@class='pui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']").click()


test_time={'id':'65609',
           'starttime': '',
           'endtime':''
          }
#输入时间如下格式：2018-1-19 10:50:00
test_time['starttime']=str(input("起始时间：年"))+'-'+str(input('月：'))+'-'+str(input('日：'))+' '+str(input('时：'))+':'+str(input('分：'))+':'+str(input('秒：'))
test_time['endtime']=str(input("结束时间：年"))+'-'+str(input('月：'))+'-'+str(input('日：'))+' '+str(input('时：'))+':'+str(input('分：'))+':'+str(input('秒：'))
check_info={'starttime':'',
            'endtime':'',
            'insid':'65609'
}
check_info['starttime']=test_time['starttime']
check_info['endtime']=test_time['endtime']
check_req=requests.post('http://121.192.177.40/index.php?r=order/CheckTbillingProfile',headers=head,data=check_info,cookies=cookies)
html=requests.post('http://121.192.177.40/index.php?r=order/edit',headers=head,data=test_time,cookies=cookies)
html_Obsj=BeautifulSoup(html.content,'html.parser')



sampleinfo={'instrumentId':'65609',
            'bookId':'',
            'userId':'',
            'BookingModeID':'',
            'Title':'1042759669',
            'starttime':'',
            'endtime':'',
            'Remark':'',                                     #默认为空
            'SampleDeliveryMan':'',                          #用户名
            'SampleDeliveryTime':'',                         #提交时间
            'SampleName':'',
            'SampleCount':'',
            'SampleTypeID':'',                               #默认为空
            'SampleFormID':'',                               #默认为空
            'SampleSourceID':'',                             #默认为空
            'PreProcess':'0',
            'SampleDescription':'',                          #默认为空
            'customFormCount':'0'
}
sampleinfo['bookId']=html_Obsj.find('input',{'name':'bookId'}).attrs['value']
sampleinfo['userId']=html_Obsj.find('input',{'name':'userId'}).attrs['value']
sampleinfo['BookingModeID']=html_Obsj.find('input',{'name':'BookingModeID'}).attrs['value']
sampleinfo['Title']=html_Obsj.find('select',{'name':'Title'}).find('option').attrs['value']
sampleinfo['starttime']=html_Obsj.find('input',{'name':'starttime'}).attrs['value']
sampleinfo['endtime']=html_Obsj.find('input',{'name':'endtime'}).attrs['value']
sampleinfo['SampleDeliveryMan']=html_Obsj.find('input',{'name':'SampleDeliveryMan'}).attrs['value']
sampleinfo['SampleDeliveryTime']=html_Obsj.find('input',{'name':'SampleDeliveryTime'}).attrs['value']
sampleinfo['SampleName']=input("请输入待测样品名：")
sampleinfo['SampleCount']=input("请输入待测样品个数:")
print(sampleinfo)

head2={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Referer':'http://121.192.177.40/index.php?r=order/edit',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
     }
submit_subscribe=requests.post('http://121.192.177.40/index.php?r=order/add',headers=head2,data=sampleinfo,cookies=cookies)

'''






























'''
driver.find_element_by_name('starttime').send_keys('2018-1-19 10:30:00')
driver.find_element_by_name('endtime').send_keys('2018-1-19 10:50:00')
driver.get('http://121.192.177.40/index.php?r=order/edit')

driver.find_element_by_name('starttime').send_keys('2018-1-17 10:30:00')
driver.find_element_by_name('endtime').send_keys('2018-1-17 10:50:00')
driver.find_element_by_xpath("//button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']").click()
subscribe_apply_page=driver.page_source
subscribe_apply_page=BeautifulSoup(subscribe_apply_page,'html.parser')
print(subscribe_apply_page)


write_data(Terminal_page.encode('utf-8'), path)
excel_List=get_data(Terminal_page)
print(excel_List)
f_csv(excel_List,'C:\\Users\\ASUS\\Desktop\\python study\\new_yqyy.csv')






#redirect_link=\

print(instruments_list.findAll('a'))









driver.get('http://121.192.177.40/index.php?r=userpanel/index')
pageSource = driver.page_source
bsObj=BeautifulSoup(pageSource)
print(bsObj)
time.sleep(2)

#driver.find_element_by_css_selector('div.button-wrapper.command > button').click()

cookies=login_html.cookies
print(cookies)
index_html=session.get('http://121.192.177.40/index.php?r=userpanel/index',headers=head)
index_html_obj=BeautifulSoup(index_html.content,'html.parser')
body=index_html_obj.body
path='C:\\Users\\ASUS\\Desktop\\python study\\new_yqyy.txt'
write_data(body.encode('utf-8'), path)
self_manage=session.get('http://121.192.177.40/index.php?r=userpanel/leftuser',headers=head)
do_subscribe=session.get('http://121.192.177.40/index.php?r=user/userorder',headers=head)
XRD_xiangan=session.get('http://121.192.177.40/index.php?r=order/require/insid/65609',headers=head)

XRD_subscribe_page=session.get('http://121.192.177.40//index.php?r=Order/date/id/65609/type/2',headers=head)
print(XRD_subscribe_page.content.decode('utf-8'))
'''