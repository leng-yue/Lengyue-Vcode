let async = require("async");
let request = require("request");
let CryptoJS = require("crypto-js");
let fs = require("fs");

function text_substr(text, start, end) {
    let x;
    x = text.indexOf(start);
    x += start.length;
    return text.slice(x, text.indexOf(end, x));
}

Math.randomNum = function (start, end) {
    return Math.floor(start + Math.random() * (end - start))
};

function AES(data, encrypt_key) {
    const iv = "2801003954373300";
    let key = CryptoJS.enc.Utf8.parse(encrypt_key);
    let iv_utf8 = CryptoJS.enc.Utf8.parse(iv);
    return CryptoJS.AES.encrypt(data, key, {
        iv: iv_utf8,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.ZeroPadding
    }).toString()
}

const ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36";
let headers = {
    "User-Agent": ua,
    "Referer": "captcha.luosimao.com"
};

let data_token, data_key, site_key, data_h, data_i, data_s;
site_key = "e7b4d20489b69bab25771f9236e2c4be";
async.waterfall([
    function (callback) {
        request.get({
            url: "https://captcha.luosimao.com/api/widget?k=" + site_key + "&l=zh-cn&s=normal&i=_7hgu8tifn",
            headers: headers
        }, function (err, resp, body) {
            data_token = text_substr(body, 'data-token="', '"');
            data_key = text_substr(body, 'data-key="', '"');
            console.info(data_token, data_key);
            callback(null);
        });
    },
    function (callback) {
        let raw_bg = ua + "||" + data_token + "||1920:1080||win32||webkit";
        let time = new Date().getTime() - 1000;
        let b_xy = Math.randomNum(100, 200);
        let raw_b = b_xy + ",2:" + time + "||" + b_xy + ",6:" + (time + Math.randomNum(200, 300));

        const encrypt_key = "c28725d494c78ad782a6199c341630ee";

        request.post({
            url: "https://captcha.luosimao.com/api/request?k=" + site_key + "&l=zh-cn",
            body: "bg=" + AES(raw_bg, encrypt_key) + "&b=" + AES(raw_b, encrypt_key),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": ua,
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }, function (err, resp, body) {
            console.info(body);
            let temp = JSON.parse(body);
            data_h = temp.h;
            data_i = temp.i;
            data_s = temp.s;
            console.info(text_substr(temp.w, '<i>', '</i>'));
            callback(null);
        });
    },
    function (callback) {
        //https://captcha.luosimao.com/api/frame?s=OAXb3WwBfrF7-ijs9s3M1fbOkbK7d3ni4M3GhdFoIxQN4xxTyeH9ZNiaIYXORTl5Xym2-ch-UGtk1oIlNpPJc4dw1X8JZ3pnQehQfrHjq4PEyKmqkZKNbRaJwDh4pzzDctoaWMP-sjoUaIERqXBdKXHIsJROsiaKAf9klesQgxQMqdfi2rzstqbwwSeRvEj3G8aTI-wy5ZHWnBacTVdeQS4C7TRk0e2_5qMfjonTEqyi7KYop_HSUTp6p2RWmO5TtYbDm8O3I1LJJhCy700NKK0FyXpOosu97xReyrBL6niOh0C7tD11UbEfndJOtC76xbMdgw16miaLoW5E-7Qao1Vr8mxYygruQLv16zRhsrNFo3Ez7W9yItKkzLZy5oNPNi5AaE3iE8eX7_NKJU30ywUi3yvqJwLUSKmlMd2HA1xcPEkvLyNME3B5vfyAzy41BAUwKUT1hP4Y8FTdOIO83jNynLfUFIuUPhIguMzDsoFSiiJ3Lp2syeh5ick6ZK-XswTeXQyQw4_4_Rtz78cqlbvWQxBFg2KXXquLx3P-XCfgx3a3ngIqPDgOrVK2U7wq7xvHqQER1oG9N2YfuOXTLQ&i=_nndzcmcx8&l=zh-cn
        request.get({
            url: "https://captcha.luosimao.com/api/frame?s=" + data_s + "&i=_udzwwui1d&l=zh-cn",
            headers: headers
        }, function (err, response, body) {
            let captchaImg = text_substr(body, 'captchaImage = ', ';');
            eval("captchaImg = " + captchaImg);
            request.get({
                url: captchaImg.p[0].replace("https", "http"),
                encoding: null,
                headers: headers,
            }, function (err, response, body) {
                request.post({
                    url: 'http://127.0.0.1:7788/luosimao?loca=' + encodeURIComponent(JSON.stringify(captchaImg.l)),
                    body: Buffer.from(body),
                    encoding: null
                }, function (err, response, body) {
                    if (err) {
                        callback(err);
                        return
                    }
                    fs.writeFile("./save.bmp", body, function () {
                    });
                    function test() {
                        fs.readFile("./location.txt", function (a, data) {
                            data = data.toString();
                            if (data) {
                                console.info(data);
                                fs.writeFile("./location.txt", "", function () {
                                });
                                callback(null, data);
                            }else{
                                test()
                            }
                        })
                    }
                    test();

                });
            });
        });
},
    function (loca, callback) {
        console.info(loca);
        let data_v = AES(loca, data_i).replace("+", "-").replace("/", "_").replace(/=+/, "");
        request.post({
            url: "https://captcha.luosimao.com/api/user_verify",
            body: "h=" + data_h + "&v=" + data_v + "&s=" + CryptoJS.MD5(loca).toString(),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": ua,
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }, function (err, response, body) {
            console.info(body);
            callback(null);
        })
    }
]);
