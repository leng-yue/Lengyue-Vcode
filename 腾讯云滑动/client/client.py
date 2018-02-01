# tencent.py
# Author : Lengyue
import requests
import random
import re
import hashlib
import os
from PIL import Image, ImageChops
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64
from flask import Flask, request
api = "http://127.0.0.1:5000/parse"

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


app = Flask(__name__)

class VerifyCode:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    def __init__(self, proxies):
        self.proxies = proxies

    # js 的 CDATA
    def GetCdata(self):
        arr = self.chlg
        for i in range(int(arr['M'])):
            if hashlib.md5((arr["randstr"] + str(i)).encode()).hexdigest() == arr["ans"]:
                self.cdata = i
                return 0
        self.cdata = 0
        return 0

    # 下载图片
    def GetImg(self, index):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Referer": "https://ssl.captcha.qq.com/cap_union_new_show"
        }
        params = {
            "aid": "2000000020",
            "captype": "7",
            "protocol": "https",
            "clientype": "1",
            "disturblevel": "1",
            "apptype": "",
            "noheader": "1",
            "color": "1AAD19",
            "showtype": "",
            "fb": "1",
            "theme": "",
            "lang": "2052",
            "sess":self.sess,
            "fwidth": "0",
            "uid": "",
            "cap_cd": "",
            "rnd": random.randint(100000, 999999),
            "rand": random.random(),
            'vsig': self.vsig,
            "img_index": index,
        }

        return requests.get(url="https://ssl.captcha.qq.com/cap_union_new_getcapbysig", headers=headers,
                            params=params, verify=False, proxies= self.proxies).content

    # 第一个包　获取 sess
    def GetFirstPackage(self):
        params = {
            'aid': "2000000020",
            #'asig': self.asig,
            'captype': '7',
            'protocol': 'https',
            'clientype': '2',
            'disturblevel': '1',
            'apptype': '',
            #'curenv': 'open',
            'noheader': '1',
            'color': '1ADD19',
            'showtype': '',
            'cap_cd': '',
            'lang': '2052',
            'fb': '1',
            'uid': '',
            #'rnd': random.randint(100000, 999999),
            #'collect': '',
            #'firstvrytype': '1',
            'callback': "_aq_233",
            'sess': ""
        }

        response = requests.get("https://ssl.captcha.qq.com/cap_union_prehandle", params=params,
                                headers=self.headers, verify=False, proxies= self.proxies).text
        response = re.findall(r"_aq_233\((.*?)\)",response)[0]
        response = json.loads(response)
        self.sess = response["sess"]

    # 第二个包　获取　vsig randstr inity ans
    def GetSecondPackage(self):
        params = {
            "aid": "2000000020",
            "captype": "7",
            "protocol": "https",
            "clientype": "2",
            "disturblevel": "1",
            "apptype": "",
            "noheader": "1",
            "color": "1AAD19",
            "showtype": "",
            "fb": "1",
            "theme": "",
            "lang": "2052",
            "sess": self.sess,
            "fwidth": "0",
            "uid": "",
            "cap_cd": "",
            "rnd": random.randint(100000, 999999),
            "rand":  random.random(),
        }

        response = requests.get("https://ssl.captcha.qq.com/cap_union_new_getsig", params=params,
                                headers=self.headers, verify=False, proxies= self.proxies).json()
        print(response)
        self.vsig = response["vsig"]
        self.inity = response["inity"]
        self.chlg = response["chlg"]

    # 　第三个包　获取 _c, websig
    def GetThirdPackage(self):
        params = {
            "aid": "2000000020",
            "captype": "7",
            "protocol": "https",
            "clientype": "1",
            "disturblevel": "1",
            "apptype": "",
            "noheader": "1",
            "color": "1AAD19",
            "showtype": "",
            "fb": "1",
            "theme": "",
            "lang": "2052",
            "sess": self.sess,
            "fwidth": "0",
            "uid": "",
            "cap_cd": "",
            "rnd": random.randint(100000, 999999),
        }
        response = requests.get("https://captcha.guard.qcloud.com/cap_union_new_show", params=params,
                                headers=self.headers,verify=False, proxies= self.proxies).text
        regular = r't.ans\+"&(.*?)="\+(.*?)\+"&websig=(.*?)&'
        response = re.findall(regular, response)[0]
        self._c = response[0]
        self.websig = response[2]
        print(self._c,self.websig)

    # 图片识别 采用图片异或
    def GetLocate(self):
        a = self.GetImg(0)
        b = self.GetImg(1)
        c = self.GetImg(2)
        # print(hashlib.md5(a+b+c).hexdigest())
        h = hashlib.md5(a + b + c).hexdigest()
        path = "checkcodes/" + h
        if not os.path.exists(path):
            os.makedirs(path)
        open(path + '/full.png', 'wb').write(a)
        open(path + '/a.png', 'wb').write(b)
        open(path + '/b.png', 'wb').write(c)
        img_full = Image.open(path + '/full.png')
        img_a = Image.open(path + '/a.png')
        img_diff = ImageChops.difference(img_full, img_a)

        img_diff.save(path + '/diff.png')
        pix = img_diff.load()
        result = ''
        for x in range(img_diff.size[0]):
            for y in range(img_diff.size[1]):
                (r, g, b) = pix[x, y]
                if r + g + b > 150 and y > 5 and x > 5:
                    result = str(x - 20) + "," + str(self.inity) + ";"
                    break
            if result != '':
                break
        __import__('shutil').rmtree(path)
        self.result = result
        print("Loca",self.result)

    # 最终数据包
    def FinalPackage(self):
        reply = requests.post(api,params={"x":self.result.split(",")[0]},data= {"js":base64.b64encode(requests.get("https://dj.captcha.qq.com/tdc.js",verify=False).text.encode()).decode()}).json()
        eks = reply["eks"]
        enced = reply["enced"]
        fps = reply["fps"]
        postData = {
            "aid": "2000000020",
            "captype": "7",
            "protocol": "https",
            "clientype": "1",
            "disturblevel": "1",
            "apptype": "",
            "noheader": "1",
            "color": "1AAD19",
            "showtype": "",
            "fb": "1",
            "theme": "",
            "lang": "2052",
            "sess": self.sess,
            "fwidth": "0",
            "uid": "",
            "cap_cd": "",
            "rnd": random.randint(100000, 999999),
            "rand": random.random(),
            "subcapclass": "10",
            "vsig": self.vsig,
            "ans": self.result,
            self._c: enced,
            "websig": self.websig,
            "cdata": self.cdata,
            #"fpinfo": "fpsig=1000EB7F2A21E362221198D7ED68369CDD36FE199D088E0617A23D35F2B3F8688FBF9F42F24E5BADE1D0A699496917892937",
            'fpinfo': 'undefined',
            "eks": eks,
            "fps": fps,
            "tlg": "1",
        }
        return requests.post(url="https://ssl.captcha.qq.com/cap_union_new_verify", data=postData,
                             headers=self.headers, verify=False, proxies= self.proxies).json()

    def Verify(self):
        self.GetFirstPackage()
        self.GetSecondPackage()
        self.GetThirdPackage()
        self.GetCdata()
        self.GetLocate()
        return self.FinalPackage()

# 主入口
@app.route("/get",methods=["POST","GET"])
def get():
    proxy = request.args.get("proxy",None)
    if proxy != None:
        proxy = base64.b64decode(proxy.encode()).decode()
    print("Got Task, proxy", proxy)
    proxies = {
        "https":proxy,
        "http":proxy
    }
    #return '{"errorCode": "0", "randstr": "@GGG", "ticket": "t027MIgKwg6mXyh9P7wCqADg-OcSOfKp8yhE4fwCc7egvlpXyJ04bJTe5CIpOUtySqeNgR8RFIry5TMiVTEto5pQLYQCYhp_amge8IGtabsvTo*", "errMessage": "OK", "sess": ""}'
    verify_class = VerifyCode(proxies)
    return json.dumps(verify_class.Verify())

if __name__ == "__main__":
    app.run(port=6777)
    exit()
    verify_class = VerifyCode(None)
    a = 0
    for i in range(99999):
        ans = verify_class.Verify()
        if ans["errorCode"] == "0":
            a += 1
        print("ACC",a,"/",i,ans)
    print(a)
    