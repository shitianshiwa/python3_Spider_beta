#-*-coding:utf-8 -*-
#(beta)0.2221
import os
import threading
import requests
import csv
import random
import time
import socket
import http.client
import json
import urllib.request
#import B站番剧数据爬虫2
from datetime import datetime
from bs4 import BeautifulSoup

wenjianjia=''
logname='bilibili_log.txt'
A=['https://api.bilibili.com/pgc/view/web/media?media_id=139632','https://api.bilibili.com/pgc/view/web/media?media_id=28221404','https://api.bilibili.com/pgc/view/web/media?media_id=4316442','https://api.bilibili.com/pgc/view/web/media?media_id=28224128']
B=['邻家索菲','街角魔族','天使降临到我身边','恋爱小行星']
C=['B站邻家索菲数据.csv','B站街角魔族数据.csv','天使降临到我身边.csv','恋爱小行星.csv']
#C2=['B站邻家索菲数据2.csv','B站街角魔族数据2.csv','天使降临到我身边2.csv','恋爱小行星2.csv']
timer=None

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
    
def get_data(html_text,name):
    global wenjianjia
    try:
        final = []
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象 html.parser
        with open('./'+wenjianjia+'/'+'bilibili_fanju_log.html', 'w', encoding='utf-8') as f:
             f.write(str(bs))
        '''
        #https://www.runoob.com/python3/python3-json.html
        json.dumps(): 对数据进行编码。
        json.loads(): 对数据进行解码。
        #json_str = json.dumps(str(bs))
        '''
        data2 = json.loads(str(bs))
        #print(data2['result']['stat'])
        #print(data2['result']['rating'])
        data={}
        data[0] = data2['result']['stat']['views']#总播放数
        data[1] = data2['result']['stat']['favorites']#追番人数
        data[2] = data2['result']['stat']['danmakus'] #弹幕总数
        try:
            data[3] = data2['result']['rating']['score']#评分 未完结的番剧没有这个？
            data[4] = data2['result']['rating']['count']#评分人数 未完结的番剧没有这个？
        except Exception as err:
            print("没有评分")
        temp=[]
        temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        count = 0
        while count < len(data):
            temp.append(data[count])
            count = count + 1
        #print (count, " 小于 5")
        print(name+":"+str(temp))
        final.append(temp)
        return final
    
    except Exception as err:
        #timer.cancel()
        with open('./'+wenjianjia+'/'+logname, 'a', encoding='utf-8') as f:
            f.write("\n"+str(err)+"\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        print(datetime.now())
        exit()
    finally:
        print(datetime.now())

def write_data(data, name):
    with open(name, 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(data)
            
def start():
    global timer
    global wenjianjia
    #if timer!=None:
        #timer.cancel()
    #print("2233")
    timeout=3600+random.choice(range(1, 10))
    print("延迟："+str(timeout)+"s")
    i=0
    while(i<len(C)):
        html = get_content(A[i])
        result = get_data(html,B[i])
        write_data(result,'./'+wenjianjia+'/'+C[i])
        i=i+1
        time.sleep(2)

    #B站番剧数据爬虫2.start()
    timer = threading.Timer(timeout, start)#一小时=3600s
    timer.start()
    
    #html = get_content('https://api.bilibili.com/pgc/view/web/media?media_id=139632')#邻家索菲 https://www.bilibili.com/bangumi/media/md139632/
    #result = get_data(html,'邻家索菲')
    #write_data(result,'B站邻家索菲数据.csv')
    
    #with open( 'bilibili.html', 'w', encoding='utf-8') as f:
         #f.write(str(result))
    
if __name__ == '__main__':
    wenjianjia='B站番剧数据爬虫'
    try:
        os.makedirs(wenjianjia)
    except Exception as err:
        print(str(err))
    final=[]
    temp=[]
    Temp =['时间','播放数','关注','弹幕','评分','评分人数']#共6个
    count = 0
    while count < len(Temp):
        temp.append(Temp[count])
        count = count + 1
    final.append(temp)
    i=0
    while(i<len(C)):
        with open('./'+wenjianjia+'/'+C[i], 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(final)
        i=i+1
    '''
    i=0
    while(i<len(C2)):
        with open('./'+wenjianjia+'/'+C2[i], 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(final)
        i=i+1
    '''
    start()
    #timer = threading.Timer(0, start)
    #timer.start()
    
'''
邻家索菲 萌系漫画改
总播放
1522.2万
 
追番人数
95.8万
 
弹幕总数
37.1万
9.7 
9450人评
2018年10月5日 开播 已完结, 全12话
简介：天野灯在意外的事情中被名为索菲·特瓦伊莱特的吸血鬼女孩所救，于是她对索菲一见钟情。灯来到了索菲的家中，开始了半强行同居。索菲虽然是吸血鬼，但她并不会袭击人类，她会在网上购买血液和感兴趣的动画商品，过着现代的庶民生活。这是个现今与吸血鬼一起同居的喜剧。
'''

'''
街角魔族 漫画改日常萌系搞笑魔法
总播放
400.5万
 
追番人数
62.6万
 
弹幕总数
8.2万
9.8 
4300人评
2019年7月12日 开播 连载中, 每周五 15:00更新
简介：某天早晨，突然觉醒了暗之力量的女高中生·吉田优子，为了解除一族所遭受的诅咒而准备开始打倒魔法少女！！但对方却是自己的救命恩人！？而且根本就没可能打赢！？废柴系庶民派魔族与高冷系肌肉魔法少女编织的日常系魔法喜剧开始！！！
'''
'''
天使降临到我身边 日常治愈漫画改萌系搞笑
总播放
2987.8万
 
追番人数
156.3万
 
弹幕总数
102.2万
9.8 
28620人评
2019年1月8日开播 已完结, 全13话
简介：怕生的御宅族女大学生宫子，遇到了天使般的小学生！？在看到妹妹带来的新朋友小花的瞬间，宫子就无法抑制住心跳！！她为了和小花成为朋友而奋斗，但……“想要和超绝可爱的她做朋友”系小品喜剧，开幕！
'''
