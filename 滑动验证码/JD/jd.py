import requests
import json
import base64
import io
import os
import execjs
import re
import time
from hashlib import md5
from PIL import Image


#  初始化JD数据库
def calculate_hash(img):
    pix = img.load()
    hash_string = ""
    for y in range(img.size[1]):
        hash_string += str(pix[0, y])
    return md5(hash_string.encode()).hexdigest()


db_data = {}
for (dir_path, dir_names, file_names) in os.walk("./img_db"):
    for file_name in file_names:
        img = Image.open("./img_db/" + file_name).convert("RGB")
        db_data[calculate_hash(img)] = img


class JDSlide:
    def __init__(self, eid):
        self.__eid = eid

    def slide(self):
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/69.0.3497.81 Safari/537.36"
        }
        # 获取滑动
        response = session.get(
            "https://iv.jd.com/slide/g.html?appId=1604ebb2287&scene=login&"
            "product=click-bind-suspend&e=%s&callback=jsonp_0682216393529359" % self.__eid
        )
        init_data = json.loads(response.text.replace("jsonp_0682216393529359(", "").replace(")", ""))
        print("初始化数据", init_data)

        # 图像定位
        img_data = base64.b64decode(init_data["bg"])
        current_img = Image.open(io.BytesIO(img_data)).convert("RGB")
        img_hash = calculate_hash(current_img)
        print("图片指纹", img_hash)
        base_img = db_data[img_hash]
        base_pix = base_img.load()
        current_pix = current_img.load()
        distance = None
        for x in range(base_img.size[0]):
            r1, g1, b1 = current_pix[x, init_data["y"] + 20]
            r2, g2, b2 = base_pix[x, init_data["y"] + 20]
            if abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2) > 50:
                distance = x
                break
        print("X坐标", distance)
        # current_img.save("./sss.jpg")

        if not distance:
            print("图片定位失败")
            return

        # 获取 _jdtdmap_sessionId
        response = session.get(
            "https://seq.jd.com/jseqf.html?bizId=passport_jd_com_login_pc&platform=js&version=1"
        )
        _jdtdmap_sessionId = re.findall(r'_jdtdmap_sessionId="(.*?)"', response.text)[0]
        print("_jdtdmap_sessionId", _jdtdmap_sessionId)

        time.sleep(2)  # 非常关键
        
        # 在线执行 看心情关闭 你懂我意思吧
        encrypted_trace = requests.post("https://lengyue.me/api/execute.php?type=jdSlide", data={
            "eval": "getJD(%i)" % (distance / 360 * 278)
        }).json()
        
        # 最终请求
        params = {
            "d": encrypted_trace["ans"],
            "c": init_data["challenge"],
            "w": 278,
            "appId": "1604ebb2287",
            "scene": "login",
            "product": "click-bind-suspend",
            "e": self.__eid,
            "s": _jdtdmap_sessionId,
            "callback": "jsonp_042151781690389"
        }
        response = session.get(
            "https://iv.jd.com/slide/s.html",
            params=params
        )
        answer_data = json.loads(response.text.replace("jsonp_042151781690389(", "").replace(")", ""))
        if "validate" not in answer_data.keys():
            print("识别失败", answer_data["message"])
            return
        answer = {
            "validate": answer_data["validate"],
            "challenge": init_data["challenge"],
        }
        print("结果", answer)
        return answer
