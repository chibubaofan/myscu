import re
import os
import csv
import time
import random
import requests
from get_user_agent import get_user_agent
"""
用于获取用户属性的py
"""
def get_all_user_fans_stat():
    """
    用于读取./users/userid下的所有文件将其一一获取其fans_stat信息写入对应的userid_with_fans_stat文件中
    :return: void
    """
    #首先从目录中获取所有的文件路径
    base_dir=".\\users\\userid"
    files=[os.path.join(base_dir,file)for file in os.listdir(base_dir)]
    #得到文件路径后对每一个文件进行读取、获取属性，写入的操作
    count=0
    for file in files:
        if count==10:
            time.sleep(60)
            count=0
            print("休息一分钟防止被封")
        time1=time.time()

        #解析出读取文件的id
        id=file.split("\\")[3]
        id=re.search("\d+",id).group()
        #若目标文件已经存在，则停止获取，
        target=f".\\users\\userid_with_fans_stat\\{id}.csv"
        if os.path.exists(target):
            print(f"目标文件 {target} 已经存在，跳过！")
            continue
        print(f"正在执行：{target}")
        #设置一个列表用于装填属性方便后续写入
        user_fans_stat_list=[]
        #读操作:占用大量时间，应该用协程来做，奈何我太菜
        with open(file,mode="r") as f:
            reader=csv.reader(f)
            for row in reader:
                #读取一行-获得属性-保存至list
                user_fans_stat=get_user_fans_stat(row[0])
                if user_fans_stat==None:
                    user_fans_stat_list.append([row[0],"None"])
                    continue
                attribute_item=[row[0],user_fans_stat]
                user_fans_stat_list.append(attribute_item)
                time.sleep(random.uniform(0,0.1))
        time2=time.time()
        timeused=time2-time1

        #写操作
        newline = ""
        with open(f".\\users\\userid_with_fans_stat\\{id}.csv",mode="w",encoding="utf-8",newline=newline) as f:
            writer=csv.writer(f)
            for i in user_fans_stat_list:
                writer.writerow(i)
            print(f"finish userid_with_fans_stat{id}.csv  共用时{timeused/60}分钟")
        count+=1

################################################################################################################################################################
def get_token(id):
    time.sleep(random.uniform(0.1,0.2))
    token = ""  # 首先要获得token，_signature可以勤更换
    url = f"https://www.toutiao.com/c/user/{id}/"
    headers = {
        "Connection":"close",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; s_v_web_id=verify_lrrjf71j_uVmEAUyT_wXmZ_4zay_AQOP_99FOFoPh6HD6; local_city_cache=%E5%BC%A0%E5%AE%B6%E5%8F%A3; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; msToken=wCav6ZIquffjfxOgjrO6eSOczzA-jBtNXgrrmX90PMrTxBqsa5BXkJvnfLILbQ23xXgfU9iZ5Zr73SytjscJNgtW83Lumm9gJYaj6nW7JA==; _ga_QEHZPBE5HH=GS1.1.1707728786.39.1.1707729284.0.0.0; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1707729285%7C2f84f2a03328dc72b1727c66af4618dd7ded0d83abadde06ff0f9559d88e9c33; tt_scid=zi6lIT2ZyDwud-I0U06-4xqwrIdsNwKmnJODCIU6yvyyEKG0xmDzPewognOB2O.D85c0"
    }
    params = {
        "source": "amos_land_page"
    }
    res = requests.get(url=url, headers=headers, params=params)
    location = res.url
    # 此处得到了token
    token=location.split("/")
    if len(token)<7:
        print("获取的token不正确  返回None")
        return None
    token=token[6]
    res.close()
    return token


def get_user_fans_stat(id):
    """
    https://www.toutiao.com/c/user/token/MS4wLjABAAAAUX9MVPDDeUDPRQ2yk5YA973JZ0N4VvF-E1qu6h5J0Ic/?source=amos_land_page&log_from=3352bc9b49724_1707038142368
    用于获取单个用户的获赞数、关注数和粉丝数
    :param id: user_id
    :return: attribute_list=[digg_count:获赞数  fans:粉丝数  following:关注数]
    """

    token=get_token(id)
    if not token:
        return None
    #得到token后拼接url的到该用户的获赞数，粉丝数和关注数
    url = "https://www.toutiao.com/api/pc/user/fans_stat"
    headers = {
        "Origin": "https://www.toutiao.com/",
        "User-Agent": f"{get_user_agent()}",
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; passport_csrf_token=6b0c674f949ca315dfdefa5126088f37; passport_csrf_token_default=6b0c674f949ca315dfdefa5126088f37; s_v_web_id=verify_lu6kgezg_NHthdRZy_GIoV_4y1H_9PRU_ceS1E9vlM9tD; local_city_cache=%E6%88%90%E9%83%BD; msToken=zPMDuYt0uwjsVKmp9azJYWa_6bVKU2QPgoACFYPshAS1Qi3j4CjP6akigUZOHm6Sv1qEr6u8QM16NiC3KiSgvk-SWnFPl2YVN42jqCYs; tt_scid=cUqc0mLAIxnyHB62gIsZ7wgeB.kFwDzeGLyDylsi38qUr22ZL15TgYjWCYU-Ws8Gc45d; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1711714609%7Ca1c6124c9de0e861a2fcbddb0a2b162927db5a0c681ab77b9792660ce8ce7907; _ga_QEHZPBE5HH=GS1.1.1711711051.51.1.1711715562.0.0.0"
    }
    data = {
        "token": f"{token}",
        "_signature": "_02B4Z6wo00f01sc7ufQAAIDBsRRku-IDv6rHH71AANfVbUbejZnxAVIOxog3MkWpEB1MseQofUVHNmWqyYWAhYK.nrsbGepxRwwoDxYSajsBYlniI-e8bGWkyQQPYW29X7i2UPjd5jIwHu8Zf6"
    }
    res = requests.post(url=url, headers=headers, data=data)
    requests.DEFAULT_RETRIES = 5
    res.encoding = "utf-8"
    if not res:
        print("请求时没有得到想要的内容，返回None")
        return None
    re_js = res.json()
    # print(re_js)
    #从json中解析出需要的属性
    #print(token)
    data=re_js["data"]
    if len(data)==0:
        return ["Undefined","Undefined","Undefined"]
    digg_count=str(data["digg_count"])
    fans=str(data["fans"])
    following=str(data["following"])
    # print(f"获赞数：{digg_count}  粉丝数：{fans}  关注数：{following}")
    #由于属性中包含文字并且是字符串，接下来处理为数字
    attribute_list=[digg_count,fans,following]
    for i in range(len(attribute_list)):
        tail = attribute_list[i][-1]
        attribute_list[i] = attribute_list[i][0:-1]
        if tail == "万":
            num = float(attribute_list[i])
            num = num * 10000
            attribute_list[i] = int(num)
        elif tail == "亿":
            num = float(attribute_list[i])
            num = num * 100000000
            attribute_list[i] = int(num)
        else:
            attribute_list[i] += tail
            attribute_list[i] = int(attribute_list[i])
    res.close()
    return attribute_list

print(get_token(3282235397))