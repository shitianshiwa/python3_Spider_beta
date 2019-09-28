#-*-coding:utf-8 -*-
'''
(beta)0.70
后台运行 nohup python3 /root/test/up主数据爬虫.py &
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
import requests
import csv
import random
import time
import socket
import http.client
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup

browser=None
timer=None

#logname='mea_log.txt'
#global b#全局变量
#url ='https://api.bilibili.com/x/relation/stat?vmid=349991143'#关注数，粉丝数等

def getSource(url):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = headers,timeout = timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

def get_data(url,logname,timeoutx):
    global browser
    
    #global timer
    #global url
    try:
        browser = getSource(url)
        bs = BeautifulSoup(browser, 'html.parser')
        #print(bs)
        data = bs.string.split(":")#字符串切割获得字符串数组
        #print(data)
        valuex=data[len(data)-1].split("}")[0]#字符串再切割获得目标值
        print(logname+",粉丝数："+valuex)
        final = []
        temp=[]
        temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        temp.append(valuex)
        final.append(temp)
        write_data(final, logname+'.csv')
        with open( logname+'_log.txt', 'a', encoding='utf-8') as f:
            f.write("\n"+"粉丝数："+valuex+",延迟："+str(timeoutx)+"s"+"\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")   
        #timer = threading.Timer(timeoutx, get_data(url,logname))
        #timer.start()
            
    except Exception as err:
        #timer.cancel()
        with open( logname, 'a', encoding='utf-8') as f:
            f.write("\n"+str(err)+"\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        print(datetime.now())
        exit()
    finally:
        print(datetime.now())
        
def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def init():
    global timer
    timer.cancel()
    #print("2233")
    timeoutx = 180+random.choice(range(1,10))
    print("延迟："+str(timeoutx)+"s")
    
    get_data("https://api.bilibili.com/x/relation/stat?vmid=349991143","mea",timeoutx)#mea

    get_data("https://api.bilibili.com/x/relation/stat?vmid=375504219","aqua",timeoutx)#湊-阿库娅Official

    get_data("https://api.bilibili.com/x/relation/stat?vmid=1473830","AIChannel",timeoutx)#AIChannel

    get_data("https://api.bilibili.com/x/relation/stat?vmid=12434430","ltt",timeoutx)#Linustechtips
    
    timer = threading.Timer(timeoutx,init)
    timer.start()
    
    #with open( 'bilibili4.html', 'w', encoding='utf-8') as f:
         #f.write(str(result))
    
if __name__ == '__main__':
    timer = threading.Timer(0,init)
    timer.start()
'''
Oo♡ 和Mea的约定 ♡oO ▪ 直播时请不要和其他观众进行版聊。 ▪ 若是性质低劣的评论一直出现会视情况进行封禁。 ▪ 请各位观众不要单方面地提及其他主播的名字。在他人直播间也是同样的，主播未提及时，请尽量不要提起神乐Mea的话题 ▪ 一起遵守礼仪然后享受（？）直播吧！
holoIive二期生、虚拟女仆、湊(みなと)あくあ！ ❖担当画师：がおう 协力：湊阿库娅字幕组。 商务合作与问题反馈请私信。
Hi Domo-!这里是想要和更多人建立羁绊的KizunaAI绊爱，请多支持(ง •̀_•́)ง微博@Kizuna_AI爱酱
刚投稿的视频若突然消失是因为发现错误回炉，不是网站问题。
'''
