
import requests
import csv
import time
import random

def get_content(group_id=None,item_id=None):
    #首先获取参数如若id不正确的话则抛出异常
    offset = 0
    if group_id==None  or item_id==None:
        raise ValueError("获取评论时某一id不正确")
    url = 'https://www.toutiao.com/article/v4/tab_comments/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        # 获取评论的Cookie
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; passport_csrf_token=6b0c674f949ca315dfdefa5126088f37; passport_csrf_token_default=6b0c674f949ca315dfdefa5126088f37; s_v_web_id=verify_lu6kgezg_NHthdRZy_GIoV_4y1H_9PRU_ceS1E9vlM9tD; local_city_cache=%E6%88%90%E9%83%BD; tt_scid=soR2SEXELlZfJkzhk09Q4OPlK2.v7GZk.LqWYlroIACc-E8MTBX-8Z-HU7nrKZXU83c6; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1711714387%7Cf0f7e4638242dc749ce17b0a97026395ca8a501f7069a296ccd2ad6b26d781b1; msToken=zPMDuYt0uwjsVKmp9azJYWa_6bVKU2QPgoACFYPshAS1Qi3j4CjP6akigUZOHm6Sv1qEr6u8QM16NiC3KiSgvk-SWnFPl2YVN42jqCYs; _ga_QEHZPBE5HH=GS1.1.1711711051.51.1.1711714607.0.0.0"
    }
    params = {
        "aid": "24",
        "app_name": "toutiao_web",
        "offset": f"{offset}",
        "count": "20",
        "group_id": f"{group_id}",
        "item_id": f"{item_id}",
        #获取评论的_signature
        "_signature": "_02B4Z6wo00d01yzJoYAAAIDAWuZ8z9w55fss7aUAAK0.f2hYQi5Xm5RjQqq0qlQd9gwGA.o.WnaqQK.gswJ.oiphIr-aUUCOcAU0HQUK9Mdu9T2tyi-cOdT0sxsCX.ZC9pJhXjj7ahuIyMDXaa"
    }
    #首先请求一次获得评论总数和评论的title
    re = requests.get(url, headers=headers, params=params)
    re.encoding = "utf-8"
    if not re:
        print("获取评论时未得到数据")
        return
    re_js=re.json()
    totalnum = re_js["total_number"]

    title = re_js["repost_params"]["title"]
    if totalnum < 40:
        print(f"该热点:《{title}》 无足够评论，跳过")
        return
    else:
        print(f"即将爬取:《{title} 》所包含的评论")
    times = int(totalnum / 20 + 1)
    print(times)
    newline = ""
    user_id_list=[]#用于获取所有用户的id
    import os
    #若已经爬取过则跳过
    target=f"./commentstwo/{params['item_id']}.csv"
    if os.path.exists(target):
        print(f"目标文件 {target} 已经存在，跳过！")
        return
    with open(f"./commentstwo/{params['item_id']}.csv", mode="w", encoding="utf-8", newline=newline) as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([str(title).replace("\n","")])#先把title写入csv文件
        count = 1
        comment_count=0
        reply_total_count=0
        for i in range(times):
            params["offset"] = f"{offset}"
            re = requests.get(url, headers=headers, params=params)
            re_js = re.json()
            data = re_js["data"]
            length=len(data)
            if length==0:break#若返回的评论数为0，则退出循环
            for j in range(length):
                dict = [str(data[j]["comment"]["text"]).replace("\n", ""),
                        data[j]["comment"]["user_id"],
                        data[j]["comment"]["user_name"],
                        data[j]['comment']['publish_loc_info']
                        ]
                user_id_list.append(dict[1])
                if i<3:#只对前三次的评论爬取回复，后续回复数骤降，没有爬取的必要
                    comment_id = data[j]["comment"]["id"]
                    reply_list, reply_count ,sub_user_id_list= get_reply(comment_id)
                    if  sub_user_id_list is not None:
                        user_id_list.extend(sub_user_id_list)
                    reply_total_count += reply_count
                    if reply_count != 0 and  reply_list is not None:
                        dict.append(reply_list)
                        reply_list.append(reply_count)
                # print(f"第{j+1}条： conmment:{dict[0]} ")
                csvwriter.writerow(dict)
            print(f"第{count}次完成")
            count += 1
            offset += 20
            #睡眠随机一段时间用于反爬
            time.sleep(random.uniform(0.5,1))
            comment_count+=length
    print(f"共爬取{comment_count}条评论;{reply_total_count}条回复")
    #去重操作防止同一个用户id重复,效果较好
    user_id_collection=set(user_id_list)
    user_id_list=list(user_id_collection)
    #将用户id写入文件
    with open(f"./userstwo/userid/{group_id}.csv",mode="w",encoding="utf-8",newline=newline)as f:
        csvwriter=csv.writer(f)
        for user_id in user_id_list:
            csvwriter.writerow([user_id])
    re.close()

