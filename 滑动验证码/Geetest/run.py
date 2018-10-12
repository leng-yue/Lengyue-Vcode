import geetest
import requests
total = 0
suc = 0
while True:
    total = total + 1
    geeData = requests.get(
        "https://passport.bilibili.com/captcha/gc?cType=2&vcType=2&_=1539152432261"
    ).json()["data"]
    referer = "https://passport.bilibili.com/login"
    ans = geetest.crack(geeData["gt"], geeData["challenge"], referer)
    # print(ans)
    if "success" in ans.keys() and ans["success"] == 1:
        suc += 1
    print("Acc", "%.2f" % (suc * 1.00 / total), suc, total, ans)
