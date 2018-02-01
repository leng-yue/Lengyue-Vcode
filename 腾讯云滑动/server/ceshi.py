import requests
import execjs
import re

#从网络上获取一个js
#_JS = open("./demo.js","r").read().replace("window","''")
a = requests.get("https://dj.captcha.qq.com/tdc.js").text
open("./demo.js","w").write(a)
_JS = a.replace("window","''")
print("原汁原味的JS ->", _JS)

#定位函数入口
#翻译函数入口
Function_Translate = re.findall(r";var (.*?)=function", _JS)[0]

#加载注入JS
JS_Inject = open("./inject.js","r").read().replace("{%replace%}",Function_Translate)

#print("准备注入的JS ->", JS_Inject)

#编译js,注入JS
_JS = _JS + JS_Inject
#print("注入后的JS ->", _JS)
JS = execjs.compile(_JS)

#寻找所有翻译目标
List_Translate = re.findall(r'%s\("(.*?)","(.*?)"\)' % Function_Translate, _JS)
a = []
b = []
for Single_Translate in List_Translate:
    a.append(Single_Translate[0])
    b.append(Single_Translate[1])


#调用之前注入的函数,存入数组, list 和 字典都有
List_Translate = JS.call("getList", a, b)
List_Translate_b = List_Translate[1]
List_Translate = List_Translate[0]

#FPS 计算开始 请注意 不要尝试修改这段代码 你会疯的= = 这里面的关系非常复杂
#print("翻译结果 -> ", List_Translate)
#print(List_Translate_b)
#FPS 正则1 直接性
fpsv = re.findall(r'[\(|, ](\d+)\)\[%s\("(.*?)","(.*?)"\)\]\((\d+)\)' % Function_Translate, _JS)
print(fpsv)
s = ""
temp = ""
for i in fpsv:
    #print(List_Translate_b[i[0]],i)
    if List_Translate_b[i[1]] == "set":
        s += "r[%s]=!0," % i[3]
        temp = i[0]
    print(i)
#正则2 关系型
l = list(set(re.findall(r'var (.)=.{0,50}%s\)' % (temp), _JS)))
for i in l:
    #print(i)
    #print('%s\[%s\("(.*?)","(.*?)"\)\]\(%s\)' % (i, Function_Translate,temp))
    #二次定位
    for h in re.findall(r'%s\[%s\("(.*?)","(.*?)"\)\]\((\d+)\)' % (i, Function_Translate), _JS):
        # print(List_Translate_b[i[0]],i)
        # 有效校验
        if h[0] in List_Translate_b.keys() and List_Translate_b[h[0]] == "set":
            s += "r[%s]=!0," % h[2]
            print(h)
print("r=[],%sr" % s)
raw = execjs.eval("r=[],%sr" % s)
#print(raw)
#注入JS计算FPS
#raw = [None,None,None,None,None,None,None,None,None,True,None,None,None,None,None,None,None,None,None,True,None,None,None,None,None,None,True,None,None,None,None,None,None,True]
fps = JS.call("getFPS",raw)
print("FPS_RAW ->", raw)
print("FPS ->", fps)

# 计算密钥开始
#Forgive是需要忽略的内容
Forgive = "localDescriptionaddEventListenergetComputedStyle"
Encrypt_Key = None
for Single_Translate in List_Translate:
    #if Single_Translate[2] == "exports":
    #    print('%s("%s", "%s")' % (Function_Translate,Single_Translate[0],Single_Translate[1]))
    if len(Single_Translate[2]) == 16:
        if Single_Translate[2] not in Forgive:
            Encrypt_Key = Single_Translate[2]

print("密匙 ->", Encrypt_Key)

#加载冷月重写的加密JS
#待加密内容
Wait_Encrypt = '{"cd":[[430,690],1,[{"t":2892,"x":269,"y":256}],24,[],1,28,1,1,0,"?rand=1512991986334","1536-864-824-24-*-*-**-*",["zh-CN","zh"],[{"t":2895,"x":261,"y":232}],1,[],0,5,{"in":["192.168.0.101"]},1513715217552,1536,[[262,19,2892490],[0,25,17],[0,26,17],[0,22,16],[7,18,17],[3,15,16],[0,7,16],[2,7,16],[0,7,17],[0,6,17],[0,2,17],[0,2,17],[0,1,116],[-2,3,15],[0,1,17],[-3,6,18],[-7,5,16],[-11,7,16],[-11,4,17],[-8,6,18],[-7,1,17],[-3,3,16],[-3,3,20],[-5,1,14],[-6,4,16],[-8,7,17],[-4,3,18],[-6,3,15],[-5,2,18],[-2,0,16],[-1,0,15],[-1,0,34],[-3,0,33],[1,0,13],[-7,0,17],[-1,0,17],[-3,0,16],[-4,0,17],[-14,2,17],[-7,3,16],[-15,5,18],[-4,0,15],[-3,0,35],[3,0,166],[0,1,752],[0,0,32],[2,0,17],[6,0,18],[8,0,14],[11,3,17],[18,1,16],[17,1,17],[16,0,16],[17,0,17],[11,0,17],[5,0,16],[2,0,16],[1,0,17],[3,0,16],[3,0,18],[6,0,17],[6,0,16],[3,0,17],[0,0,17],[2,0,16],[1,0,34]],864,1515230448,"09447b77b8b0952a69b35d3246b72301c6a8449e659da2b3cf45a55b4865a3a2",2,"other",[{"x":0,"y":0,"z":0},{"x":0,"y":0,"z":0}],"chrome/63.0.3239.108",1923262133,1514278022,0,[],0,true,8,"https://ssl.captcha.qq.com/cap_union_new_show",1515233370,"UTF-8",null],"sd":{"od":"gACQAS","ft":"6f_7P_n_H","clientType":"1","coordinate":[70,53,0.4294],"trycnt":2,"refreshcnt":0,"slideValue":[[123,227,2],[0,0,33],[2,0,16],[6,0,18],[8,0,14],[11,3,17],[18,1,16],[17,1,17],[16,0,16],[17,0,17],[11,0,18],[5,0,15],[2,0,16],[1,0,17],[3,0,16],[3,0,18],[6,0,17],[6,0,16],[3,0,17],[0,0,17],[2,0,16],[1,0,34],[0,0,11]],"dragobj":0,"jshook":4}}'
print("待加密内容 ->", Wait_Encrypt)
#编译encrypt.js
JS_Encrypt = open("./encrypt.js","r").read()
JS = execjs.compile(JS_Encrypt)
#加密
enced = JS.call("encrypt", Wait_Encrypt, Encrypt_Key)
print("加密结果 ->", enced)

