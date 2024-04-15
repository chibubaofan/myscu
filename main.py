from get_hot_board import get_hot_board_content
from User_attribute_gainer import get_all_user_fans_stat
from User_fans_gainer import  get_all_user_fans
from Content_gainer import get_content
from get_user_info import get_user_info
import os
import csv
import time
import re
import random
import requests

# #获取评论用：
# get_hot_board_content()
# #获取主页三个属性用：
# get_all_user_fans_stat()
# #获取粉丝列表用：
# #get_all_user_fans()
def Write(user_info_list,id):
    newline = ""
    with open(f".\\userstwo\\userid_with_info\\{id}.csv", mode="a+", encoding="utf-8", newline=newline) as f:
        writer = csv.writer(f)
        for i in user_info_list:
            writer.writerow(i)

#7351579443392938548,7351674237813637673,7351627318885892647,7351570656149897764,7351448327684260362,7351418705282515519,7351400441252758026
# list=['1789613453053952',"7351579443392938548",'7351674237813637673','7351627318885892647','7351570656149897764','7351448327684260362','7351418705282515519','7351400441252758026']
# for num in list:
#     get_content(num,num)


base_dir = ".\\userstwo\\userid"
files = [os.path.join(base_dir, file) for file in os.listdir(base_dir)]
# 得到文件路径后对每一个文件进行读取、获取属性，写入的操作



for file in files:
    try:

        print(f"正在处理{file}")
        index = 0
        usercount = 0
        time1 = time.time()

        # 解析出读取文件的id
        id = file.split("\\")[3]
        id = re.search("\d+", id).group()
        target = f".\\userstwo\\userid_with_info_index\\{id}.csv"


        if os.path.exists(target):
           with open(target,mode='r')as f:
               index=int(f.read())

        # 设置一个列表用于装填属性方便后续写入
        user_id_list = []
        user_info_list = []
        # 读操作:占用大量时间，应该用协程来做，奈何我太菜
        with open(file, mode="r") as f:
            reader = csv.reader(f)
            for row in reader:
                # 读取一行-获得属性-保存至list
                user_id_list.append(row[0])
        user_id_list=user_id_list[index:]
        for user_id in user_id_list:
            user_info = get_user_info(user_id)
            if user_info==None:
                user_info=""
            usercount += 1
            print(usercount)
            user_info_list.append(user_info)
            time.sleep(random.uniform(0, 0.1))
            if usercount % 100== 0 or user_id==user_id_list[-1]:
                Write(user_info_list,id)
                user_info_list.clear()
        time2 = time.time()
        timeused = time2 - time1
        print(f"finish userid_with_fans_stat{id}.csv  共用时{timeused / 60}分钟")
    except KeyError as ex:
        print("KeyError:"+ex.__str__()+str(ex.__traceback__))
    except TypeError as ex:
        print("TypeError:"+ex.__str__()+str(ex.__traceback__))
    except requests.exceptions.JSONDecodeError as ex:
        print("JSONDecodeError:"+ex.__str__()+str(ex.__traceback__))
    finally:
        used=time.time()
        used-=time1
        used/=60
        print(used)
        Write(user_info_list,id)
        file=f".\\userstwo\\userid_with_info_index\\{id}.csv"
        with open(file,mode="w")as f:
            num=usercount+index
            f.write(str(num))


