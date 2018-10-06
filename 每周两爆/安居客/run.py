"""
Author: Lengyue
Date: 2018-10-06
Project: Crack Anjuke-AntiSpider
https://www.anjuke.com/captcha-verify/?callback=shield&from=antispam
"""

import requests
import re
import time
import json
import execjs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}

# Step 1, Get sessionId
response = requests.get(
    "https://www.anjuke.com/captcha-verify/?callback=shield&from=antispam",
    headers=headers
)
sessionId = re.findall(r"sessionId' : '(.*?)'", response.text)[0]
print("sessionId", sessionId)

# Step 2, Get captcha
response = requests.get(
    "https://verifycode.58.com/captcha/getV3",
    headers=headers,
    params={
        "callback": "callback",
        "showType": "embed",
        "sessionId": sessionId,
        "_": str(int(time.time() * 1000))
    }
)
captchaData = json.loads(response.text.replace("callback(", "").replace(")", ""))
responseId = captchaData["data"]["responseId"]
bgImgUrl = captchaData["data"]["bgImgUrl"]
print("responseId", responseId)
print("AESKey", responseId[0:16])
print("bgImgUrl", bgImgUrl)

# Step 3, Get Image
response = requests.get(
    "https://verifycode.58.com" + bgImgUrl,
    headers=headers
)
open("./demo.jpg", "wb").write(response.content)
print("Downloaded Image, size %i" % len(response.content))
coordinateX = int(input("请输入 x 坐标: "))

# Step 4, Get FP
response = requests.get(
    "https://cdata.58.com/fpToken",
    headers=headers,
    params={
        "callback": "callback",
    }
)
fpData = json.loads(response.text.replace("callback(", "").replace(")", ""))
fpToken = fpData["token"]
print("fpToken", fpToken)

# Step 5, Calculate answer

traceData = ""  # 请载入自己的轨迹算法

# Test Data
# responseId = "5c74b40858b24e188f3a32db84542be1"
# sessionId = "a1078b548b5b4dd19eae7dc68887ca78"
# coordinateX = 155
# traceData = "38,37,1|39,37,38|46,35,52|64,33,69|88,33,86|114,33,102|138,33,119|153,33,138|166,33,152|"

jsCode = execjs.compile(open("./anjuke.js", "r").read())
answerData = jsCode.call("getSlideAnswer", responseId, fpToken, coordinateX, traceData)
print("answerData", answerData)

# Step 6, Request
response = requests.get(
    "https://verifycode.58.com/captcha/checkV3",
    headers=headers,
    params={
        "callback": "callback",
        "data": answerData,
        "responseId": responseId,
        "sessionId": sessionId,
        "_": str(int(time.time() * 1000))
    }
)
print(response.text)
