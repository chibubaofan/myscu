
import requests
from Url_manager import Url_manager_hotboard
import Content_gainer
"""
用于获取热榜上的时间的
"""
def get_hot_board_content():
    url = "https://www.toutiao.com/hot-event/hot-board/"
    headers = {
        "Refer": "https://www.toutiao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Cookie": "__ac_signature=_02B4Z6wo00f019U9NBgAAIDAoxLpVKFk-ufVGTCAAJEIz5UsiB0mSToK5TvgxebtV09eaMAg6pdWCkQMuyXy3IRcEzSoQb1K5rwChmRGvmVz5RlFaWIkZY93qdjEo3BbvlgPU1Vy5KLKlTlq0b; tt_webid=7312031009742341670; _ga=GA1.1.729102522.1706085777; s_v_web_id=verify_lrrjf71j_uVmEAUyT_wXmZ_4zay_AQOP_99FOFoPh6HD6; local_city_cache=%E5%BC%A0%E5%AE%B6%E5%8F%A3; csrftoken=ac3eaea1112744e4cc7f98d9ed57826d; _S_DPR=2; _S_IPAD=0; _S_WIN_WH=1232_678; notRedShot=1; msToken=wIgrj7jvT2n4E6yY-unztgSTENh9eed0-SX8wzGl3r1pSyiHbAuAS4c7YjV782IO22TXwIrDTkZ7g-4mCTmEVEJ5SoM8BqgwzSkeP0-A; ttwid=1%7CjCLqkL7Nj1vXvfx_tukcUqTutLwFB5XjFfcAuSf6mBo%7C1706873690%7C37b652ef73443b56fe9b7ec82ddc5dab945bfc50134e74da1da032ba4050ff7a; tt_scid=ikF33G0SKY.bHjo8peX1iVKfq5fsk2TpgRA1mnk6O-IYZ2CYKD.CqcLsz48ihpHo51d7; _ga_QEHZPBE5HH=GS1.1.1706873267.15.1.1706873705.0.0.0"
    }
    params = {
        "origin": "toutiao_pc",
        "_signature": "_02B4Z6wo00f0121wDRQAAIDAzm2.UF3hyX9tVAmAAL7st43UCCwNoV-auVRrmgXxDa-GXm7tDiZ7tGKvpVFqrtMiU3nbj2x1Rc4bp6qAoFim5XKANU.DuvgvCobTkly.XtCQWFlqrJlsJJIIf1"
    }
    re = requests.get(url=url, headers=headers, params=params)
    re.encoding = "utf-8"
    re_js = re.json()
    total_data = re_js["data"]
    count = 0
    url_manager = Url_manager_hotboard()
    # 将获得的热榜url传给Url_manager获得id
    for data in total_data:
        if data["Url"]:
            url_manager.add_url(data["Url"])
    # 处理url获得id
    url_manager.handle_url()
    id_list = url_manager.get_id_list()
    # 得到id列表之后开始爬评论
    for id in id_list:
        Content_gainer.get_content(group_id=id, item_id=id)

