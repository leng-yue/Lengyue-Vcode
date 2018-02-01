import time
import execjs
import re
import base64
from flask import Flask, request
import json
import class_track

app = Flask(__name__)
@app.route("/parse", methods=['POST'])
def get():
    #从网络上获取一个js
    _JS = base64.b64decode(request.form["js"].encode()).decode().replace("window","''")
    #print("原汁原味的JS ->", _JS)

    # 定位函数入口
    # 翻译函数入口
    Function_Translate = re.findall(r";var (.*?)=function", _JS)[0]

    # 加载注入JS
    JS_Inject = open("./inject.js", "r").read().replace("{%replace%}", Function_Translate)

    # print("准备注入的JS ->", JS_Inject)

    # 编译js,注入JS
    _JS = _JS + JS_Inject
    # print("注入后的JS ->", _JS)
    JS = execjs.compile(_JS)

    # 寻找所有翻译目标
    List_Translate = re.findall(r'%s\("(.*?)","(.*?)"\)' % Function_Translate, _JS)
    a = []
    b = []
    for Single_Translate in List_Translate:
        a.append(Single_Translate[0])
        b.append(Single_Translate[1])

    # 调用之前注入的函数,存入数组, list 和 字典都有
    List_Translate = JS.call("getList", a, b)
    List_Translate_b = List_Translate[1]
    List_Translate = List_Translate[0]

    # FPS 计算开始 请注意 不要尝试修改这段代码 你会疯的= = 这里面的关系非常复杂
    # print("翻译结果 -> ", List_Translate)
    # print(List_Translate_b)
    # FPS 正则1 直接性
    fpsv = re.findall(r'[\(|, ](\d+)\)\[%s\("(.*?)","(.*?)"\)\]\((\d+)\)' % Function_Translate, _JS)
    print(fpsv)
    s = ""
    temp = ""
    for i in fpsv:
        # print(List_Translate_b[i[0]],i)
        if List_Translate_b[i[1]] == "set":
            s += "r[%s]=!0," % i[3]
            temp = i[0]
        print(i)
    # 正则2 关系型
    l = list(set(re.findall(r'var (.)=.{0,50}%s\)' % (temp), _JS)))
    for i in l:
        # print(i)
        # print('%s\[%s\("(.*?)","(.*?)"\)\]\(%s\)' % (i, Function_Translate,temp))
        # 二次定位
        for h in re.findall(r'%s\[%s\("(.*?)","(.*?)"\)\]\((\d+)\)' % (i, Function_Translate), _JS):
            # print(List_Translate_b[i[0]],i)
            # 有效校验
            if h[0] in List_Translate_b.keys() and List_Translate_b[h[0]] == "set":
                s += "r[%s]=!0," % h[2]
                print(h)
    print("r=[],%sr" % s)
    raw = execjs.eval("r=[],%sr" % s)
    # print(raw)
    # 注入JS计算FPS
    # raw = [None,None,None,None,None,None,None,None,None,True,None,None,None,None,None,None,None,None,None,True,None,None,None,None,None,None,True,None,None,None,None,None,None,True]
    fps = JS.call("getFPS", raw)
    print("FPS_RAW ->", raw)
    print("FPS ->", fps)

    # 计算密钥开始
    # Forgive是需要忽略的内容
    Forgive = "localDescriptionaddEventListenergetComputedStyle"
    Encrypt_Key = None
    for Single_Translate in List_Translate:
        # if Single_Translate[2] == "exports":
        #    print('%s("%s", "%s")' % (Function_Translate,Single_Translate[0],Single_Translate[1]))
        if len(Single_Translate[2]) == 16:
            if Single_Translate[2] not in Forgive:
                Encrypt_Key = Single_Translate[2]

    print("密匙 ->", Encrypt_Key)

    # 加载冷月重写的加密JS
    # 待加密内容
    # [[84,281,89],[6,0,17],[10,2,16],[14,0,15],[9,0,17],[3,0,18],[2,0,15],[1,0,18],[4,0,16],[4,0,21],[3,0,13],[2,0,21],[2,0,30],[0,0,15],[1,0,16],[2,0,20],[4,0,14],[9,0,16],[9,0,16],[27,0,17],[21,0,17],[12,0,19],[6,0,15],[10,0,15],[8,0,17],[8,0,18],[9,0,16],[10,0,17],[3,0,17],[1,0,133],[0,0,16],[4,0,18],[7,0,16],[5,0,16],[2,0,18],[2,-1,16],[-1,0,282],[-1,0,18],[0,0,33],[-1,0,18],[-1,0,48],[0,0,26]]
    track = class_track.getTrack(int(request.args.get("x")))
    Wait_Encrypt = '{"cd":[[360,567],0,[],32,[],0,0,0,2,0,"https://weixin110.qq.com/security/readtemplate?ra' \
                   'nd=1512991986334","360-640-640-32-*-*-**-*",[],[{"t":2,"x":300,"y":282}],1,[],0,0,{"in":' \
                   '["172.16.2.15"]},1513715019750,360,' + str(track[:-1]) + ',640,151523' \
                   '0250,null,1,"Android",[],"chrome/39.0.0.0",2138613663,'+str(int(time.time()))+',0,[],0,true,8,"https://s' \
                   'sl.captcha.qq.com/cap_union_new_show",'+str(int(time.time()))+',"UTF-8",null],"sd":{"od":"'+fps+'","ft":"' \
                   'qn_7PJm7H","clientType":"1","coordinate":[17,59,0.4794],"trycnt":1,"refreshcnt":0,"slideV' \
                   'alue":'+str(track)+',"dragobj":0}}'

    print("待加密内容 ->", Wait_Encrypt)
    # 编译encrypt.js
    JS_Encrypt = open("./encrypt.js", "r").read()
    JS = execjs.compile(JS_Encrypt)
    # 加密
    enced = JS.call("encrypt", Wait_Encrypt, Encrypt_Key)
    print("加密结果 ->", enced)

    eks = re.findall(r'"_(.*?)"', _JS)
    for i in eks:
        if len(i) > 20:
            print("Eks", "->", "_" + i)
            eks = "_" + i
    # print(base64.b64decode(enced.encode()).decode())
    # print(len(base64.b64decode(enced.encode())))

    # 加载解密js
    # enced = "c8pYlG/FIPFSTH7iYU61RwRL1Vw6PmCFEJUrVbqeMDY5bC+JVTkCC+vnXfhI8Jxln9aob5JM3qkTIXcsBhBLFa3v1nagJNyElLNG0phonX074hG2DHOZitEBqwdZuFnoUX43pPJf6VMkEtPv2Y87zym3exJi/vdw+Knvq1fnynpbT+gIM5lWoCDDK4Zsc9fGvEi0x2heVMm42lAkMN7n+J6Manp8npuTH26g52xpW9hbFJnJp0H+YxRQKJRgV2RMW3PjJ/9Ptd3Mo2h5zmfkTWDEj23jwPUpfIhkv+VdEUQrSMkPuQzn4HRVzJkjjbV8HP0m1qvmHq+Xjz0w1C42QdVISsB15UNB7w8Tp2M6ZFfzcvsOAclnxq/8j+d1eWxwUNQUM08+dPWtG66/TAkM+0Plio8ozT4eShUnKiMhb6Wno5SAhDIBOKCQ41zk///LIaFt0Ypm6gH0nl9HugRbBHpJOenxo2e+zJDp27Qny942HEdkzR3xDdjJS+aCtoRGDv40rSm7DkLVSErAdeVDQR0vyxOkMcgdqsGwny1WOyXkbOKJ/7s2+1+weqnFCYjCLKPEjqdYH7va6I3ljI7jY9VISsB15UNByVa9dQwsoDpVNOv+43RCsGbGHFCvmdQNmqvbIq49lrG0qdln0UIS3Ev44bORuwx2NDOX4i79erjOLS0gk7rrbBUErhRBH+RAdixUBlPNidGwkMgqLl/XIb0XGcM04r09AagtLGcfqfWW98Qu8TgEEQkBF9/1HaWXGk40aLy7+2X0r0gNKR6FWQGoLSxnH6n1aMknv4263AKG8N7DgtCeVvCRA36aMeL6Coe1H+noqA2F63vofjWhculstpf8MvSdX/YuvzItbzFrfOuXIGVZqjNrE/iRGZDOQbzfLv3jpjpd6RV/TXgbo+W+pMKShOF3WyblxVpBUneJQ2+VJ2TI3SnqCqClEqe+XO7t2eCJ8X1VH4mewS50eLV1fdluoNxBKrwE2EOpUetEgTEcubwuLO9i9WMM75VAPRwRXmpWhklm1m01bv9zIENFO+jy0w2FMzDHV5nUkRrXHxUEkXxqx0VlSj8Cl7szFKq1uPsHFhS6DG1qn2rHiwzQLFXIQeHkGL0+IX/aPSWtFoFpCtdIFA8uqjbvxmaGc97T7uVB/A5tCzxsoxeo/0yPpvF/h9UbaQxmMTWfTKJ6WzONadgOmQ18XAH5SJbWN5EKibSUC/COexncKDTTIO2KAaJ0U7285cMC3efOSJ3pALekWSPqXuFAgRNkTdV9KuQ6eFd3xvE02o/7KYRBdWNFWDQGh935tbd4JBWX4zRK9qG5cj0WbbWBWV4rCNdjToiFwjt8/YB719ZfATGXJ6kAFFkoHr7/m3ORkqrK1EdFtDwxLhHPpGbGHFCvmdQNl9XApl25ygWtbVMb0SSDL+E8bHa8n7KBbkgKFBGB8G5SBXyGGrO3muS7vQUV/5AT4fPVgAH90peu+FuMofZvZLJhVYU9JnAf6QC3pFkj6l6oPCYOj7FwA3+lKHvtHufFq/47kafkJpzO5uTepCRxxmEsCdHXz2R9o9J2of5PHDPpALekWSPqXswh3XFpD+JNstHK2vLbltev/I/ndXlscLCQyCouX9ch8XHYJKSGcjLj9aQofufnhRFFW+HVr/qyLo3gxIvTIOIaTjRovLv7ZcYLwgf4tapJGrjWucqMp8pdnE9gRTgCzJWvxrREziS+qRijWVqsemY="
    JS_Decrypt = open("./decrypt.js", "r").read()
    JS = execjs.compile(JS_Decrypt)
    # 加密
    deced = JS.call("decrypt", enced, Encrypt_Key)
    print("解密结果 ->", deced)

    return json.dumps({"eks":eks,"enced":enced,"fps":fps, "raw":deced})

if __name__ == "__main__":
    app.run()

