## Tvcode 是冷月开发的腾讯滑动识别程序
#### 最后更新 2017/12/12
#### 请勿用于非法用途

#### 使用方式:

	import tencent #导入模块
    aid = "1252020920" #aid 和 asig是必要参数
    asig = "D48pTEFAsoRt44ABoMz3IlJUEuWQY6lNFkMNjqcQywBdCxx8ZgJTmN3Yn--MjCtap7FNG5h91-2ei18s3nswvGQTmykMuxd2rLo88fFP2c4ms5huZIk-uIW22j_1PmINp_ld3kCgKAqMUqUq9GR6kA**"
    verify_class = tencent.VerifyCode(aid,asig)
    print(verify_class.Verify()) # 请求

#### 测试结果:
![ScreenHost](https://raw.githubusercontent.com/leng-yue/AliVcode/master/%E8%85%BE%E8%AE%AF%E4%BA%91%E6%BB%91%E5%8A%A8/screenhost.png)

