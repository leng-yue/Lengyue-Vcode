/*
JD移动端验证码
*/

var JD = function(){
     this.A = function(a, c)
    {
        for (var t = a.toString().length; t < c;)
            a = "0" + a,
                t++;
        return a
    };
    this.Z = function (a, c) {
    return function(a) {
        var c, t, e, i, o, n, r, s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_".split("");
        for (t = e = 0,
                 i = a.length,
                 n = (i -= o = i % 3) / 3 << 2,
             o > 0 && (n += 4),
                 c = new Array(n); t < i; )
            r = a.charCodeAt(t++) << 16 | a.charCodeAt(t++) << 8 | a.charCodeAt(t++),
                c[e++] = s[r >> 18] + s[r >> 12 & 63] + s[r >> 6 & 63] + s[63 & r];
        return 1 == o ? (r = a.charCodeAt(t++),
            c[e++] = s[r >> 2] + s[(3 & r) << 4]) : 2 == o && (r = a.charCodeAt(t++) << 8 | a.charCodeAt(t++),
            c[e++] = s[r >> 10] + s[r >> 4 & 63] + s[(15 & r) << 2]),
            c.join("")
    }(Q(a, c, 99992))};
        function aa(a, c) {
            var t = a
                , e = c;
            return c || (e = "E736B80A35290F193C2034A8021CC63B"),
                Z(t, e)
        }
    function Q(a, c, t) {
        return void 0 === a || null === a || 0 === a.length ? a : (a = K(a),
            c = K(c),
            function(a, c) {
                for (var t = a.length, e = 0; e < t; e++)
                    a[e] = String.fromCharCode(255 & a[e], a[e] >>> 8 & 255, a[e] >>> 16 & 255, a[e] >>> 24 & 255);
                var i = a.join("");
                return i
            }(function(a, c, t) {
                var e, i, o, n, r, s, h = a.length, p = h - 1;
                for (i = a[p],
                         o = 0,
                         s = 0 | Math.floor(6 + 52 / h); s > 0; --s) {
                    for (o = J(o + X()),
                             n = o >>> 2 & 3,
                             r = 0; r < p; ++r)
                        e = a[r + 1],
                            i = a[r] = J(a[r] + G(o, e, i, r, n, c, t));
                    e = a[0],
                        i = a[p] = J(a[p] + G(o, e, i, p, n, c, t))
                }
                return a
            }(z(a, !0), function(a) {
                return a.length < 4 && (a.length = 4),
                    a
            }(z(c, !1)), t)))
    }

    function U(a, c) {
        a = [a[0] >>> 16, 65535 & a[0], a[1] >>> 16, 65535 & a[1]],
            c = [c[0] >>> 16, 65535 & c[0], c[1] >>> 16, 65535 & c[1]];
        var t = [0, 0, 0, 0];
        return t[3] += a[3] + c[3],
            t[2] += t[3] >>> 16,
            t[3] &= 65535,
            t[2] += a[2] + c[2],
            t[1] += t[2] >>> 16,
            t[2] &= 65535,
            t[1] += a[1] + c[1],
            t[0] += t[1] >>> 16,
            t[1] &= 65535,
            t[0] += a[0] + c[0],
            t[0] &= 65535,
            [t[0] << 16 | t[1], t[2] << 16 | t[3]]
    }
    function N(a, c) {
        a = [a[0] >>> 16, 65535 & a[0], a[1] >>> 16, 65535 & a[1]],
            c = [c[0] >>> 16, 65535 & c[0], c[1] >>> 16, 65535 & c[1]];
        var t = [0, 0, 0, 0];
        return t[3] += a[3] * c[3],
            t[2] += t[3] >>> 16,
            t[3] &= 65535,
            t[2] += a[2] * c[3],
            t[1] += t[2] >>> 16,
            t[2] &= 65535,
            t[2] += a[3] * c[2],
            t[1] += t[2] >>> 16,
            t[2] &= 65535,
            t[1] += a[1] * c[3],
            t[0] += t[1] >>> 16,
            t[1] &= 65535,
            t[1] += a[2] * c[2],
            t[0] += t[1] >>> 16,
            t[1] &= 65535,
            t[1] += a[3] * c[1],
            t[0] += t[1] >>> 16,
            t[1] &= 65535,
            t[0] += a[0] * c[3] + a[1] * c[2] + a[2] * c[1] + a[3] * c[0],
            t[0] &= 65535,
            [t[0] << 16 | t[1], t[2] << 16 | t[3]]
    }
    function R(a, c) {
        return 32 == (c %= 64) ? [a[1], a[0]] : c < 32 ? [a[0] << c | a[1] >>> 32 - c, a[1] << c | a[0] >>> 32 - c] : (c -= 32,
            [a[1] << c | a[0] >>> 32 - c, a[0] << c | a[1] >>> 32 - c])
    }
    function W(a, c) {
        return 0 == (c %= 64) ? a : c < 32 ? [a[0] << c | a[1] >>> 32 - c, a[1] << c] : [a[1] << c - 32, 0]
    }
    function H(a, c) {
        return [a[0] ^ c[0], a[1] ^ c[1]]
    }
    function Y(a) {
        return a = H(a = N(a = H(a = N(a = H(a, [0, a[0] >>> 1]), [4283543511, 3981806797]), [0, a[0] >>> 1]), [3301882366, 444984403]), [0, a[0] >>> 1])
    }
    function V(a, c) {
        a = a || "",
            c = c || 0;
        for (var t = a.length % 16, e = a.length - t, i = [0, c], o = [0, c], n = [0, 0], r = [0, 0], s = [2277735313, 289559509], h = [1291169091, 658871167], p = 0; p < e; p += 16)
            n = [255 & a.charCodeAt(p + 4) | (255 & a.charCodeAt(p + 5)) << 8 | (255 & a.charCodeAt(p + 6)) << 16 | (255 & a.charCodeAt(p + 7)) << 24, 255 & a.charCodeAt(p) | (255 & a.charCodeAt(p + 1)) << 8 | (255 & a.charCodeAt(p + 2)) << 16 | (255 & a.charCodeAt(p + 3)) << 24],
                r = [255 & a.charCodeAt(p + 12) | (255 & a.charCodeAt(p + 13)) << 8 | (255 & a.charCodeAt(p + 14)) << 16 | (255 & a.charCodeAt(p + 15)) << 24, 255 & a.charCodeAt(p + 8) | (255 & a.charCodeAt(p + 9)) << 8 | (255 & a.charCodeAt(p + 10)) << 16 | (255 & a.charCodeAt(p + 11)) << 24],
                n = N(n = R(n = N(n, s), 31), h),
                i = U(N(i = U(i = R(i = H(i, n), 27), o), [0, 5]), [0, 1390208809]),
                r = N(r = R(r = N(r, h), 33), s),
                o = U(N(o = U(o = R(o = H(o, r), 31), i), [0, 5]), [0, 944331445]);
        switch (n = [0, 0],
            r = [0, 0],
            t) {
            case 15:
                r = H(r, W([0, a.charCodeAt(p + 14)], 48));
            case 14:
                r = H(r, W([0, a.charCodeAt(p + 13)], 40));
            case 13:
                r = H(r, W([0, a.charCodeAt(p + 12)], 32));
            case 12:
                r = H(r, W([0, a.charCodeAt(p + 11)], 24));
            case 11:
                r = H(r, W([0, a.charCodeAt(p + 10)], 16));
            case 10:
                r = H(r, W([0, a.charCodeAt(p + 9)], 8));
            case 9:
                r = N(r = R(r = N(r = H(r, [0, a.charCodeAt(p + 8)]), h), 33), s),
                    o = H(o, r);
            case 8:
                n = H(n, W([0, a.charCodeAt(p + 7)], 56));
            case 7:
                n = H(n, W([0, a.charCodeAt(p + 6)], 48));
            case 6:
                n = H(n, W([0, a.charCodeAt(p + 5)], 40));
            case 5:
                n = H(n, W([0, a.charCodeAt(p + 4)], 32));
            case 4:
                n = H(n, W([0, a.charCodeAt(p + 3)], 24));
            case 3:
                n = H(n, W([0, a.charCodeAt(p + 2)], 16));
            case 2:
                n = H(n, W([0, a.charCodeAt(p + 1)], 8));
            case 1:
                n = N(n = R(n = N(n = H(n, [0, a.charCodeAt(p)]), s), 31), h),
                    i = H(i, n)
        }
        return i = H(i, [0, a.length]),
            o = H(o, [0, a.length]),
            i = U(i, o),
            o = U(o, i),
            i = Y(i),
            o = Y(o),
            i = U(i, o),
            o = U(o, i),
        ("00000000" + (i[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (i[1] >>> 0).toString(16)).slice(-8) + ("00000000" + (o[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (o[1] >>> 0).toString(16)).slice(-8)
    }
    function X() {
        return 1111471640 + parseInt(function(a) {
            var c, t, e, i, o, n, r, s, h, p, d = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];
            if (r = a.length,
                a = (a += Array(5 - r % 4).join("=")).replace(/\-/g, "+").replace(/\_/g, "/"),
                /[^ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\+\/\=]/.test(a))
                return "";
            for (s = "=" == a.charAt(r - 2) ? 1 : "=" == a.charAt(r - 1) ? 2 : 0,
                     h = r,
                 s > 0 && (h -= 4),
                     h = 3 * (h >> 2) + s,
                     p = new Array(h),
                     o = n = 0; o < r && -1 != (c = d[a.charCodeAt(o++)]) && -1 != (t = d[a.charCodeAt(o++)]) && (p[n++] = String.fromCharCode(c << 2 | (48 & t) >> 4),
            -1 != (e = d[a.charCodeAt(o++)])) && (p[n++] = String.fromCharCode((15 & t) << 4 | (60 & e) >> 2),
            -1 != (i = d[a.charCodeAt(o++)])); )
                p[n++] = String.fromCharCode((3 & e) << 6 | i);
            return p.join("")
        }("MTU0Mjk2NDEyOQ"))
    }
    function z(a, c) {
        var t, e = a.length, i = e >> 2;
        0 != (3 & e) && ++i,
            c ? (t = new Array(i + 1))[i] = e : t = new Array(i);
        for (var o = 0; o < e; ++o)
            t[o >> 2] |= a.charCodeAt(o) << ((3 & o) << 3);
        return t
    }
    function J(a) {
        return 4294967295 & a
    }
    function G(a, c, t, e, i, o, n) {
        var r = n - 25700;
        if (1 == r >>> 16) {
            var s = r >>> 12 & 7
                , h = r >>> 8 & 7
                , p = r >>> 4 & 7
                , d = 7 & r;
            return q(a, c, t, e, i, o) ^ (c >>> s ^ t << h) + (a >>> p & 63 ^ t + c >>> (7 - d >>> 1) & 63)
        }
        return q(a, c, t, e, i, o)
    }
    function q(a, c, t, e, i, o) {
        var n = {
            aa: function(a, c) {
                return a ^ c
            },
            bb: function(a, c) {
                return a + c
            },
            cc: function(a, c) {
                return a << c
            },
            dd: function(a, c) {
                return a >>> c
            }
        };
        return n.aa(n.bb(n.aa(t >>> 5, n.cc(c, 2)), n.aa(n.dd(c, 3), n.cc(t, 4))), (a ^ c) + (o[n.aa(3 & e, i)] ^ t))
    }
    function K(a) {
        if (/^[\x00-\x7f]*$captcha/.test(a))
            return a;
        for (var c = [], t = a.length, e = 0, i = 0; e < t; ++e,
            ++i) {
            var o = a.charCodeAt(e);
            if (o < 128)
                c[i] = a.charAt(e);
            else if (o < 2048)
                c[i] = String.fromCharCode(192 | o >> 6, 128 | 63 & o);
            else {
                if (!(o < 55296 || o > 57343)) {
                    if (e + 1 < t) {
                        var n = a.charCodeAt(e + 1);
                        if (o < 56320 && 56320 <= n && n <= 57343) {
                            var r = 65536 + ((1023 & o) << 10 | 1023 & n);
                            c[i] = String.fromCharCode(240 | r >> 18 & 63, 128 | r >> 12 & 63, 128 | r >> 6 & 63, 128 | 63 & r),
                                ++e;
                            continue
                        }
                    }
                    throw new Error("Malformed string")
                }
                c[i] = String.fromCharCode(224 | o >> 12, 128 | o >> 6 & 63, 128 | 63 & o)
            }
        }
        return c.join("")
    }
    this.x = function (a) {
        for (var c = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"], t = "", e = 0; e < a; e++) {
            t += c[Math.floor(35 * Math.random())]
        }
        return t
    }

};
function JDencrypt(sessionId){
    var jd = new JD();
    var e = Date.parse(new Date)
        , i = e % 41
        , r = {};
    r.si = sessionId;
    var ra = "OEBwOFvbxfJgvYzl";
    var c = encodeURI('{ht: 189, wt: 325, x: 116, y: 45}');
    var fp = '~~febac1544efd29848d8022ac95d4980015229140445882299806577360569235!!c90720ac5c58fe79b15ef3d8a23f984a~~057920cc9f896a6ee375d8abe80e01ac~~3.4999999403953552~~24~~~~Arial,BookAntiqua,BookmanOldStyle,Calibri,Cambria,Century,CenturyGothic,CenturySchoolbook,Consolas,Courier,CourierNew,Garamond,Georgia,Helvetica,Impact,LucidaBright,LucidaConsole,LucidaHandwriting,LucidaSans,LucidaSansTypewriter,LucidaSansUnicode,MonotypeCorsiva,MSGothic,MSPGothic,PalatinoLinotype,SegoePrint,SegoeScript,SegoeUI,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings,Symbol,BookshelfSymbol7,Candara,Constantia,Corbel,Ebrima,FangSong,FrenchScriptMT,Gabriola,MicrosoftYaHei,MicrosoftYiBaiti,MingLiUExtB,PMingLiUExtB,SimHei,SimSun,SimSunExtB~~411x823,411x823~~8~~Win32~~-8~~zh-CN~~zh-CN,en-US,en,zh~~0,1,1~~1111';
    var touchList = {"touchList":[{"eid":"click","did":"loginBtn","cn":"btn J_ping btn-active btn-active-disable","sx":339,"sy":317,"px":339,"py":246,"time":1540512009978},{"eid":"click","did":"loginBtn","cn":"btn J_ping btn-active btn-active-disable","sx":339,"sy":317,"px":339,"py":246,"time":1540512009978},{"eid":"click","did":"cpc_img","cn":"","sx":360,"sy":498,"px":360,"py":427,"time":1540512737522},{"eid":"click","did":"cpc_img","cn":"","sx":360,"sy":498,"px":360,"py":427,"time":1540512737522}]};
    r.tk = jd.Z(e + jd.A(r.si.length, 4) + r.si + jd.A(ra.length, 4) + ra + jd.A(c.length, 6) + c + JSON.stringify(touchList) + jd.x(i), "E736B80A35290F193C2034A8021CC63B")
    r.ct = jd.Z(jd.x(e % 19) + jd.A(r.si.length, 4) + r.si + fp + e, "E736B80A35290F193C2034A8021CC63B");
    r.version = 1;
    return r;
}
console.info(JDencrypt('Dh6p8QABAAAAAAAAAAAAMKr55z4eW2slM44f1nyWLPIeJTUH8jB9_WQZVfOTyECAm6aLDLcT6bf1YbHbkmRF1w'));
//console.info(new JD().Z('15405127440000086Dh6p8QABAAAAAAAAAAAAMKr55z4eW2slM44f1nyWLPIeJTUH8jB9_WQZVfOTyECAm6aLDLcT6bf1YbHbkmRF1w0016OEBwOFvbxfJgvYzl000055%7B%22ht%22:236,%22wt%22:406,%22x%22:310,%22y%22:174%7D{"touchList":[{"eid":"click","did":"loginBtn","cn":"btn J_ping btn-active btn-active-disable","sx":339,"sy":317,"px":339,"py":246,"time":1540512009978},{"eid":"click","did":"loginBtn","cn":"btn J_ping btn-active btn-active-disable","sx":339,"sy":317,"px":339,"py":246,"time":1540512009978},{"eid":"click","did":"cpc_img","cn":"","sx":360,"sy":498,"px":360,"py":427,"time":1540512737522},{"eid":"click","did":"cpc_img","cn":"","sx":360,"sy":498,"px":360,"py":427,"time":1540512737522}]}t9vulhbvcyiyp66fqw5n5mencfhpq760yw1px78x', "E736B80A35290F193C2034A8021CC63B"))