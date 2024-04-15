import json
import time
import random
import requests
from bs4 import BeautifulSoup
from User_attribute_gainer import get_user_fans_stat

class user():

    def __init__(self, id1=None):
        self.id1 = id1
        self.id2 = None
        self.all_num = 0
        self.ori_num = 0
        self.withInter_num = 0
        self.video_num = 0
        self.weitoutiao_num = 0
        self.wenda_num = 0
        self.litVideo_num = 0
        self.hot_num = 0
        self.has_col=0
        self.name=None
        self.desc=None
        self.auth=None
        self.article=0

    def set(self, num):
        self.all_num = num['all_num']
        self.ori_num = num['ori_num']
        self.withInter_num = num['withInter_num']
        self.litVideo_num = num['litVideo_num']
        self.wenda_num = num['wenda_num']
        self.weitoutiao_num = num['weitoutiao_num']
        self.video_num = num['video_num']
        self.hot_num = num['hot_num']
        self.has_col=num['has_col']
        self.article=num['article']
        if num['name']!=None:
            self.name = num['name']
            self.desc = num['desc']
            self.auth = num['auth']


    def set_id1(self, id1):
        self.id1 = id1

    def set_id2(self, id2):
        self.id2 = id2

    def set_name(self, name):
        self.name = name

    def get_tostring(self):
        ori_propor = None
        inter_propor = None
        hot_propor=None
        if (self.all_num != 0):
            ori_propor = self.ori_num / self.all_num
            inter_propor = self.withInter_num / self.all_num
            hot_propor=self.hot_num/self.all_num

        dict = set()
        dict = {
            '名字':self.name,
            '简介':self.desc,
            '认证':self.auth,
            'id1': self.id1,
            'id2': self.id2,
            '全部发布数': self.all_num,
            '原创发布数': self.ori_num,
            '有互动的数量': self.withInter_num,
            '文章数量':self.article,
            '视频数量': self.video_num,
            '小视频数量': self.litVideo_num,
            '微头条数量': self.weitoutiao_num,
            '问答数量': self.wenda_num,
            '原创比例': ori_propor,
            '互动比例': inter_propor,
            'hot数量' :  self.hot_num,
            'hot比例' : hot_propor,
            '是否有合集':self.has_col

        }
        return dict


def get_token(id):
    time.sleep(random.uniform(0.1, 0.2))
    token = ""  # 首先要获得token，_signature可以勤更换
    url = f"https://www.toutiao.com/c/user/{id}/"
    headers = {
        "Connection": "close",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; s_v_web_id=verify_lrrjf71j_uVmEAUyT_wXmZ_4zay_AQOP_99FOFoPh6HD6; local_city_cache=%E5%BC%A0%E5%AE%B6%E5%8F%A3; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; msToken=wCav6ZIquffjfxOgjrO6eSOczzA-jBtNXgrrmX90PMrTxBqsa5BXkJvnfLILbQ23xXgfU9iZ5Zr73SytjscJNgtW83Lumm9gJYaj6nW7JA==; _ga_QEHZPBE5HH=GS1.1.1707728786.39.1.1707729284.0.0.0; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1707729285%7C2f84f2a03328dc72b1727c66af4618dd7ded0d83abadde06ff0f9559d88e9c33; tt_scid=zi6lIT2ZyDwud-I0U06-4xqwrIdsNwKmnJODCIU6yvyyEKG0xmDzPewognOB2O.D85c0"
    }
    params = {
        "source": "amos_land_page"
    }
    res = requests.get(url=url, headers=headers, params=params)
    location = res.url
    # 此处得到了token
    token = location.split("/")
    if len(token) < 7:
        print("获取的token不正确  返回None")
        return None
    token = token[6]
    res.close()
    return token


