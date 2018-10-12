import requests
import execjs
import json
import time
import trace
import random
import os
from img_locate import ImgProcess


def crack(gt, challenge, referer):
    headers = {
        "Referer": referer,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53"
                      "7.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    }

    # 获取初始化数据
    uri = "gt=" + gt + \
          "&challenge=" + challenge + \
          "&width=100%&product=float&offline=false&protocol=https://&voice=/static/js/voice.1.1.3.js" \
          "&type=slide&pencil=/static/js/pencil.1.0.1.js&path=/static/js/geetest.6.0.9.js&callback=geetest"
    response = requests.get(
        "https://api.geetest.com/get.php?" + uri,
        headers=headers,
    )
    initData = json.loads(response.text.replace("geetest(", "")[:-1])
    # print("initData", initData)

    # 下载图片
    fullbg = str(time.time()) + str(random.random())
    bg = str(time.time()) + str(random.random())
    open("Image/" + fullbg + ".jpg", "wb").write(
        requests.get("https://static.geetest.com/" + initData["fullbg"]).content)
    open("Image/" + bg + ".jpg", "wb").write(requests.get("https://static.geetest.com/" + initData["bg"]).content)

    # 图片处理
    # 代码改自 OSinoooO/bilibili_geetest
    img_process = ImgProcess()
    img1 = img_process.get_merge_image('Image/' + fullbg + '.jpg')
    img2 = img_process.get_merge_image('Image/' + bg + '.jpg')
    os.remove("Image/" + fullbg + ".jpg")
    os.remove("Image/" + bg + ".jpg")
    distance = int(img_process.get_gap(img1, img2) - 7)
    initData = json.dumps(initData)

    # 采用垃圾算法获取轨迹 建议重写
    track = json.dumps(trace.get_trace_fast(distance))
    # track = input("%i track " % distance)
    # print("Track", track)
    time.sleep(1)

    _js = execjs.compile(open("./js/geetest.js").read())
    params = json.loads(_js.call("get_slide_w", initData, track, distance))
    params.update({
        "callback": "geetest"
    })
    response = requests.get(
        "https://api.geetest.com/ajax.php",
        headers=headers,
        params=params
    )
    # print(response.text)
    return json.loads(response.text.replace("geetest(", "")[:-1])
