#-*-coding:utf-8 -*-
#beta0.111
#import urllib
#from urllib import request as r
#repr = r.urlopen("http://www.baidu.com")
#html = repr.read()
#import re
#url=re.search(r'<img hidefocus="true" src="(.*?)".*?',html).group(1)
#省略一行代码

#print(html)
#with open( 'c:\index.html', 'w', encoding='utf8') as f:
     #f.write(str(html))
import os
import requests
import csv
import random
import time
import socket
import json
import http.client
import urllib.request
import threading
from datetime import datetime
from bs4 import BeautifulSoup

timer=None
wenjianjia=''

def get_content(url , data = None):
    header={
        'Accept': 'application/json, text/plain, */*',
        'Content-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
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
    #return html_text
    
def get_data(html_text):
    global wenjianjia
    try:
        final = []
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
        with open( './'+wenjianjia+'/biliob_log.html', 'w', encoding='utf-8') as f:
            f.write(str(bs)) 
        data2 = json.loads(str(bs))
        data3=data2['content']
        i=1
        for x in data3:
            temp=[]
            temp.append(i)#序号
            temp.append(x['title'])#名字
            temp.append(x['currentPlay'])#播放
            temp.append(x['currentPts'])#综分
            temp.append(x['currentWatch'])#追番
            temp.append(x['currentReview'])#评论
            temp.append(x['currentDanmaku'])#弹幕
            print(temp)
            final.append(temp)
            i+=1
        temp=[]
        temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        final.append(temp)
        temp=[]
        final.append(temp)
        return final
    except Exception as err:
        with open( './'+wenjianjia+'/biliob_log.txt', 'a', encoding='utf-8') as f:
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
            
def start():
    global timer
    global wenjianjia
    #timer.cancel()
    #print("2233")
    timeout=86400#24小时
    print("延迟："+str(timeout)+"s")
    
    url ='https://www.biliob.com/api/bangumi'
    html = get_content(url)
    result = get_data(html)
    write_data(result, './'+wenjianjia+'/Bilob.csv')

    timer = threading.Timer(timeout, start)#一小时=3600s
    timer.start()
    
    #with open( 'bilibili3.html', 'w', encoding='utf-8') as f:
         #f.write(str(result))    

            
if __name__ == '__main__':
    wenjianjia='Biliob番剧排行榜'
    try:
        os.makedirs(wenjianjia)
    except Exception as err:  # FileExistsError or OSError:
        print(str(err))
    final = []
    temp=[]
    temp.append('名字')
    temp.append('播放')
    temp.append('综分')
    temp.append('追番')
    temp.append('评论')
    temp.append('弹幕')
    final.append(temp)
    write_data(final, './'+wenjianjia+'/Bilob.csv')
    start()
    #timer = threading.Timer(0, start)
    #timer.start()
    
'''
https://www.biliob.com/api/bangumi
'''
