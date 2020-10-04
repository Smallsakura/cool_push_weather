# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : 163.py.py
@Time    : 2020/10/4 19:32
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import os
import requests
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

spkeys = os.environ['SPKEY'].split('#')


# print("秘钥", spkeys)

# 采集网易云的接口
def get_163_info():
    headers = {
        "authority": "api.uomg.com",
        "path": "/api/comments.163?format = json",
        "scheme": "https",
        "accept": "text / html, application / xhtml + xml, application / xml;    q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
        "accept-encoding": "gzip, deflate, braccept - language: zh - CN, zh;q = 0.9, en;q = 0.8",
        "cache-control": "no - cache",
        "cookie": "Hm_lvt_697a67a1161cac5798b4cf766ef2b3b0 = 1601308892, 1601342651;PHPSESSID = 40p60bvvkj8c3mgfa60dparog1;Hm_lpvt_697a67a1161cac5798b4cf766ef2b3b0 = 1601342664",
        "pragma": "no - cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 80.0.3987.163Safari / 537.36",
    }
    url = "http://api.uomg.com/api/rand.music?sort=%E7%83%AD%E6%AD%8C%E6%A6%9C&format=json"
    data = requests.get(url, headers=headers).json().get('data')
    # print(data)
    # data = json.loads(resp)
    try:
        print('推荐歌曲', data['name'])
        # print(data['picurl'])
        # print(data['url'])
        # import re
        # rid = re.findall(r"=(.*?)", data['url'])[0]
        # print("rid",rid)
        id = data["url"].replace(
            "http://music.163.com/song/media/outer/url?id=", "")
        # print("歌曲id", id,rid)
        # data['avatarurl']
        # msg = "@image=https://xuthus.cc/images/Photo_0411_1a.jpg@" + \
        #     data['content']+"--from "+data['nickname']
        # push(msg.encode("utf-8"))
        # data['msg']="@music=[type=custom,title={},url={},image={}]@".format(data['name'],data['url'],data['picurl'])
        data['music'] = "[CQ:music,type=163,id={}]".format(id)
        info = "夜深了，听完这首歌就睡觉吧！"
        # print(data['msg'])
        for spkey in spkeys:
            # requests.post('https://push.xuthus.cc/send/',spkey, info.encode('utf-8'))
            requests.post('https://push.xuthus.cc/send/' +
                          spkey, (info+data['music']).encode('utf-8'))
        #
        return data
    except Exception as e:
        print(str(e))
        return get_163_info()


# 获取词霸英语
def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    english = eed.json()['content']
    zh_CN = eed.json()['note']
    str = '\n【奇怪的知识】\n' + english + '\n' + zh_CN
    return str


print(get_iciba_everyday())


# 主函数


def main(*args):
    api = 'http://t.weather.itboy.net/api/weather/city/'  # API地址，必须配合城市代码使用
    city_code = '101200901'  # 进入https://where.heweather.com/index.html查询你的城市代码
    tqurl = api + city_code
    response = requests.get(tqurl)
    d = response.json()  # 将数据以json形式返回，这个d就是返回的json数据
    if (d['status'] == 200):  # 当返回状态码为200，输出天气状况
        print("城市：", d["cityInfo"]["parent"], d["cityInfo"]["city"])
        print("更新时间：", d["time"])
        weather_list = d["data"]["forecast"]
        time_api = "http://quan.suning.com/getSysTime.do"
        time_data = requests.get(time_api).json()['sysTime2']
        # print(time_data)
        import datetime
        next_day = (datetime.datetime.strptime(
            time_data, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(1))
        print("明天是", next_day)
        next_day = datetime.datetime.strftime(next_day, "%Y-%m-%d")
        print(next_day)
        p = 0
        for i in range(len(weather_list)):
            if weather_list[i]['ymd'] == next_day:
                p = i
        print("日期：", d["data"]["forecast"][p]["ymd"])
        print("星期：", d["data"]["forecast"][p]["week"])
        print("天气：", d["data"]["forecast"][p]["type"])
        print("温度：", d["data"]["forecast"][p]["high"],
              d["data"]["forecast"][p]["low"])
        print("湿度：", d["data"]["shidu"])
        print("PM25:", d["data"]["pm25"])
        print("PM10:", d["data"]["pm10"])
        print("空气质量：", d["data"]["quality"])
        print("风力风向：", d["data"]["forecast"][p]
              ["fx"], d["data"]["forecast"][p]["fl"])
        print("感冒指数：", d["data"]["ganmao"])
        print("温馨提示：", d["data"]["forecast"][p]["notice"], "。")
        for spkey in spkeys:
            cpurl = 'https://push.xuthus.cc/send/' + \
                spkey  # 自己改发送方式，我专门创建了个群来收消息，所以我用的group
            tdwt = '【明日份天气】\n城市：' + d['cityInfo']['parent'] + ' ' + d['cityInfo']['city'] + '\n日期：' + \
                   d["data"]["forecast"][p]["ymd"] + ' ' + d["data"]["forecast"][p]["week"] + '\n天气：' + \
                   d["data"]["forecast"][p]["type"] + '\n温度：' + d["data"]["forecast"][p]["high"] + ' ' + \
                   d["data"]["forecast"][p]["low"] + '\n湿度：' + \
                   d["data"]["shidu"] + '\n空气质量：' + d["data"]["quality"] + '\n风力风向：' + d["data"]["forecast"][p][
                       "fx"] + ' ' + d["data"]["forecast"][p]["fl"] + '\n温馨提示：' + \
                   d["data"]["forecast"][p]["notice"] + '。\n[更新时间：' + d["time"] + ']\n✁-----------------' + \
                   get_iciba_everyday().rstrip()  # 天气提示内容，基本上该有的都做好了，如果要添加信息可以看上面的print，我感觉有用的我都弄进来了。

            requests.post(cpurl,
                          tdwt.encode('utf-8'))  # 把天气数据转换成UTF-8格式，不然要报错。
            # 发送音乐
        get_163_info()
    else:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务状态！'
        requests.post('https://push.xuthus.cc/send/' +
                      spkeys[0], error.encode('utf-8'))


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
