import csv

import requests
import re
from bs4 import BeautifulSoup
import  time
import random



class Url_manager_hotboard:
    """
    获取url并进行处理从中获得group_id以及item_id
    """
    def __init__(self):
        #url处理器的url集合
        self.url_collection=set()
        self.id_group=[]

    #获取url的list形式
    def get_url_list(self):
        return    list(self.url_collection)
    #获取id列表
    def get_id_group(self):
        return self.id_group
    #添加url
    def add_url(self,url=None):
        if url!=None:
             self.url_collection.add(url)
             print("添加热榜Url成功")
        else:
            raise ValueError("获得的热榜Url有问题")
    #处理url_list中的url
    def handle_url(self):
        url_list=self.get_url_list()
        for url in url_list:
            #若得到的是trending,则进行处理后再得到id对象
            if re.search("/trending/",url,):
               self.handle_trending(url)
            #若得到的是media_live,则处理下一个url
            elif re.search("/media_live/",url):
                continue
            #涉及到直播的，处理下一个url
            elif re.search("live",url):
                continue
            else :
                id=re.search("/\d+",url)
                # print(id)
                with open("comments_link.csv",mode="a",encoding='utf-8',newline="") as f:
                    self.id_group.append(id.group())
                    csvwriter=csv.writer(f)
                    csvwriter.writerow([id.group(),url])
            print("finish 1")
            time.sleep(random.uniform(0.3,0.5))


    #处理带有trending的url从中获得url并的到id
    def handle_trending(self,url):
        headers = {
            "Refer": "https://www.toutiao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; s_v_web_id=verify_lrrjf71j_uVmEAUyT_wXmZ_4zay_AQOP_99FOFoPh6HD6; local_city_cache=%E5%BC%A0%E5%AE%B6%E5%8F%A3; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; _S_WIN_WH=1232_678; notRedShot=1; msToken=_AB6G7Y6nY2ckN2VnhS1X2yp2zoGqFaVswrTiQgg3GN37fUz4P2qGRlFtLSrBAoNmeMC5_S17S_uLEfQsd0cXVdoCwgBdv5EFMxOSZBy; _ga_QEHZPBE5HH=GS1.1.1706873267.15.1.1706877572.0.0.0; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1706877576%7C19ed18329d7821c294b6adecad4c21e165a6c81a90ec0424cb10ecea63da1f46; tt_scid=wVBpOdjxts6TK1gIHtnJsO.WKSZV7p1DszwIPmjV7k2e7T3lR13e834etMh7UgP.66db"
        }
        #获取到id之后将链接也获取一下，
        with open("comments_link.csv",mode="a",encoding='utf-8',newline="") as f:
            csvwriter=csv.writer(f)
            res=requests.get(url,headers=headers)
            res.encoding="utf-8"
            soup = BeautifulSoup(res.text, "html.parser")
            事件详情 = soup.find_all(name='div', class_='block-container')
            #将事件详情中的id解析出来
            for block_container in 事件详情:
                soup=BeautifulSoup(str(block_container),"html.parser")
                a_list=soup.find_all(name='a')
                for a in a_list:
                    if not re.search("/c/user",str(a["href"])):
                        id=re.search('/\d+',str(a["href"]))
                        if id:
                            self.id_group.append(id.group())
                            csvwriter.writerow([id.group(),a["href"]])
    def get_id_list(self):
        for i in range(len(self.id_group)):
            self.id_group[i]=self.id_group[i][1:]
        id_group_collection=set(self.id_group)
        return list(id_group_collection)


