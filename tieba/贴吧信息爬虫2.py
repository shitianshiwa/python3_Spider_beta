#coding : UTF-8
'''
版本0.132(beta)
后台运行 nohup python3 /root/test/贴吧信息爬虫2.py
'''
import os
import csv
import random
import time
import json
import signal
import time
import threading
#import zlib
#import hashlib
#from urllib import request as r
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

wenjianjia=''
tieba={}
timer=None
countx = 0
errorx=0
'''
def req_maker(path):
    if path:
        req = r.Request(path)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36")
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        req.add_header("Accept-Encoding", "gzip, deflate, sdch")
        req.add_header("Accept-Language", "zh-CN,zh;q=0.8,en;q=0.6")
        req.add_header("Cookie", cookie)
        return req
    else:
        return None


def get_response_str(req):
    with r.urlopen(req) as f:
        decompressed_data =zlib.decompress(f.read(), 16 + zlib.MAX_WBITS)
    return str(decompressed_data, "utf-8", errors='replace')
        

def get_now_str():
    return int(float(time.time()) * 1000)
    
Python下Selenium PhantomJs设置header的方法
2018年04月07日 11:58:00 weixin_33857679 阅读数 16
https://blog.csdn.net/weixin_33857679/article/details/92267975
'''
def getSource():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Content-Encoding': 'gzip,deflate,br',
        'Content-Type': 'text/html; charset=utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Cookie':''  
    }
    #使用copy()防止修改原代码定义dict
    cap = DesiredCapabilities.PHANTOMJS.copy() 
 
    for key, value in headers.items():
        cap['phantomjs.page.customHeaders.{}'.format(key)] = value
 
    # 不载入图片，爬页面速度会快很多
    cap["phantomjs.page.settings.loadImages"] = False
 
    driver = webdriver.PhantomJS(desired_capabilities=cap)#注意selenium的版本，高版本才支持chromedriver.exe.这里selenium==2.53.6
    return driver