def get_reply(id):#获取某一评论的回复
    offset = 0
    url = 'https://www.toutiao.com/2/comment/v4/reply_list/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        # 获取回复的Cookie
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; passport_csrf_token=6b0c674f949ca315dfdefa5126088f37; passport_csrf_token_default=6b0c674f949ca315dfdefa5126088f37; s_v_web_id=verify_lu6kgezg_NHthdRZy_GIoV_4y1H_9PRU_ceS1E9vlM9tD; local_city_cache=%E6%88%90%E9%83%BD; msToken=zPMDuYt0uwjsVKmp9azJYWa_6bVKU2QPgoACFYPshAS1Qi3j4CjP6akigUZOHm6Sv1qEr6u8QM16NiC3KiSgvk-SWnFPl2YVN42jqCYs; _ga_QEHZPBE5HH=GS1.1.1711711051.51.1.1711714607.0.0.0; tt_scid=cUqc0mLAIxnyHB62gIsZ7wgeB.kFwDzeGLyDylsi38qUr22ZL15TgYjWCYU-Ws8Gc45d; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1711714609%7Ca1c6124c9de0e861a2fcbddb0a2b162927db5a0c681ab77b9792660ce8ce7907"
    }
    params = {
        "aid": "24",
        "app_name": "toutiao_web",
        "id": f"{id}",
        "offset": f"{offset}",
        "count": "20",
        "repost": "0",
        #获取回复的_signature
        "_signature": "_02B4Z6wo00901qlq0lQAAIDB30UPG3XwAmqpTtbAAMxof9lC.Z4upsty8MKxL4n5ev4XLg.RCFPffHfSGA4cltpOmp-ZVi5UgknJxWBTFX1e6QYqlHz-.AgyZ5voyio.WOSMEYBPtF-MvbEX6a"
    }
    #首先得到一个回复总数
    re=requests.get(url=url,headers=headers,params=params)
    re.encoding="utf-8"
    if not re:
        print("获取回复时没有得到数据")
        return
    re_js=re.json()
    data=re_js["data"]
    totalnum=data["total_count"]
    times=int(totalnum/20) +1
    reply_count=0
    reply_list = []
    user_id_list=[]
    for i in range(times):
        params["offset"]=offset
        offset+=15
        re = requests.get(url=url, headers=headers, params=params)
        re.encoding = "utf-8"
        re_js = re.json()
        data = re_js["data"]["data"]
        if data==None:
            print("没有获得对应的回复")
            return None,0,None
        for data_item in data:
            reply_item=[]
            reply_item.append(str(data_item["text"]).replace("\n",""))
            reply_item.append(data_item["user"]["user_id"])
            user_id_list.append(data_item["user"]["user_id"])#回复的usera_id
            reply_item.append(data_item["user"]["name"])
            reply_item.append(data_item["publish_loc_info"])

            reply_list.append(reply_item)
            if reply_item[0]:     reply_count+=1#有回复则回复数加一
    re.close()
    return reply_list,reply_count,user_id_list


