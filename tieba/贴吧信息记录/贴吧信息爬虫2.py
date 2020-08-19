#coding : UTF-8
'''
版本0.1336(beta)
cd 贴吧信息记录
linux系统后台运行 nohup python3 贴吧信息爬虫2.py
ps aux|grep firefox|grep -v grep
ps aux|grep  geckodriver|grep -v grep
ps aux|grep python|grep -v grep
ps -ef | grep firefox | grep -v grep | cut -c 9-15 | xargs kill -s 9
https://www.cnblogs.com/fatt/p/5050866.html
linux下杀死进程（kill）的N种方法
'''
import os
import csv
import random
import time
import json
import signal
import time
import threading
import zlib
#import logging  # 引入logging模块
#import lxml
#import hashlib
import socket
from socket import error as SocketError
from urllib import request as r
from datetime import datetime
from bs4 import BeautifulSoup
#from selenium import webdriver
# 导入firefox选项
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities#获取浏览器日志 
'''
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
 
caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get("your url")
logs = [json.loads(log['message'])['message']['params'] for log in driver.get_log('performance')]
#获取request请求信息
for log in logs:
    if 'request' in log:
        requestUrl = log['request']['url']
 
driver.quit()
使用selenium.webdriver.common.desired_capabilities获取浏览器日志 - miss_林 - 博客园
https://www.cnblogs.com/misslin/p/10234915.html
'''
#from selenium.webdriver.support.wait import WebDriverWait#显示等待:WebDriverWait() WebDriverWait(driver,timeout,poll_frequency=0.5,ignored_exceptions=None)
#from selenium.webdriver.common.by import By#从selenium.webdriver.common.by 导入By包进行元素定位
'''
By是selenium中内置的一个class，在这个class中有各种方法来定位元素

By所支持的定位器的分类：

CLASS_NAME = 'class name'
CSS_SELECTOR = 'css selector'
ID = 'id'
LINK_TEXT = 'link text'
NAME = 'name'
PARTIAL_LINK_TEXT = 'partial link text'
TAG_NAME = 'tag name'
XPATH = 'xpath'
主要应用于一个过滤器，而webdriver的方法是一个定位器。

例如：

 # 用户名输入框
 username_Input = (By.ID, 'username')
 # 密码输入框
 pwd_Input = (By.ID, 'password')
 # 登录按钮
 login_btn = (By.TAG_NAME, 'button')
 # 首页的“新建投放计划”按钮

————————————————
版权声明：本文为CSDN博主「白清羽」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/gufenchen/java/article/details/98056959
'''
#from selenium.webdriver.support import expected_conditions as EC#判断一个元素是否存在，如何判断alert弹窗出来了，如何判断动态的元素等等一系列的判断，在selenium的expected_conditions模块收集了一系列的场景判断方法，
'''
selenium之等待页面（或者特定元素）加载完成_Python_weixin_42081389的博客-CSDN博客
https://blog.csdn.net/weixin_42081389/article/details/98486562
from selenium.webdriver.support.ui import WebDriverWait
selenium.webdriver.support.ui 和selenium.webdriver.support.wait的区别
原创爬虫王者 最后发布于2019-04-25 08:47:03 阅读数 780  收藏
展开
网上搜了很久，没有找到合适答案。

我们知道，selenium.webdriver.support.ui 和selenium.webdriver.support.wait都是用来做显式等待的，但两者有什么区别呢？

进入selenium的官方文档https://seleniumhq.github.io/selenium/docs/api/py/api.html可以发现，里面并没有出现selenium.webdriver.support.ui，所以判断是ui换成了wait，这样更直接易懂。也就是说二者没有区别！

所以，我们用selenium.webdriver.support.wait就好啦！
————————————————
版权声明：本文为CSDN博主「爬虫王者」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_39498924/java/article/details/89499590
'''
#检测超时需要的模块
#PhantomJS   都能用
#Firefox  都能用
#import selenium.common.exceptions

socket.setdefaulttimeout(random.choice(range(60, 120)))# 这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
wenjianjia=''
tieba=None
timer=None
countx = 0
errorx=0
#browser=None
#weiwancheng=False

