/*
Geetest-v2 JS 入口
其余代码 请参考博客补齐
https://lengyue.me/index.php/category/captcha/geetest/
*/
function get_slide_w(j9S, track, x) {
    var j9S = JSON.parse(j9S);
    var O32 = aa_encode_1(JSON.parse(track));
    O32 = aa_encode_2(O32, j9S["c"], j9S["s"]);
    var passtime = 0;
    for (var i = 0, v = JSON.parse(track); i < v.length; i++){
        passtime+=v[i][2];
    }

    var Z9S = {
        "userresponse": a4(x, j9S.challenge),
        "passtime": passtime,
        "imgload": RandomNum(300, 400),
        "aa": O32,
        "ep": {
            "v": "6.0.9"
        }
    };
    Z9S.rp = MD5(j9S.gt + j9S.challenge.slice(0, 32) + Z9S.passtime);
    var e9S = RSA_Encrypt(key)
        , a9S = AES_Encrypt(JSON.stringify(Z9S), key)
        , I9S = ce(a9S)
        , L9S = {
        'gt': j9S.gt,
        'challenge': j9S.challenge,
        'w': I9S + e9S
    };
    return JSON.stringify(L9S);
}