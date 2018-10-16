"""
没周两爆 - 数美滑动破解
样例网站
作者 冷月 https://www.6.cn/
日期 2018-10-16
"""
import requests
import json


# 初始化环境
session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/69.0.3497.81 Safari/537.36"
}


# 获取验证码
response = session.get(
    "https://captcha.fengkongcloud.com/ca/v1/register",
    params={
        "organization": "TKWQ4vmgC3PJLGDTMIoJ",
        "appId": "default",
        "channel": "DEFAULT",
        "lang": "zh-cn",
        "model": "slide",
        "rversion": "1.0.1",
        "data": "{}",
        "callback": "sm_1539652688401"
    }
)
init_data = json.loads(response.text.replace("sm_1539652688401(", "").replace(")", ""))
data = session.get("https://castatic.fengkongcloud.com" + init_data["detail"]["bg"]).content
open("./current.jpg", "wb").write(data)

# 计算加密结果
act = requests.post(
    "https://lengyue.me/api/execute.php?type=shumei",
    data={
        "eval": 'window.shumei(%s, %i)' % (json.dumps(init_data), (int(input("请输入距离: ")) - 10) / 2)
    }
)

# 获取验证结果
response = session.get(
    "https://captcha.fengkongcloud.com/ca/v1/fverify",
    params={
        "organization": "TKWQ4vmgC3PJLGDTMIoJ",
        "appId": "default",
        "channel": "DEFAULT",
        "lang": "zh-cn",
        "rid": init_data["detail"]["rid"],
        "act": act,
        "callback": "sm_1539652810662",
    }
)
print(response.text.replace("sm_1539652810662(", "").replace(")", ""))
