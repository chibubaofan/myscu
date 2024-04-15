import random
import requests
import re
import os
import csv
import time
from User_attribute_gainer import get_token
from get_user_agent import get_user_agent

def get_all_user_fans():
    """
    用于获取目前所拥有的所有id的粉丝列表
    """
    # 首先从目录中获取所有的文件路径
    base_dir = ".\\users\\userid"
    files = [os.path.join(base_dir, file) for file in os.listdir(base_dir)]
    # 得到文件路径后对每一个文件进行读取、获取属性，写入的操作
    count = 0
    for file in files:
        if count == 10:
            print("休息一分钟防止被封")
            time.sleep(60)
            count = 0

        time1 = time.time()
        # 解析出读取文件的id
        id = file.split("\\")[3]
        id = re.search("\d+", id).group()
        # 若目标文件已经存在，则停止获取，
        target = f".\\users\\userid_with_fans_list\\{id}.csv"
        print(f"正在执行：{target}")
        #首先将所有userid读取出来，边爬粉丝列表边写
        user_id_list=[]
        with open(file, mode="r") as f:
            reader = csv.reader(f)
            for row in reader:
                user_id_list.append(row[0])
                #print(row[0])
        if os.path.exists(target):
            # 接下来读取target中有多少行，从而可以持续写入

            csv.field_size_limit(500 * 1024 * 1024)
            with open(target, mode="r", encoding="utf-8") as f:
                csvreader = csv.reader(f)
                length =0
                for row in csvreader:
                    length+=1
                print(length)
                user_id_list = user_id_list[length:]
                if len(user_id_list)!=0:
                    count+=1
        #接下来边获取边写入
        newline=""
        with open(target,mode="a",encoding="utf-8",newline=newline)as f:
            writer = csv.writer(f)
            for user_id in user_id_list:
                user_fans_item=[]
                user_fans_item.append(user_id)
                token,fans_list=get_user_fans_list(user_id)
                user_fans_item.append(token)
                user_fans_item.append(fans_list)
                writer.writerow(user_fans_item)

        #完成一次后提示
        time2 = time.time()
        timeused = time2 - time1
        print(f"finish userid_with_fans_stat{id}.csv  共用时{timeused / 60}分钟")







def get_user_fans_list(id):
    """
    用于获取单个用户的粉丝列表
    :param id: 用户的唯一标识符
    :return: 返回fans_list和id对应的token
    """
    fans_list=[]
    url="https://www.toutiao.com/api/pc/user/followed"
    headers = {
        "Connection":"close",
        "User-Agent": f"{get_user_agent()}",
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; s_v_web_id=verify_lrrjf71j_uVmEAUyT_wXmZ_4zay_AQOP_99FOFoPh6HD6; local_city_cache=%E5%BC%A0%E5%AE%B6%E5%8F%A3; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; msToken=wCav6ZIquffjfxOgjrO6eSOczzA-jBtNXgrrmX90PMrTxBqsa5BXkJvnfLILbQ23xXgfU9iZ5Zr73SytjscJNgtW83Lumm9gJYaj6nW7JA==; _ga_QEHZPBE5HH=GS1.1.1707728786.39.1.1707728798.0.0.0; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1707728799%7C2a71910cb005f4f85c12098297952e938f58fc94448a902f6aad61c8f271d153; tt_scid=Cnk06hFVJDBUejaKugjCGvPxdPbvyd2TVkCFB357Uq-PL2TF-mQCRK7u8XmPtEYi6379",
        "Referer":"https: // www.toutiao.com / c / user / token / MS4wLjABAAAANOQ4JYtxqi3RTMyiasR - H8SCyxjQSrGUGYkMbQbqguu - DkyRAw8D8MMFuczg1MXi /?source = amos_land_page & log_from = 8cb7e6f67ac24_1707102360538"
    }

    cursor=0
    token=get_token(id)
    #print(id,token)
    #测试用例
    #token="MS4wLjABAAAANOQ4JYtxqi3RTMyiasR-H8SCyxjQSrGUGYkMbQbqguu-DkyRAw8D8MMFuczg1MXi"
    params={
        "token":f"{token}" ,
        "cursor": f"{cursor}",
        "count": "20",
        "_signature": "_02B4Z6wo00901kapy8AAAIDB5bR5hRVctQZGjc9AAPRyA0bRXpDaY.LY.qNKKmPB7f0TKgA3o.2ceFueKa5oHtyP-p7-wUj002jGXIlXIvd8ABZ6pym8AS3uy.xHj-fwqNPZLKcHk8UcAyQl24"

    }
    has_more=True
    while has_more:
        #获取信息并解析出下次的cursor（光标，理解为标记）、修改has_more
        res = requests.get(url=url, headers=headers, params=params)
        res.encoding = "utf-8"
        requests.DEFAULT_RETRIES = 5
        if not res:
            print(f"{token}          {res.status_code}")
            return token,None
        re_js=res.json()
        data=re_js["data"]
        if len(data)==0:
            print(f"{token}的粉丝列表显示为Undefined或请求失败或粉丝数为0")
            return token,None
        has_more=data["has_more"]
        cursor=data["cursor"]
        params["cursor"]=cursor
        #接下来解析出粉丝id
        data=data["data"]
        for fan in data:
            user_id=fan["user_id"]
            fans_list.append(user_id)
            #print(user_id)
        time.sleep(random.uniform(0.4,0.5))
        res.close()
        #返回用户的token和其所有粉丝的token

    return token,fans_list