def get_data(name,browser):
    global wenjianjia
    final = []
    str2=name.encode('utf-8')
    str2=str(str2).replace('\\x','%')
    str2=str2.split("'")[1]
    html_str1=None
    html_str2=None
    html_str3=None
    '''
    html_str1 = get_response_str(req_maker('https://tieba.baidu.com/f?kw='+str2))
    html_str2 = get_response_str(req_maker('http://tieba.baidu.com/sign/info?kw='+str2+'&ie=utf-8'))
    html_tree1=BeautifulSoup(html_str1, 'html.parser')
    html_tree2=BeautifulSoup(html_str2, 'html.parser')
    '''
    html_str1='https://tieba.baidu.com/f?kw='+str2#直接获取贴吧主页的网页必须把中文转utf-8在连进去
    html_str2='http://tieba.baidu.com/sign/info?kw='+str2+'&ie=utf-8'#贴吧信息api
    html_str3='https://tieba.baidu.com/f?kw='+str2+'&ie=utf-8&tab=good'#贴吧精品区网页
    browser.get(html_str1)    
    html_tree1 = BeautifulSoup(str(browser.page_source), 'html.parser')
    browser.get(html_str2)
    html_tree2 = BeautifulSoup(str(browser.page_source), 'html.parser')
    browser.get(html_str3)
    html_tree3 = BeautifulSoup(str(browser.page_source), 'html.parser')
    #备份当时获取到的内容，以备以后需要时查看
    with open( './'+wenjianjia+'/'+'百度贴吧'+name+'吧.html', 'w', encoding='utf-8') as f:
        f.write(str(html_tree1))
    with open( './'+wenjianjia+'/'+'百度贴吧'+name+'吧.json', 'w', encoding='utf-8') as f:
        f.write(str(html_tree2))
    with open( './'+wenjianjia+'/'+'百度贴吧'+name+'精品区.html', 'w', encoding='utf-8') as f:
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
    body = html_tree2.body # 获取body部分
    body=str(body).split("<body>")[1].split("</body>")[0]
    #print(body)
    data2 = json.loads(str(body))
    data3 = str(data2).replace("'",'"')
    data3 = str(data3).replace("True",'true')
    data3 = str(data3).replace("False",'false')#解决处理转换成json后，保存文件后json格式出错
    #print(data3)
    #网页
    body=str(html_tree1).split('<div class="th_footer_l">')[1].split('</div>')[0]#主题贴数，贴子总数，关注人数，
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
    data4[2]=data2['data']['forum_info']['level_1_dir_name']                    #贴吧目录1
    data4[3]=data2['data']['forum_info']['level_2_dir_name']                    #贴吧目录2
    #贴吧信息  
    data4[4]=html_tree4.find_all('span')[2].string                              #当日关注人数(网页端)
    data4[5]=data2['data']['forum_info']['current_rank_info']['member_count']   #当日关注人数（api端）
    data4[6]=html_tree4.find_all('span')[0].string                              #当日主题贴数(网页端)
    data4[7]=html_tree4.find_all('span')[1].string                              #当日贴子总数(网页端)
    data4[8]=str(html_tree3).split('<div class="th_footer_l">')[1].split('</div>')[0].split('<span class="red_text">')[1].split('</span>')[0]#精品贴总数
    data4[9]=html_tree4.find_all('a')[0].string                                 #会员名字(网页端)
    #当日
    data4[10]=data2['data']['forum_info']['current_rank_info']['sign_count']     #当日签到人数
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

    temp=[]
    temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    count = 0
    while count < len(data4):
        temp.append(data4[count])
        count = count + 1
    print(str(temp))
    final.append(temp)
        
    write_data(final, './'+wenjianjia+'/'+'百度贴吧'+name+'吧.csv')

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容 写文件
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def start():
    global wenjianjia
    global countx
    global errorx
    try:
        global timer
        #timer.cancel()
        browser = getSource()
        #print("2233")
        timeout=3600+random.choice(range(30,60))
        print("延迟："+str(timeout)+"s")
        
        while countx < len(tieba):
            get_data(tieba[countx],browser)
            time.sleep(2)#延迟
            countx = countx + 1
        countx = 0
        browser.service.process.send_signal(signal.SIGTERM)#进程终止
        browser.quit()
        print(datetime.now())
        timer = threading.Timer(timeout, start)#一小时=3600s
        timer.start()
    except Exception as err:
        if(browser!=None):
            browser.service.process.send_signal(signal.SIGTERM)
            browser.quit()
        #print(str(err))
        with open('./'+wenjianjia+'/'+'tieba_log.txt', 'a', encoding='utf-8') as f:
            f.write("\n"+str(countx)+'.'+str(err)+"\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        time.sleep(60)#延迟
        if(errorx<3):
            errorx=errorx+1
            start()
        print(datetime.now())
        exit()
    finally:
        errorx=0
        print(datetime.now())
        
    #with open( '百度贴吧邻家索菲吧.csv', 'w', encoding='utf-8') as f:
         #f.write(str(result))
    
if __name__ == '__main__':
    cookie = ""
    final=[]
    temp=[]
    Tieba=["邻家的吸血鬼小妹","邻家索菲","魔兽地图编辑器","天使降临到我身边","天使降临到了我身边","vtuber","台风","东方","战争雷霆","舰队collection","街角魔族"]#11个
    Temp =['时间','贴吧名','贴吧id','贴吧目录1','贴吧目录2','当日即时关注人数(网页获取)','当日关注人数(api获取)','当日即时主题贴数','当日即时贴子总数','当日即时精品贴总数','贴吧会员名','当日即时签到人数','当日即时签到排名',
           '昨日关注人数','昨日签到人数','昨日签到排名','每周关注人数','每周签到人数','每周签到排名','每月关注人数','每月签到人数','每月签到排名']#22个
    wenjianjia='贴吧信息记录'
    try:
        os.makedirs(wenjianjia)
    except Exception as err:#FileExistsError or OSError:
        print(str(err))
    count = 0
    while count < len(Tieba):
        tieba[count] = Tieba[count]
        count = count + 1
    count = 0
    while count < len(Temp):
        temp.append(Temp[count])
        count = count + 1
    final.append(temp)
    count = 0
    while count < len(tieba):
        with open('./'+wenjianjia+'/'+'百度贴吧'+tieba[count]+'吧.csv', 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(final)
        count = count + 1
    start()
    #timer = threading.Timer(0, start)
    #timer.start()
    '''
    tieba[0]="邻家的吸血鬼小妹"
    tieba[1]="邻家索菲"
    tieba[2]="魔兽地图编辑器"
    tieba[3]="天使降临到我身边"
    tieba[4]="天使降临到了我身边"
    tieba[5]="vtuber"
    tieba[6]="台风"
    tieba[7]="东方"
    tieba[8]="战争雷霆"
    tieba[9]="舰队collection"
    tieba[10]="街角魔族"
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
http://tieba.baidu.com/sign/info?kw=贴吧名
测试用的是这个版本
https://www.python.org/downloads/release/python-368/
pip install selenium==2.53.6（最后支持PhantomJS浏览器的版本，该浏览器从2018年3月4日开始暂停更新）https://github.com/SeleniumHQ/selenium
PhantomJS（https://github.com/ariya/phantomjs），放在python根目录的Scripts文件夹里
pip install beautifulsoup4 https://github.com/DeronW/beautifulsoup

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