eks = re.findall(r'"_(.*?)"',_JS)
for i in eks:
    if len(i) > 20:
        print("Eks","->","_" + i)
        eks = "_" + i
#print(base64.b64decode(enced.encode()).decode())
#print(len(base64.b64decode(enced.encode())))


#加载解密js
#enced = "c8pYlG/FIPFSTH7iYU61RwRL1Vw6PmCFEJUrVbqeMDY5bC+JVTkCC+vnXfhI8Jxln9aob5JM3qkTIXcsBhBLFa3v1nagJNyElLNG0phonX074hG2DHOZitEBqwdZuFnoUX43pPJf6VMkEtPv2Y87zym3exJi/vdw+Knvq1fnynpbT+gIM5lWoCDDK4Zsc9fGvEi0x2heVMm42lAkMN7n+J6Manp8npuTH26g52xpW9hbFJnJp0H+YxRQKJRgV2RMW3PjJ/9Ptd3Mo2h5zmfkTWDEj23jwPUpfIhkv+VdEUQrSMkPuQzn4HRVzJkjjbV8HP0m1qvmHq+Xjz0w1C42QdVISsB15UNB7w8Tp2M6ZFfzcvsOAclnxq/8j+d1eWxwUNQUM08+dPWtG66/TAkM+0Plio8ozT4eShUnKiMhb6Wno5SAhDIBOKCQ41zk///LIaFt0Ypm6gH0nl9HugRbBHpJOenxo2e+zJDp27Qny942HEdkzR3xDdjJS+aCtoRGDv40rSm7DkLVSErAdeVDQR0vyxOkMcgdqsGwny1WOyXkbOKJ/7s2+1+weqnFCYjCLKPEjqdYH7va6I3ljI7jY9VISsB15UNByVa9dQwsoDpVNOv+43RCsGbGHFCvmdQNmqvbIq49lrG0qdln0UIS3Ev44bORuwx2NDOX4i79erjOLS0gk7rrbBUErhRBH+RAdixUBlPNidGwkMgqLl/XIb0XGcM04r09AagtLGcfqfWW98Qu8TgEEQkBF9/1HaWXGk40aLy7+2X0r0gNKR6FWQGoLSxnH6n1aMknv4263AKG8N7DgtCeVvCRA36aMeL6Coe1H+noqA2F63vofjWhculstpf8MvSdX/YuvzItbzFrfOuXIGVZqjNrE/iRGZDOQbzfLv3jpjpd6RV/TXgbo+W+pMKShOF3WyblxVpBUneJQ2+VJ2TI3SnqCqClEqe+XO7t2eCJ8X1VH4mewS50eLV1fdluoNxBKrwE2EOpUetEgTEcubwuLO9i9WMM75VAPRwRXmpWhklm1m01bv9zIENFO+jy0w2FMzDHV5nUkRrXHxUEkXxqx0VlSj8Cl7szFKq1uPsHFhS6DG1qn2rHiwzQLFXIQeHkGL0+IX/aPSWtFoFpCtdIFA8uqjbvxmaGc97T7uVB/A5tCzxsoxeo/0yPpvF/h9UbaQxmMTWfTKJ6WzONadgOmQ18XAH5SJbWN5EKibSUC/COexncKDTTIO2KAaJ0U7285cMC3efOSJ3pALekWSPqXuFAgRNkTdV9KuQ6eFd3xvE02o/7KYRBdWNFWDQGh935tbd4JBWX4zRK9qG5cj0WbbWBWV4rCNdjToiFwjt8/YB719ZfATGXJ6kAFFkoHr7/m3ORkqrK1EdFtDwxLhHPpGbGHFCvmdQNl9XApl25ygWtbVMb0SSDL+E8bHa8n7KBbkgKFBGB8G5SBXyGGrO3muS7vQUV/5AT4fPVgAH90peu+FuMofZvZLJhVYU9JnAf6QC3pFkj6l6oPCYOj7FwA3+lKHvtHufFq/47kafkJpzO5uTepCRxxmEsCdHXz2R9o9J2of5PHDPpALekWSPqXswh3XFpD+JNstHK2vLbltev/I/ndXlscLCQyCouX9ch8XHYJKSGcjLj9aQofufnhRFFW+HVr/qyLo3gxIvTIOIaTjRovLv7ZcYLwgf4tapJGrjWucqMp8pdnE9gRTgCzJWvxrREziS+qRijWVqsemY="
JS_Decrypt = open("./decrypt.js","r").read()
JS = execjs.compile(JS_Decrypt)
#加密
deced = JS.call("decrypt", enced, Encrypt_Key)
print("解密结果 ->", deced)
#print(xtea3.new(Encrypt_Key.encode(),mode=xtea3.MODE_CTR).decrypt(base64.b64decode(enced.encode())))
#print(json.dumps({"eks":eks,"enced":enced,"fps":fps}))