def get_tabs_info(token):
    url = 'https://www.toutiao.com/api/pc/user/tabs_info'
    headers = {
        'Cookie': '__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; s_v_web_id=verify_lrrjf71j_uVmEAUyT_wXmZ_4zay_AQOP_99FOFoPh6HD6; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; passport_csrf_token=6b0c674f949ca315dfdefa5126088f37; passport_csrf_token_default=6b0c674f949ca315dfdefa5126088f37; local_city_cache=%E6%88%90%E9%83%BD; msToken=eIYyZPb4N-7j8VTY88Og8LBF4JWmPPvQijY7rTyAbtgpVJknqL_rzmo0u-fOa9yByVY1wYfgcHXNlV_8ULj1gNo8JZ2LbEyLAQVZyklb; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1711203140%7C7147f8a2bc31845823f26b66541d67ae099ef0260b1009915d659105d163ce50; tt_scid=h.QoihvTw-zmFJY4HqRxdZxv6KlIygTSVhwKbFR.BR0e7feQ0h-LtqNOesLN0XWSea6a; _ga_QEHZPBE5HH=GS1.1.1711202135.45.1.1711203280.0.0.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }
    data = {
        '_signature': '_02B4Z6wo00f01.ZzyagAAIDAgFwU5DPh8ef2V80AAJhriYT7ul2eoiAT0BRWjarFGVyNdclt1QRbM3FBDtPQ72jmTK86xT82hzp5e-qHlYps9RMUTKLPxUSl3mjVCRMHmxqvyrRU5NGIGaIne9',
        'token': f'{token}'
    }
    req = requests.post(url=url, headers=headers, data=data,timeout=5)
    jsd = req.json()
    req.close()
    return jsd


"""
{show_name: "视频", category: "pc_profile_video"}
{show_name: "微头条", category: "pc_profile_ugc"}
{show_name: "问答", category: "profile_wenda"}
{show_name: "小视频", category: "pc_profile_short_video"}
            '全部发布数':self.all_num,
            '原创发布数':self.ori_num,
            '有互动的数量':self.withInter_num,
            '视频数量':self.video_num,
            '小视频数量':self.litVideo_num,
            '微头条数量':self.weitoutiao_num,
            '问答数量':self.wenda_num,
            '原创比例':ori_propor,
            '互动比例':inter_propor
"""


def get_num(option, token):  # 用来获取用户发布数量的函数
    article=0
    has_get_info=False
    all_num = 0
    ori_num = 0
    withInter_num = 0
    video_num = 0
    litVideo_num = 0
    weitoutiao_num = 0
    wenda_num = 0
    hot_num = 0
    has_col=0
    name=None
    desc=None
    auth=None
    for title in option:
        if title['show_name'] == '合集':
            has_col=1
        sub_num = get_num_sub(title, token,has_get_info)

        all_num += sub_num['all']
        ori_num += sub_num['ori']
        withInter_num += sub_num['inter']
        hot_num += sub_num['hot']
        if has_get_info==False:
           desc=sub_num['desc']
           name=sub_num['name']
           auth=sub_num['auth']
        if name!=None:
            has_get_info=True
        if title['show_name'] == '视频':
            video_num = sub_num['all']
        elif title['show_name'] == '微头条':
            weitoutiao_num = sub_num['all']
        elif title['show_name'] == '问答':
            wenda_num = sub_num['all']
        elif title['show_name'] == '小视频':
            litVideo_num = sub_num['all']
        elif title['show_name'] == '文章':
            article=sub_num['all']
        else:
            print("获取的目录有误或者有了新的目录出现")

    num = {
        "all_num": all_num,
        "ori_num": ori_num,
        "withInter_num": withInter_num,
        "video_num": video_num,
        "litVideo_num": litVideo_num,
        "weitoutiao_num": weitoutiao_num,
        "wenda_num": wenda_num,
        'hot_num': hot_num,
        'has_col':has_col,
        'name':name,
        'desc':desc,
        'auth':auth,
        'article':article
    }

    return num


def get_num_sub(title, token,has_get_info):
    keyError_num=0
    # 首先设置参数
    t=time.time()
    all_num = 0
    ori_num = 0
    with_inter_num = 0
    hot_num = 0
    desc=None
    name=None
    auth=None
    has_more = True
    url = "https://www.toutiao.com/api/pc/list/user/feed"
    headers = {
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; notRedShot=1; _S_WIN_WH=1232_678; passport_csrf_token=6b0c674f949ca315dfdefa5126088f37; passport_csrf_token_default=6b0c674f949ca315dfdefa5126088f37; local_city_cache=%E6%88%90%E9%83%BD; msToken=jQ7CZDkPl75rzrsKcGyX9PXaWNhFy-kyta2US8ee4CSSOlSdl-C2vV8dggVxRHbP_6dVrAlBFltL2tkiMhTg9wmYRa9tiUS7ejBaqPyV; s_v_web_id=verify_lu6kgezg_NHthdRZy_GIoV_4y1H_9PRU_ceS1E9vlM9tD; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1711348098%7Ce42f1d4d9abc34277ccb9623bcbcc7b8ab25cf1597c38d8fca7ebe7fedc9147a; tt_scid=nFVDVtEfEMdh9wzT6u2-585mO59wIUYw4YutGhlD2csqaE17OB5tYDF8dvYC-g5Ja183; _ga_QEHZPBE5HH=GS1.1.1711348071.46.1.1711348203.0.0.0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Referer": f"https://www.toutiao.com/c/user/token/{token}/?source=amos_land_page&log_from=26d438a0184d7_1710685501945&tab=al"
    }
    params = {
        'hot_video':0,
        "category": f"{title['category']}",
        "max_behot_time": 0,
        "aid": "24",
        "app_name": "toutiao_web",
        "token": f"{token}",
        "_signature": "_02B4Z6wo00d01qw.ihwAAIDB2hBXURBJiUqsG46AAM0bLVOdeN9uZdh-L0iVQxEJPhGyDT5we4v6DAqmCeFhVNRW567agGnKWfzatEKZpIn9NKSHqEdaRo.SVt9SSO0t6AQYgOa6HX1dTakK02"
    }
    while has_more is True:

        if keyError_num>=20:
            print("等待网络稳定")
            time.sleep(20)
            break
        time.sleep(random.uniform(0.5, 0.6))
        js_data=None
        data=None
        while True:
            res = requests.get(url=url, headers=headers, params=params,timeout=5)
            if res==None:
                time.sleep(random.uniform(2,3))
                continue
            try:
                js_data = res.json()
            except requests.exceptions.JSONDecodeError as ex:
                nt=time.time()
                print("碰到了空的option")
                has_more=False
                res.close()
                subnum = {
                    'all': 0,
                    'ori': 0,
                    'inter': 0,
                    'hot': 0,
                    'desc': None,
                    'auth': None,
                    'name': None
                }
                return subnum


            data = js_data['data']  # 得到用户数据
            if data == None :
                if title['show_name'] == '合集':
                    data=[]
                    has_more=js_data['has_more']
                    max_behot_time=js_data['next']['max_behot_time']
                    params['max_behot_time'] = max_behot_time
                    break
                time.sleep(random.uniform(2, 3))
                continue
            break


        max_behot_time = js_data['next']['max_behot_time']
        has_more = js_data['has_more']
        params['max_behot_time'] = max_behot_time  # 每次更新内容


        length=len(data)
        all_num += length# 所有的数量
        """
        burycount:反感数0.4
        commentcount:评论数0.2
        diggcount:点赞数0.1
        forwardcount:转发数0.3
        readcount:播放量0.001
        repincount:收藏数0.3
        sharecount:分享数0.3
        """
        if title['show_name'] == '视频' or title['show_name'] == '小视频'or title['show_name'] == '文章':
            ori_num+=length
        for dataitem in data:

            if title['show_name'] == '视频':
                if has_get_info == False:
                    user_info = dataitem['user']
                    user_info=user_info['info']
                    name = user_info['name']
                    desc = user_info['desc']
                    auth=''
                    if "verified_content" in user_info:
                        auth = user_info['verified_content']
                    has_get_info = True
                it_c=set()
                buryCount = 0
                commentCount =0
                diggCount = 0
                forwardCount = 0
                readCount = 0
                repinCount = 0
                shareCount =0
                showCount = 0
                try:
                    it_c = dataitem['itemCell']['itemCounter']
                    if 'buryCount' in it_c:
                        buryCount = it_c['buryCount']
                    commentCount = it_c['commentCount']
                    diggCount = it_c['diggCount']
                    forwardCount = it_c['forwardCount']
                    readCount = it_c['readCount']
                    repinCount = it_c['repinCount']
                    shareCount = it_c['shareCount']
                    showCount = it_c['showCount']
                except KeyError as ex:
                    print("keyError" + ex.__str__())
                    keyError_num+=1
                    continue

                standard=buryCount*0.4+commentCount*0.2+diggCount*0.1+forwardCount*0.3+readCount*0.01+repinCount*0.3+shareCount*0.3+showCount*0.0001
                if standard>=0.6:
                    with_inter_num+=1
                if standard>=2.7:
                    hot_num+=1


            elif title['show_name'] == '微头条':
                it_c=set()
                if has_get_info==False:
                    user_info=dataitem['user']
                    desc=user_info['desc']
                    name=user_info['name']
                    auth = ''
                    if "verified_content" in user_info:
                        auth = user_info['verified_content']
                    has_get_info=True

                buryCount = 0
                commentCount =0
                diggCount = 0
                forwardCount =0
                fansReadCount=0
                readCount = 0
                repinCount = 0
                shareCount = 0
                showCount=0
                try:
                    it_c = dataitem['itemCell']['itemCounter']
                    if 'buryCount' in it_c:
                        buryCount = it_c['buryCount']
                    commentCount = it_c['commentCount']
                    diggCount = it_c['diggCount']
                    forwardCount = it_c['forwardCount']
                    fansReadCount = it_c['fansReadCount']
                    readCount = it_c['readCount']
                    repinCount = it_c['repinCount']
                    shareCount = it_c['shareCount']
                    showCount = it_c['showCount']
                except KeyError as ex:
                    print("keyError" + ex.__str__())
                    keyError_num+=1
                    continue

                standard = buryCount * 0.4 + commentCount * 0.2 + diggCount * 0.1 + forwardCount * 0.3 + readCount * 0.01 + repinCount * 0.3 + shareCount * 0.3+showCount*0.0001+fansReadCount*0.01
                if standard >= 0.6:
                    with_inter_num += 1
                if standard >= 2.7:
                    hot_num += 1
                if 'extra' not in dataitem:
                    ori_num+=1
            elif title['show_name'] == '问答':

                if 'itemCell' in dataitem:

                    readCount=0
                    showCount=0
                    try:
                        it_c = dataitem['itemCell']['itemCounter']
                        readCount = it_c['readCount']
                        showCount = it_c['showCount']
                    except KeyError as ex:
                        print("keyError"+ex.__str__())
                        keyError_num+=1
                        continue

                    standard=readCount*0.1+showCount*0.001
                    if standard>=1:
                        with_inter_num+=1
                else:
                    buryCount=0
                    ori_num+=1

                    buryCount = dataitem['bury_count']
                    commentCount=dataitem['comment_count']
                    repinCount=dataitem['repin_count']
                    standard=buryCount*0.3+commentCount*0.2*repinCount*0.5
                    if standard>=0.4:
                        with_inter_num+=1
                    if standard>=2:
                        hot_num+=1


            elif title['show_name'] == '小视频':
                if has_get_info == False:
                    user_info = dataitem['user']['info']
                    name = user_info['name']
                    desc = user_info['desc']
                    auth = ''
                    if "verified_content" in user_info:
                        auth = user_info['verified_content']
                    has_get_info = True
                it_c = set()
                buryCount = 0
                commentCount = 0
                diggCount = 0
                forwardCount = 0
                readCount = 0
                repinCount = 0
                shareCount = 0
                showCount = 0
                try:
                    it_c = dataitem['itemCell']['itemCounter']
                    if 'buryCount' in it_c:
                        buryCount = it_c['buryCount']
                    commentCount = it_c['commentCount']
                    diggCount = it_c['diggCount']
                    forwardCount = it_c['forwardCount']
                    readCount = it_c['readCount']
                    repinCount = it_c['repinCount']
                    shareCount = it_c['shareCount']
                    showCount = it_c['showCount']
                except KeyError as ex:
                    print("keyError" + ex.__str__())
                    keyError_num+=1
                    continue
                # for key in it_c.keys():
                #     print(key)

                standard = buryCount * 0.4 + commentCount * 0.2 + diggCount * 0.1 + forwardCount * 0.3 + readCount * 0.01 + repinCount * 0.3 + shareCount * 0.3 + showCount * 0.0001
                if standard >= 0.6:
                    with_inter_num += 1
                if standard >= 2.7:
                    hot_num += 1
            elif title['show_name'] == '文章':
                if has_get_info == False:
                    user_info = dataitem['user_info']
                    name = user_info['name']
                    desc = user_info['description']
                    auth = ''
                    if "verified_content" in user_info:
                        auth = user_info['verified_content']
                    has_get_info = True
                it_c = set()
                buryCount = 0
                commentCount = 0
                diggCount =0
                forwardCount = 0
                readCount = 0
                repinCount = 0
                shareCount = 0
                showCount = 0
                try:
                    it_c = dataitem['itemCell']['itemCounter']
                    if 'buryCount' in it_c:
                        buryCount = it_c['buryCount']
                    commentCount = it_c['commentCount']
                    diggCount = it_c['diggCount']
                    forwardCount = it_c['forwardCount']
                    readCount = it_c['readCount']
                    repinCount = it_c['repinCount']
                    shareCount = it_c['shareCount']
                    showCount = it_c['showCount']
                except KeyError as ex:
                    print("keyError" + ex.__str__())
                    keyError_num+=1
                    continue



                standard = buryCount * 0.4 + commentCount * 0.2 + diggCount * 0.1 + forwardCount * 0.3 + readCount * 0.01 + repinCount * 0.3 + shareCount * 0.3 + showCount * 0.0001
                if standard >= 0.6:
                    with_inter_num += 1
                if standard >= 2.7:
                    hot_num += 1
            else:
                print("获取的目录有误或者该用户有合集")
        res.close()

    subnum = {
        'all': all_num,
        'ori': ori_num,
        'inter': with_inter_num,
        'hot': hot_num,
        'desc':desc,
        'auth':auth,
        'name':name
    }
    return subnum


def get_user_info(id):
    print("id:"+id)
    userexam = user(id)  # 初始化并设置id1
    token = get_token(id)
    if token==None:
        return None
    userexam.set_id2(token)  # 设置id2

    jsd = get_tabs_info(token)


    option = jsd['data'][1:]
    num=None

    num = get_num(option, token)

    userexam.set(num)
    dict=userexam.get_tostring()
    list2=get_user_fans_stat(id)
    time.sleep(random.uniform(0.2,0.3))
    dict.update({'获赞数':list2[0],'粉丝数':list2[1],'关注数':list2[2]})
    if dict['名字']!=None:
        dict['名字']=dict['名字'].replace("\n","")
    if dict['简介']!=None:
        dict['简介']=dict['简介'].replace("\n","")
    l=list(dict.values())
    print(l)
    return l
if __name__ == '__main__':

    print(get_user_info('87993682070'))

