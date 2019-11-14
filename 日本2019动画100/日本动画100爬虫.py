# coding : UTF-8
# html5lib 	BeautifulSoup(markup, "html5lib")
'''
版本0.013(beta)
后台运行 nohup python3 /root/test/日本动画100爬虫.py
新增获取百分比数据项，2019-11-10
Python 定时任务的实现方式
https://www.cnblogs.com/fengff/p/11011000.html
本文转载自：
https://lz5z.com/Python%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1%E7%9A%84%E5%AE%9E%E7%8E%B0%E6%96%B9%E5%BC%8F/
'''
import os
import csv
import random
import time
import json
import signal
import time
import threading
# import zlib
# import hashlib
# from urllib import request as r
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

wenjianjia=''
#timer = None
'''
Python下Selenium PhantomJs设置header的方法
2018年04月07日 11:58:00 weixin_33857679 阅读数 16
https://blog.csdn.net/weixin_33857679/article/details/92267975
'''


def getSource():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Content-Encoding': 'gzip,deflate,br',
        'Content-Type': 'text/html; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    # 使用copy()防止修改原代码定义dict
    cap = DesiredCapabilities.PHANTOMJS.copy()

    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value

    # 不载入图片，爬页面速度会快很多
    cap["phantomjs.page.settings.loadImages"] = False

    # 注意selenium的版本，高版本才支持chromedriver.exe.这里selenium==2.53.6
    driver = webdriver.PhantomJS(desired_capabilities=cap)
    return driver


def get_data(name, browser):
    global wenjianjia
    browser.get(name)
    # 第一次获取对象 BeautifulSoup(str(browser.page_source), 'html.parser')
    html_tree1 = BeautifulSoup(str(browser.page_source), "html5lib")
    # 备份当时获取到的内容，以备以后需要时查看
    with open('./'+wenjianjia+'/'+'日本动画100.html', 'w', encoding='utf-8') as f:
        f.write(str(html_tree1))

    body = html_tree1.body.find_all('div', id='content')
    body = BeautifulSoup(str(body), "html5lib")  # 第二次获取对象

    #定位或切割获取到的文本内容
    tv = body.find('section', id='ranking-tv')
    tv1 = tv.find_all('h2')
    tv2 = tv.find_all('div',{'class': 'graph'})
    #for temp in tv2:
        #print(temp['style'].split(':')[1].split('%')[0])
    movie = body.find('section', id='ranking-movie')
    movie1 = movie.find_all('h2')
    movie2 = movie.find_all('div',{'class': 'graph'})
    #for temp in movie2:
        #print(temp['style'].split(':')[1].split('%')[0])

    final = []
    temp = []
    temp.append('分割1')
    temp.append(datetime.now())
    #temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))#添加当时处理的时间，有微小误差
    temp.append('分割2')
    i = 0
    while(i<len(tv1)):
        temp.append(str(i+1))#把序号与名字分开到单独的格子里
        temp.append(tv1[i].string)
        temp.append(tv2[i]['style'].split(':')[1].split('%')[0])
        temp.append('分割2')
        # print(tv1[i].string+','+tv2[i]['style'].split(':')[1].split('%')[0])
        i=i+1
    final.append(temp)
    write_data(final, './'+wenjianjia+'/'+'best100_tv.csv')

    final = []
    temp = []
    temp.append('分割1')
    temp.append(datetime.now())
    #temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))#添加当时处理的时间，有微小误差
    temp.append('分割2')
    i = 0
    while(i<len(movie1)):
        temp.append(str(i+1)+' . '+movie1[i].string)
        temp.append(movie2[i]['style'].split(':')[1].split('%')[0])
        temp.append('分割2')
        # print(movie1[i].string+','+movie2[i]['style'].split(':')[1].split('%')[0])
        i=i+1
    final.append(temp)
    write_data(final, './'+wenjianjia+'/'+'best100_movie.csv')

    # print(final)
    # print(str(tv))
    # print(str(movie))
    # with open( 'donghua.html', 'w', encoding='utf-8') as f:
       # f.write(str(tv))

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:  # 'a'  模式，追加内容 写文件
        f_csv = csv.writer(f)
        f_csv.writerows(data)

def start():
    try:
        global wenjianjia
        #global timer
        # print("2233")
        #timeout = 86400+random.choice(range(30, 60))
        #print("延迟："+str(timeout)+"s")
        browser = getSource()
        print("定时周期任务，每日北京时间0:00执行")
        get_data("https://best100.animefestival.jp/", browser)
        browser.service.process.send_signal(signal.SIGTERM)  # 进程终止
        browser.quit()
        #print(datetime.now())
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # timer = threading.Timer(timeout, start)  # 24小时
        # timer.start()
    except Exception as err:
        if(browser != None):
            browser.service.process.send_signal(signal.SIGTERM)
            browser.quit()
        # print(str(err))
        with open('./'+wenjianjia+'/'+'donghua_log.txt', 'a', encoding='utf-8') as f:
            f.write("\n"+str(err)+"\n" +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        print(datetime.now())
        exit()
    finally:
        print(datetime.now())

        # with open( './日本动画100/日本动画100.csv', 'w', encoding='utf-8') as f:
            # f.write(str(result))

if __name__ == '__main__':
    wenjianjia='日本动画100'
    try:
        os.makedirs(wenjianjia)
    except Exception as err:
        print(str(err))
    # BlockingScheduler
    start()
    scheduler = BlockingScheduler()
    scheduler.add_job(start, 'cron', day_of_week='0-6', hour=0, minute=0)
    scheduler.start()
    
'''
https://www.cnblogs.com/lizm166/p/8360388.html
https://tieba.baidu.com/f?kw=贴吧名
http://tieba.baidu.com/sign/info?kw=贴吧名
测试用的是这个版本
https://www.python.org/downloads/release/python-368/
python3 -m pip install selenium==2.53.6（最后支持PhantomJS浏览器的版本，该浏览器从2018年3月4日开始暂停更新）https://github.com/SeleniumHQ/selenium
PhantomJS（https://github.com/ariya/phantomjs），放在python根目录的Scripts文件夹里
python3 -m pip install beautifulsoup4 https://github.com/DeronW/beautifulsoup
python3 -m pip install html5lib
python3 -m pip install apscheduler

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
