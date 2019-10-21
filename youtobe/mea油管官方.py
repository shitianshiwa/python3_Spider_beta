#-*-coding:utf-8 -*-
#(beta)0.11
'''
后台运行 nohup python3 /root/test/mea油管官方.py
显示所有进程 ps aux
杀死进程 PID（数字）
Linux系统 nohup python3 /root/test/AIChannel官方0.6.py(文件路径每个人都不一样,用filezilla把文件传上linux服务器)
Linux 定时循环执行 python 脚本 - sherlockChen - 博客园
https://www.cnblogs.com/sherlockChen/p/8196590.html
每天一个linux命令（50）：crontab命令 - peida - 博客园
https://www.cnblogs.com/peida/archive/2013/01/08/2850483.html
一、crond简介

crond是linux下用来周期性的执行某种任务或等待处理某些事件的一个守护进程，与windows下的计划任务类似，当安装完成操作系统后，默认会安装此服务工具，并且会自动启动crond进程，crond进程每分钟会定期检查是否有要执行的任务，如果有要执行的任务，则自动执行该任务。
'''
import threading
import csv
import random
import time
import signal
import json
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

browser=None
timer=None
b=0

#https://www.youtube.com/channel/UCWCc8tO-uUl_7SJXIKJACMw
#url ='https://www.youtube.com/channel/UCWCc8tO-uUl_7SJXIKJACMw'
#https://www.youtube.com/channel/UC4YaOt1yT-ZeyB0OmxHgolA


def getSource():
   
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html; charset=utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }
    #使用copy()防止修改原代码定义dict
    cap = DesiredCapabilities.PHANTOMJS.copy() 
 
    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value
 
    # 不载入图片，爬页面速度会快很多
    cap["phantomjs.page.settings.loadImages"] = False
 
    driver = webdriver.PhantomJS(desired_capabilities=cap)#注意selenium的版本，高版本才支持chromedriver.exe.这里selenium==2.53.6
    return driver
  
'''
Python下Selenium PhantomJs设置header的方法
2018年04月07日 11:58:00 weixin_33857679 阅读数 16
https://blog.csdn.net/weixin_33857679/article/details/92267975
--------
driver.get(encodeUrl(url))?
-------------
在Python2.x中：
items() 用于返回一个字典的拷贝列表[Returns a copy of the list of all items (key/value pairs) in D]，占额外的内存。
iteritems() 用于返回本身字典列表操作后的迭代[Returns an iterator on all items(key/value pairs) in D], 不占用额外的内存。
Python 3.x 中，iteritems() 和 viewitems()这两个方法都已经废除了，而items() 得到的是结果和py2.x中viewitems()是一致的。在py3.x中用items() 替代iteritems(), 可以用于 for来循环遍历。
--------------------- 
版权声明：本文为CSDN博主「笔墨留年」的原创文章，遵循CC 4.0 by-sa版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/aaronjny/article/details/62088640
'''

def get_data(url,logname):
    global b
    global timer
    global browser
    try:
        final=[]
        temp=[]
        browser = getSource()
        browser.get(url)
        bs = BeautifulSoup(str(browser.page_source), 'html.parser')#subscriberCountText
        with open( 'youtobe_mea_log.html', 'w', encoding='utf-8') as f:
                 f.write(str(bs))  
        #print(bs)
        body = bs.find_all('script')
        body2=body[26]
        #for x in body:
          #print("666"+str(x.string))
        body3=body2.string.split('window["ytInitialData"] = ')[1].split('window["ytInitialPlayerResponse"] = ')[0].split(';')[0]
        data2 = json.loads(str(body3))
        data4=data2['header']['c4TabbedHeaderRenderer']['subscriberCountText']['runs'][0]['text'].split(' ')[0]
        temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        temp.append(str(data4))
        final.append(temp)
        print(str(data4))

        if(browser!=None):
            browser.service.process.send_signal(signal.SIGTERM)
            browser.quit()
        return final
    
    except Exception as err:
        b+=1
        print(str(b))
        if(timer!=None):
            timer.cancel()
        if(browser!=None):
            browser.service.process.send_signal(signal.SIGTERM)
            browser.quit()
        if(b>10):
            exit()
        with open(logname+'_log.txt', 'a', encoding='utf-8') as f:
            f.write("\n"+str(err)+"\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        print(datetime.now())
        timeoutx = 10+random.choice(range(5,20))
        print("错误延迟："+str(timeoutx)+"s")
        timer = threading.Timer(timeoutx, start)
        timer.start()
    finally:
        print(datetime.now())
        
def write_data(data, name):
    global b
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(data)
    b=0

def start():
    global timer
    if(timer!=None):
        timer.cancel()
    #print("2233")
    timeout=3600
    print("延迟："+str(timeout)+"s")

    result=get_data('https://www.youtube.com/channel/UCWCc8tO-uUl_7SJXIKJACMw','youtobe_mea')
    write_data(result,'youtobe_mea.csv')

    timer = threading.Timer(timeout, start)#一小时=3600s
    timer.start()
    
    #with open( 'youtobe.html', 'w', encoding='utf-8') as f:
         #f.write(str(result))  
    
if __name__ == '__main__':
    final=[]
    temp=[]
    temp.append('时间')
    temp.append('订阅数')
    final.append(temp)
    with open('youtobe_mea.csv', 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(final)
    timer = threading.Timer(0, start)
    timer.start()
    
'''
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