def req_maker(path):
    if path:
        req = r.Request(path)
        req.add_header(
            "User-Agent", "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.124 Safari/537.36")
        req.add_header(
            "Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
        req.add_header("Accept-Encoding", "gzip, deflate, br")
        req.add_header("Accept-Language", "zh-CN,zh;q=0.8,en;q=0.6")
        req.add_header("Cookie", cookie)
        return req
    else:
        return None

def req_maker2(path):
    if path:
        req = r.Request(path)
        req.add_header(
            "User-Agent", "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.124 Safari/537.36")
        req.add_header(
            "Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
        req.add_header("Accept-Encoding", "gzip, deflate")
        req.add_header("Accept-Language", "zh-CN,zh;q=0.8,en;q=0.6")
        req.add_header("Cookie", cookie)
        return req
    else:
        return None

def get_response_str(req):
    with r.urlopen(req,timeout=60) as f:
        time.sleep(2)
        decompressed_data =zlib.decompress(f.read(), 16 + zlib.MAX_WBITS)
    return str(decompressed_data, "utf-8", errors='replace')
        

def get_now_str():
    return int(float(time.time()) * 1000)

'''
Python下Selenium PhantomJs设置header的方法
2018年04月07日 11:58:00 weixin_33857679 阅读数 16
https://blog.csdn.net/weixin_33857679/article/details/92267975
'''
def getSource():
    '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Content-Encoding': 'gzip,deflate,br',
        #'Content-Type': 'text/html; charset=utf-8',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Cookie':''  
    }
    #使用copy()防止修改原代码定义dict
    cap = DesiredCapabilities.PHANTOMJS.copy() 
 
    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value
 
    # 不载入图片，爬页面速度会快很多
    cap["phantomjs.page.settings.loadImages"] = False
    service_args=[]
    service_args.append('--load-images=no')  ##关闭图片加载
    #service_args.append('--disk-cache=yes')  ##开启缓存
    service_args.append('--ignore-ssl-errors=true') ##忽略https错误
    '''
    '''
    版权声明：本文为CSDN博主「老司儿」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/ll641058431/java/article/details/79725136
    '''
    # 创建firefox浏览器驱动，无头模式（超爽）
    #firefox_options = Options()
    #firefox_options.set_headless()
    '''
    https://peter.sh/experiments/chromium-command-line-switches/

    chrome_options.add_argument('--user-agent=""')  # 设置请求头的User-Agent
    chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
    chrome_options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
    chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('--disable-javascript')  # 禁用javascript
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面

    chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('–disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--start-maximized')
    ————————————————
    版权声明：本文为CSDN博主「清风冷吟」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/weixin_43968923/java/article/details/87899762
    现象：运行selenium 做网页自动化时，刚开始速度正常，但运行一段时间后速度明显变慢，查看cpu占用情况，发现慢的原因是firefox的cpu占用达100%。估计是缓存问题。解决办法：

    一、定时重启页面：

    webdriver.refresh()                    测试有效

    也有介绍调用：webdriver.delete_all_cookies()            此方法测试无效

    二、通过修改fireprofile优化内存及cpu占用（有效）：

    profile = webdriver.FirefoxProfile()

    profile.set_preference("permissions.default.image", 2)  #禁止下载图片，根据情况使用

    # 禁用浏览器缓存

    profile.set_preference("network.http.use-cache", False)

    profile.set_preference("browser.cache.memory.enable", False)

    profile.set_preference("browser.cache.disk.enable", False)

    profile.set_preference("browser.sessionhistory.max_total_viewers", 3)

    profile.set_preference("network.dns.disableIPv6", True)

    profile.set_preference("Content.notify.interval", 750000)

    profile.set_preference("content.notify.backoffcount", 3)

    # 有的网站支持 有的不支持 2 35 profile.set_preference("network.http.pipelining", True)

    profile.set_preference("network.http.proxy.pipelining", True)

    profile.set_preference("network.http.pipelining.maxrequests", 32)

    三、最有效的办法是第一第二步同步进行，运行一段时间重启页面。
    ————————————————
    版权声明：本文为CSDN博主「wenzhp1975」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/wenzhp1975/java/article/details/102679081
    '''
    #firefox_profile = webdriver.FirefoxProfile()
    #firefox_profile.set_preference("permissions.default.image", 2)#禁止下载图片，根据情况使用
    # 禁用浏览器缓存
    #firefox_profile.set_preference("network.http.use-cache", False)
    #firefox_profile.set_preference("browser.cache.memory.enable", False)
    #firefox_profile.set_preference("browser.cache.disk.enable", False)
    #firefox_profile.set_preference("browser.sessionhistory.max_total_viewers", 3)
    #firefox_profile.set_preference("network.dns.disableIPv6", True)
    #firefox_profile.set_preference("Content.notify.interval", 750000)
    #firefox_profile.set_preference("content.notify.backoffcount", 3)
    #firefox_options.add_argument("--headless")
    #firefox_options.add_argument("--blink-settings=imagesEnabled=false")
    #firefox_options.add_argument('--start-maximized')
    #firefox_options.add_argument('--incognito') 
    #driver = webdriver.Firefox(options=firefox_options,firefox_profile=firefox_profile)#executable_path=r'geckodriver.exe路径'
    #driver = webdriver.PhantomJS(desired_capabilities=cap,service_args=service_args)#注意selenium的版本，高版本才支持chromedriver.exe.这里selenium==2.53.6
    #driver.set_page_load_timeout(60)  # 设置页面最长加载时间为5s
    #driver.set_script_timeout(60)     #这两种设置都进行才有效
    '''
    selenium 超时问题解决
    http://blog.leanote.com/post/boom/selenium-%E8%B6%85%E6%97%B6%E9%97%AE%E9%A2%98%E8%A7%A3%E5%86%B3
    '''
    #return driver

def get_data(name):
    global wenjianjia
    final = []
    str2=name.encode('utf-8')
    str2=str(str2).replace('\\x','%')
    str2=str2.split("'")[1]
    html_str1=None
    html_str2=None
    html_str3=None
    html_str1='https://tieba.baidu.com/f?kw='+str2#直接获取贴吧主页的网页必须把中文转utf-8在连进去
    html_str2='http://tieba.baidu.com/sign/info?kw='+str2+'&ie=utf-8'#贴吧信息api
    html_str3='https://tieba.baidu.com/f?kw='+str2+'&ie=utf-8&tab=good'#贴吧精品区网页
    try:
        html_tree11 = get_response_str(req_maker(html_str1))
        html_tree1=BeautifulSoup(str(html_tree11), 'html.parser')
        print(html_str1)
        html_tree22 = get_response_str(req_maker2(html_str2))
        html_tree2=BeautifulSoup(str(html_tree22), 'html.parser')
        print(html_str2)
        html_tree33 = get_response_str(req_maker(html_str3))
        html_tree3=BeautifulSoup(str(html_tree33), 'html.parser')
        print(html_str3)
        '''
        html_str1 = get_response_str(req_maker('https://tieba.baidu.com/f?kw='+str2))
        html_tree1=BeautifulSoup(html_str1, 'html.parser')
        '''
        #browser.get(html_str1)
        #time.sleep(2)#有时候会没加载完内容，所以弄个2秒延时 
        #element =WebDriverWait(browser,80,0.5).until(EC.presence_of_element_located((By.TAG_NAME,'body')),message="")
        # 此处注意，如果省略message=“”，则By.ID外面是两层()
        '''
        方法	说明
        title_is	判断当前页面的 title 是否完全等于（==）预期字符串，返回布尔值
        title_contains	判断当前页面的 title 是否包含预期字符串，返回布尔值
        presence_of_element_located	判断某个元素是否被加到了 dom 树里，并不代表该元素一定可见
        visibility_of_element_located	判断元素是否可见（可见代表元素非隐藏，并且元素宽和高都不等于 0）
        visibility_of	同上一方法，只是上一方法参数为locator，这个方法参数是 定位后的元素
        presence_of_all_elements_located	判断是否至少有 1 个元素存在于 dom 树中。举例：如果页面上有 n 个元素的 class 都是’wp’，那么只要有 1 个元素存在，这个方法就返回 True
        text_to_be_present_in_element	判断某个元素中的 text 是否 包含 了预期的字符串
        text_to_be_present_in_element_value	判断某个元素中的 value 属性是否包含 了预期的字符串
        frame_to_be_available_and_switch_to_it	判断该 frame 是否可以 switch进去，如果可以的话，返回 True 并且 switch 进去，否则返回 False
        invisibility_of_element_located	判断某个元素中是否不存在于dom树或不可见
        element_to_be_clickable	判断某个元素中是否可见并且可点击
        staleness_of	等某个元素从 dom 树中移除，注意，这个方法也是返回 True或 False
        element_to_be_selected	判断某个元素是否被选中了,一般用在下拉列表
        element_selection_state_to_be	判断某个元素的选中状态是否符合预期
        element_located_selection_state_to_be	跟上面的方法作用一样，只是上面的方法传入定位到的 element，而这个方法传入 locator
        alert_is_present	判断页面上是否存在 alert
        ————————————————
        版权声明：本文为CSDN博主「腰椎间盘没你突出」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
        原文链接：https://blog.csdn.net/sinat_41774836/java/article/details/88965281
        '''
        #html_tree1 = BeautifulSoup(str(browser.page_source), 'html.parser')#lxml据说能提高处理网页的效率，所以换换看(2019-11-16再换回来看看)
        
        #browser.get(html_str2)
        #time.sleep(2)#有时候会没加载完内容，所以弄个2秒延时
        #element =WebDriverWait(browser,80,0.5).until(EC.presence_of_element_located((By.TAG_NAME,'body')),message="")
        #html_tree2 = BeautifulSoup(str(browser.page_source), 'html.parser')
        #browser.get(html_str3)
        #time.sleep(2)#有时候会没加载完内容，所以弄个2秒延时        
        #element =WebDriverWait(browser,80,0.5).until(EC.presence_of_element_located((By.TAG_NAME,'body')),message="")
        #html_tree3 = BeautifulSoup(str(browser.page_source), 'html.parser')
    #except selenium.common.exceptions.TimeoutException as err:
    #    print("捕捉到请求超时错误"+str(err))
    #    return False
    except SocketError as e:
        print("SocketError"+str(datetime.now())+str(e))
        return False
    except Exception as err:
        print("网络错误："+str(err))
        return False
    #browser.close()#不能用
    #备份当时获取到的内容，以备以后需要时查看
    with open( '../'+wenjianjia+'/'+'百度贴吧'+name+'吧.html', 'w', encoding='utf-8') as f:
        f.write(str(html_tree1))
    with open( '../'+wenjianjia+'/'+'百度贴吧'+name+'吧.json', 'w', encoding='utf-8') as f:
        f.write(str(html_tree2))
    with open( '../'+wenjianjia+'/'+'百度贴吧'+name+'精品区.html', 'w', encoding='utf-8') as f:
        f.write(str(html_tree3))
        
    #print(html_tree1)
    #print(html_tree2)
    #body=body.encode('UTF-8')
    #encode() 方法以指定的编码格式编码字符串
    #str.encode(encoding='UTF-8',errors='strict')
    #print("UTF-8 编码：", str_utf8)
    #print("UTF-8 解码：", str_utf8.decode('UTF-8','strict'))
    #print(str(html_tree1))
    #print(str(html_tree2))
        
    #----------------------------
    #api
    #body = html_tree2.body # 获取body部分
    #print(html_tree2)
    #body=str(body).split("<body>")[1].split("</body>")[0]
    #print(body)
    data2=None
    data3=None
    #print(data3)
    #网页
    try:
        data2 = json.loads(str(html_tree2))
        data3 = str(data2).replace("'",'"')
        data3 = str(data3).replace("True",'true')
        data3 = str(data3).replace("False",'false')#解决处理转换成json后，保存文件后json格式出错
        body=str(html_tree1).split('<div class="th_footer_l">')[1].split('</div>')[0]#主题贴数，贴子总数，关注人数，
    except Exception as err:
        print("网页:"+str(err))
        return False
    html_tree4 = BeautifulSoup(body, 'html.parser')
    #----------------------------
    '''
    #贴吧信息
    print(html_tree4.find_all('span')[0].string)#主题贴数
    print(html_tree4.find_all('span')[1].string)#贴子总数
    print(str(html_tree3).split('<div class="th_footer_l">')[1].split('</div>')[0].split('<span class="red_text">')[1].split('</span>')[0])#精品贴总数
    print(html_tree4.find_all('span')[2].string)#关注人数
    print(html_tree4.find_all('a')[0].string)#会员名字
    print(str(data2['data']['forum_info']['forum_info']['forum_id']))#这个贴吧的id号
    print(str(data2['data']['forum_info']['level_1_dir_name']))#贴吧目录1
    print(str(data2['data']['forum_info']['level_2_dir_name']))#贴吧目录2
    #当日
    print(str(data2['data']['forum_info']['current_rank_info']['member_count']))#关注人数
    print(str(data2['data']['forum_info']['current_rank_info']['sign_count']))#签到人数
    print(str(data2['data']['forum_info']['current_rank_info']['sign_rank']))#签到排名
    #昨日
    print(str(data2['data']['forum_info']['yesterday_rank_info']['member_count']))#关注人数
    print(str(data2['data']['forum_info']['yesterday_rank_info']['sign_count']))#签到人数
    print(str(data2['data']['forum_info']['yesterday_rank_info']['sign_rank']))#签到排名
    #每周
    print(str(data2['data']['forum_info']['weekly_rank_info']['member_count']))#关注人数
    print(str(data2['data']['forum_info']['weekly_rank_info']['sign_count']))#签到人数
    print(str(data2['data']['forum_info']['weekly_rank_info']['sign_rank']))#签到排名
    #每月
    print(str(data2['data']['forum_info']['monthly_rank_info']['member_count']))#关注人数
    print(str(data2['data']['forum_info']['monthly_rank_info']['sign_count']))#签到人数
    print(str(data2['data']['forum_info']['monthly_rank_info']['sign_rank']))#签到排名
    '''
    
    data4={}
    data4[0]=name#贴吧名
    data4[1]=data2['data']['forum_info']['forum_info']['forum_id']              #这个贴吧的id号
    try:
        data4[2]=data2['data']['forum_info']['level_1_dir_name']                    #贴吧目录1
        data4[3]=data2['data']['forum_info']['level_2_dir_name']                    #贴吧目录2
    except (IndexError, KeyError) as err:
        print("贴吧目录错误："+str(err))
        data4[2]="无"                   #贴吧目录1
        data4[3]="无"                   #贴吧目录2
    '''
    https://www.jianshu.com/p/65aece7b8d78
    python-14-json文件与异常捕获
    '''
    #贴吧信息  
    data4[5]=data2['data']['forum_info']['current_rank_info']['member_count']   #当日关注人数（api端）
    try:
        data4[4]=html_tree4.find_all('span')[2].string                              #当日关注人数(网页端)
    except Exception as err:
        print("当日关注人数(网页端):"+str(err))
        data4[4]=0
    
    try:
        data4[6]=html_tree4.find_all('span')[0].string                              #当日主题贴数(网页端)
    except Exception as err:
        print("当日主题贴数(网页端):"+str(err))
        data4[6]=0
    
    try:
        data4[7]=html_tree4.find_all('span')[1].string                              #当日贴子总数(网页端)
    except Exception as err:
        print("当日贴子总数(网页端):"+str(err))
        data4[7]=0
    
    try:
        data4[9]=html_tree4.find_all('a')[0].string                                 #会员名字(网页端)
    except Exception as err:
        print("会员名字(网页端):"+str(err))
        data4[9]=0
    
    try:
        data4[8]=str(html_tree3).split('<div class="th_footer_l">')[1].split('</div>')[0].split('<span class="red_text">')[1].split('</span>')[0]#精品贴总数
    except Exception as err:
        data4[8]=0
        print("精品贴总数:"+str(err))
    #当日
    data4[10]=data2['data']['forum_info']['current_rank_info']['sign_count']     #当日签到人数
    try:
        data4[11]=data2['data']['forum_info']['current_rank_info']['sign_rank']     #当日签到排名
        #昨日
        data4[12]=data2['data']['forum_info']['yesterday_rank_info']['member_count']#昨天关注人数
        data4[13]=data2['data']['forum_info']['yesterday_rank_info']['sign_count']  #昨天签到人数
        data4[14]=data2['data']['forum_info']['yesterday_rank_info']['sign_rank']   #昨天签到排名
        #每周
        data4[15]=data2['data']['forum_info']['weekly_rank_info']['member_count']   #周均关注人数
        data4[16]=data2['data']['forum_info']['weekly_rank_info']['sign_count']     #周均签到人数
        data4[17]=data2['data']['forum_info']['weekly_rank_info']['sign_rank']      #周均签到排名
        #每月
        data4[18]=data2['data']['forum_info']['monthly_rank_info']['member_count']  #月均关注人数
        data4[19]=data2['data']['forum_info']['monthly_rank_info']['sign_count']    #月均签到人数
        data4[20]=data2['data']['forum_info']['monthly_rank_info']['sign_rank']     #月均签到排名
    except (IndexError, KeyError) as err:
        print("贴吧关注+签到+签到排名错误："+str(err))
        data4[11]=0 #当日签到排名
        #昨日
        data4[12]=0#昨天关注人数
        data4[13]=0#昨天签到人数
        data4[14]=0#昨天签到排名
        #每周
        data4[15]=0#周均关注人数
        data4[16]=0#周均签到人数
        data4[17]=0#周均签到排名
        #每月
        data4[18]=0#月均关注人数
        data4[19]=0#月均签到人数
        data4[20]=0#月均签到排名
 
    temp=[]
    temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    count = 0
    while count < len(data4):
        temp.append(data4[count])
        count = count + 1
    print(str(temp))
    final.append(temp)
        
    write_data(final, '../'+wenjianjia+'/'+'百度贴吧'+name+'吧.csv')
    return True

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='' ,encoding="utf-8") as f:#  'a'  模式，追加内容 写文件
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def usejson():
    # 读取JSON配置文件
    #global weiwancheng
    filename = "../"+wenjianjia+"/tieba.json"
    jsontemp = None
    f_obj = None
    temp=[]
    try:
        f_obj = open(filename, encoding="utf-8")
        jsontemp = json.load(f_obj)
        f_obj.close()
    except Exception as err:  # FileExistsError or OSError:
        print("读取配置文件失败！ "+str(err))
        #f_obj.close()
        exit()
    temp.append(jsontemp['tieba'])
    temp.append(jsontemp['paqucd'])
    return temp
    '''
    for x in tiezilists:
        if x[2] == True:
            time.sleep(random.choice(range(10, 20)))
            print('链接:'+x[0]+',标题'+x[1])
            start(x[0])
        else:
            print('链接:'+x[0]+',标题'+str(x[1])+","+str(x[2])+",该贴不更新！\n")

    print("完成运行！"+str(datetime.now()))
    logger.info("完成运行！"+str(datetime.now()));

    https://www.cnblogs.com/lpdeboke/p/11414254.html
    python中json的基本使用
    https://jingyan.baidu.com/article/c74d6000d138fb0f6b595d45.html
    如何使用python的json模块从json文件读取数据听语音
    https://blog.csdn.net/weixin_41931602/article/details/80557416
    python ： 'gbk' codec can't decode byte 0xbe in position 18: illegal multibyte sequenc
    '''

def start():
    global wenjianjia
    global countx
    global errorx
    #global browser
    global timer
    final=[]
    temp=[]
    Temp =['时间','贴吧名','贴吧id','贴吧目录1','贴吧目录2','当日即时关注人数(网页获取)','当日关注人数(api获取)','当日即时主题贴数','当日即时贴子总数','当日即时精品贴总数','贴吧会员名','当日即时签到人数','当日即时签到排名',
           '昨日关注人数','昨日签到人数','昨日签到排名','每周关注人数','每周签到人数','每周签到排名','每月关注人数','每月签到人数','每月签到排名']#22个
    #global weiwancheng
    #timer.cancel()
    print(str(datetime.now())+",start")
    #print("2233")
    count = 0
    tieba=usejson()
    while count < len(Temp):
        temp.append(Temp[count])
        count = count + 1
    final.append(temp)
    count = 0
    while count < len(tieba[0]):
        temp2='../'+wenjianjia+'/'+'百度贴吧'+tieba[0][count]+'吧.csv'
        if os.path.exists(temp2)==False:
            with open(temp2, 'a', errors='ignore', newline='',encoding="utf-8") as f:#  'a'  模式，追加内容
                f_csv = csv.writer(f)
                f_csv.writerows(final)
        count = count + 1

    timeout=tieba[1]+random.choice(range(30,60))
    chongshi=0
    '''
    #没有以下的情况存在，一定是执行完本次，才开启下一次轮回
    if weiwancheng==True:
        if(errorx<2):
            print("上次爬虫还没执行完，等下一次继续")
            timer = threading.Timer(timeout, start)#一小时=3600s
            timer.start()
            return
        else:
            print("第二次尝试，发现上一次爬虫仍未完成，无法继续爬虫！")
            exit()
        errorx=errorx+1
    weiwancheng=True
    '''
    while countx < len(tieba[0]):
        #if(browser==None):
        #  browser = getSource()
        #else:
        #  browser.service.process.send_signal(signal.SIGTERM)
        #  browser.close()
        #  browser.quit()
        #  os.system('taskkill /im geckodriver.exe /F')#查找清除残余进程
        #  os.system('taskkill /im firefox.exe /F')
        #  browser=None
        #  with open('../'+wenjianjia+'/'+'tieba_log.txt', 'a', encoding='utf-8') as f:
        #        f.write("\n"+str(countx)+".浏览器卡住了\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        #  print(datetime.now())
        #  exit()
        if chongshi>5:
            print("连续重试超过6次，关闭爬虫！")
            exit()
        
        if get_data(tieba[0][countx])==True:
            #browser.save_screenshot("temp.png")
            countx = countx + 1
            chongshi=0
        else:
            print("重试"+str(chongshi+1)+"次")
            chongshi=chongshi+1
        #browser.close()
        #browser.service.process.send_signal(signal.SIGTERM)
        #browser.quit()
        #os.system('taskkill /im geckodriver.exe /F')#查找清除残余进程
        #os.system('taskkill /im firefox.exe /F')
        #browser=None
        #browser.refresh()
        time.sleep(random.choice(range(30,60)))#延迟
    countx = 0
    #os.system('taskkill /im geckodriver.exe /F')#查找清除残余进程
    #os.system('taskkill /im firefox.exe /F')
    #browser=None
    #weiwancheng=False
    print(str(datetime.now())+",end")
    print("延迟："+str(timeout)+"s后，再次爬取")
    timer = threading.Timer(timeout, start)#一小时=3600s
    timer.start()
        
    #with open( '百度贴吧邻家索菲吧.csv', 'w', encoding='utf-8') as f:
         #f.write(str(result))
'''
        try:
        except Exception as err:
            if(browser!=None):
                browser.service.process.send_signal(signal.SIGTERM)
                browser.quit()
                browser=None
            #print(str(err))
            with open('../'+wenjianjia+'/'+'tieba_log.txt', 'a', encoding='utf-8') as f:
                f.write("\n"+str(countx)+'.'+str(err)+"\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            time.sleep(random.choice(range(60,180)))#延迟
            if(errorx<3):
                errorx=errorx+1
                start()
            else:
                print(str(datetime.now())+"，关闭爬虫")
                exit()
        finally:
            errorx=0
            print(str(datetime.now())+":错误清0")
            '''        
    
if __name__ == '__main__':
    cookie = ""
    wenjianjia='贴吧信息记录'
    '''
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    if os.path.exists("../"+wenjianjia+"/logs") == False:
        os.makedirs("../"+wenjianjia+"/logs")  # 创建logs文件夹用来存放日志
    log_path = "../"+wenjianjia+"/logs"
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    '''
    # 日志
    #logger.debug('this is a logger debug message')
    #logger.info('this is a logger info message')
    #logger.warning('this is a logger warning message')
    #logger.error('this is a logger error message')
    #logger.critical('this is a logger critical message')
    # python中logging日志模块详解
    # https://www.cnblogs.com/xianyulouie/p/11041777.html
    try:
        os.makedirs("../"+wenjianjia)
    except Exception as err:#FileExistsError or OSError:
        print("创建文件夹："+str(err))
    start()
    #timer = threading.Timer(0, start)
    #timer.start()
    '''
    temp.append('时间')#-1
    temp.append('贴吧名')#0
    temp.append('贴吧id')#1
    temp.append('贴吧目录1')#2
    temp.append('贴吧目录2')#3
    temp.append('当日关注人数(网页获取)')#4
    temp.append('当日关注人数(api获取)')#5
    temp.append('当日主题贴数')#6
    temp.append('当日贴子总数')#7
    temp.append('当日精品贴总数')#8
    temp.append('贴吧会员名')#9
    temp.append('当日签到人数')#10
    temp.append('当日签到排名')#11
    temp.append('昨日关注人数')#12
    temp.append('昨日签到人数')#13
    temp.append('昨日签到排名')#14
    temp.append('每周关注人数')#15
    temp.append('每周签到人数')#16
    temp.append('每周签到排名')#17
    temp.append('每月关注人数')#18
    temp.append('每月签到人数')#19
    temp.append('每月签到排名')#20
    '''
'''
https://www.cnblogs.com/lizm166/p/8360388.html
https://tieba.baidu.com/f?kw=贴吧名
https://tieba.baidu.com/f?kw=贴吧名&ie=utf-8&tab=good
http://tieba.baidu.com/sign/info?kw=贴吧名&ie=utf-8   贴吧签到人气榜月榜单公布时间：2019年10月30日 23:59，周榜单公布时间：2019年11月09日 23:59
测试用的是这个版本 http://tieba.baidu.com/sign/index?kw=贴吧名&ie=utf-8
https://www.python.org/downloads/release/python-368/
python3 -m pip install selenium==2.53.6（最后支持PhantomJS浏览器的版本，该浏览器从2018年3月4日开始暂停更新）https://github.com/SeleniumHQ/selenium
python3 -m pip install beautifulsoup4 https://github.com/DeronW/beautifulsoup
python3 -m pip install lxml

PhantomJS（https://github.com/ariya/phantomjs），放在python根目录的Scripts文件夹里

Signal翻译过来中文就是信号- -
当然, 本身他就是Linux系统编程中非常重要的概念, 信号机制是进程之间传递消息的一种机制,
其全称为软中断信号
作用是通知进程发生了异步事件。进程之间可以调用系统来传递信号, 本身内核也可以发送信号给进程, 告诉该进程发生了某个事件.

注意，信号只是用来通知某进程发生了什么事件，并不给该进程传递任何数据。

接收信号的进程对不同的信号有三种处理方法

指定处理函数
忽略
根据系统默认值处理, 大部分信号的默认处理是终止进程

然后就是一大段类型了..
Linux系统有两大类信号

POSIX标准的规则信号(regular signal 1-31编号)
实时信号(real-time signal 32-63)

规则信号

信号编号
名称
默认动作
说明

1
SIGHUP
终止
终止控制终端或进程

2
SIGINT
终止
由键盘引起的终端(Ctrl-c)

3
SIGQUIT
dump
控制终端发送给进程的信号, 键盘产生的退出(Ctrl-\),

4
GIGILL
dusmp
非法指令引起

5
SIGTRAP
dump
debug中断

6
SIGABRT/SIGIOT
dump
异常中止

7
SIGBUS/SIGEMT
dump
总线异常/EMT指令

8
SIGFPE
dump
浮点运算溢出

9
SIGKILL
终止
强制杀死进程(大招, 进程不可捕获)

10
SIGUSR1
终止
用户信号, 进程可自定义用途

11
SIGSEGV
dump
非法内存地址引起

12
SIGUSR2
终止
用户信号, 进程可自定义用途

13
SIGPIPE
终止
向某个没有读取的管道中写入数据

14
SIGALRM
终止
时钟中断(闹钟)

15
SIGTERM
终止
进程终止(进程可捕获)

16
SIGSTKFLT
终止
协处理器栈错误

17
SIGCHLD
忽略
子进程退出或中断

18
SIGCONT
继续
如进程停止状态则开始运行

19
SIGSTOP
停止
停止进程运行

20
SIGSTP
停止
键盘产生的停止

21
SIGTTIN
停止
后台进程请求输入

22
SIGTTOU
停止
后台进程请求输出

23
SIGURG
忽略
socket发送紧急情况

24
SIGXCPU
dump
CPU时间限制被打破

25
SIGXFSZ
dump
文件大小限制被打破

26
SIGVTALRM
终止
虚拟定时时钟

27
SIGPROF
终止
profile timer clock

28
SIGWINCH
忽略
窗口尺寸调整

29
SIGIO/SIGPOLL
终止
I/O可用

30
SIGPWR
终止
电源异常

31
SIGSYS/SYSUNUSED
dump
系统调用异常

注意: 由于不同系统中同一个数值对应的信号类型不一样, 所以最好使用信号名称.
信号的数值越小, 优先级越高.

OK, 现在来说说Python中的处理
先列几个常用的信号:

编号
信号名称
说明

2
SIGINT
当按下键盘(Ctrl-c)组合键时进程就会收到这个信号

15
SIGTERM
当用户输入 kill sigterm pid. 对应的进程就会收到这个信号. 这个信号进程是可以捕获并指定函数处理, 例如做一下程序清理等工作. 甚至忽视这个信号

9
SIGKILL
强制杀死进程, 这个信号进程无法忽视, 直接在系统层面把进程杀掉. 所以在Python中他的不能监听的

14
SIGALRM
闹钟信号

作者：thisgf
链接：https://www.jianshu.com/p/c8edab99173d
来源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
'''
