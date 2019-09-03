#-*-coding:utf-8 -*-
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

logname='bilibili_log.txt'
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
    
def get_data(html_text):
    try:
        final = []
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
        body = bs.body # 获取body部分
        data = body.find('div', {'class': 'media-info-datas'})  # 找到class为media-info-datas的div
        data1 = data.find('div', {'class': 'media-info-count'})  #找到class为media-info-count的div
        data2 = data1.find_all('span', {'class': 'media-info-label'})#找到class为media-info-label的span，文字总播放数，追番人数，弹幕总数
        em= data1.find_all('em')  # 获取所有的em,数字总播放数，追番人数，弹幕总数
        data3 = data.find('div', {'class': 'media-info-score-wrp'})  #找到class为media-info-score-wrp的div
        data4= data3.find('div', {'class': 'media-info-score-content'})#评分
        data5= data3.find('div', {'class': 'media-info-review-times'})#评分人数
        temp=[]
        temp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        count = 0
        while count < 3:
            #temp.append(data2[count].string)
            temp.append(em[count].string)
            count = count + 1
        #print (count, " 小于 5")
        temp.append(data4.string)
        temp.append(data5.string)
        final.append(temp)
        return final
    except Exception as err:
        timer.cancel()
        with open( logname, 'a', encoding='utf-8') as f:
            f.write("\n"+str(err)+"\n"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
        print(datetime.now())
        exit()
    finally:
        print(datetime.now())

def write_data(data, name):
    file_name = name
    with open('./'+file_name, 'a', errors='ignore', newline='') as f:#  'a'  模式，追加内容
            f_csv = csv.writer(f)
            f_csv.writerows(data)
            
def start():
    print("2233")
    url1 ='https://www.bilibili.com/bangumi/media/md139632/'#邻家索菲
    url2 ='https://www.bilibili.com/bangumi/media/md28221404/'#街角魔族
    html1 = get_content(url1)
    result1 = get_data(html1)
    write_data(result1, 'B站邻家索菲数据.csv')
    html2 = get_content(url2)
    result2 = get_data(html2) 
    write_data(result2, 'B站街角魔族数据.csv')
    timer = threading.Timer(3600, start)
    timer.start()
    #with open( 'bilibili.html', 'w', encoding='utf-8') as f:
         #f.write(str(result))
    
if __name__ == '__main__':
    timer = threading.Timer(0, start)
    timer.start()
    
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

