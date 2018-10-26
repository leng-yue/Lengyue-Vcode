var jd = {
fp: function(c) {
        var a = [];
        for (var b in c) {
            a.push(encodeURIComponent(b) + "=" + encodeURIComponent(c[b]))
        }
        a.push(("v=" + Math.random()).replace(".", ""));
        return a.join("&")
    },
    st: function(d) {
        var c = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-~".split("")
          , b = c.length
          , e = +d
          , a = [];
        do {
            mod = e % b;
            e = (e - mod) / b;
            a.unshift(c[mod])
        } while (e);return a.join("")
    },
    pi: function(a, b) {
        return (Array(b).join(0) + a).slice(-b)
    },
    pm: function(d, c, b) {
        var f = this;
        var e = f.st(Math.abs(d));
        var a = "";
        if (!b) {
            a += (d > 0 ? "1" : "0")
        }
        a += f.pi(e, c);
        return a
    },
    encrypt: function(c) {
        var g = this;
        var b = new Array();
        for (var e = 0; e < c.length; e++) {
            if (e == 0) {
                b.push(g.pm(c[e][0] < 262143 ? c[e][0] : 262143, 3, true));
                b.push(g.pm(c[e][1] < 16777215 ? c[e][1] : 16777215, 4, true));
                b.push(g.pm(c[e][2] < 4398046511103 ? c[e][2] : 4398046511103, 7, true))
            } else {
                var a = c[e][0] - c[e - 1][0];
                var f = c[e][1] - c[e - 1][1];
                var d = c[e][2] - c[e - 1][2];
                b.push(g.pm(a < 4095 ? a : 4095, 2, false));
                b.push(g.pm(f < 4095 ? f : 4095, 2, false));
                b.push(g.pm(d < 16777215 ? d : 16777215, 4, true))
            }
        }
        return b.join("")
    }
}

function RandomNum(min, max) {
    return Math.floor(Math.random()*(max-min)) + min + 1
}

function RandomChoice(arr) {
    return arr[Math.floor(Math.random()*arr.length)]
}

function getTrace(distance){
    distance = Math.floor(distance);
    var trace = [];
    var sy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0];
    var st = [15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17,
        18, 15, 16, 17, 18, 15, 16, 17, 18, 15, 16, 17, 18, 14, 16, 17, 18, 16, 17, 18, 19, 20, 17];
    //items[Math.floor(Math.random()*items.length)]

    if (distance < 95) {
        var sx = [1, 2, 1, 2, 1, 2, 1, 1, 2, 1];
    }else{
        var sx = [1, 2, 1, 2, 1, 2, 2, 2, 3, 4];
    }
    var zt = new Date().getTime() - 2000;
    trace.push(["672", "341", zt]);
    var baseX = 36,
        baseY = 415,
        zx = 0,
        zy = 0;
    var random_x = RandomNum(9, 14);
    trace.push([""+baseX, ""+ baseY, zt]);
    var n = 0, x=0, y=0, t=0;
    while (true){
        n += 1;
        if (n < 5){
            x = 1;
        }else{
            x = RandomChoice(sx)
        }
        if (distance > 125 && random_x === n){
            x = RandomNum(14, 18)
        }
        y = RandomChoice(sy);
        t = RandomChoice(st);
        zx += x;
        zy += y;
        zt += t;
        trace.push([""+(zx + baseX), ""+ (zy+baseY), zt]);
        if (distance - zx < 6){
            break;
        }
    }
    var value = distance - zx;
    for (var i = 0; i < value; i++){
        t = RandomChoice(st);

        if (value === i + 1){
            t = RandomNum(42, 56)
        }
        if (value === i + 2){
            t = RandomNum(32, 38)
        }
        if (value === i + 3){
            t = RandomNum(30, 36)
        }
        x = 1;
        zx += x;
        zt += t;
        trace.push([""+(zx + baseX), ""+ (zy+baseY), zt]);
    }
    t = RandomNum(100, 200);
    zt += t;
    trace.push([""+(zx + baseX), ""+ (zy+baseY), zt]);
	return trace;
}

//console.info(jd.encrypt([["672","393",1540448662141],["24","425",1540448662141],["26","426",1540448662202],["28","426",1540448662214],["36","427",1540448662230],["48","430",1540448662248],["62","432",1540448662264],["67","433",1540448662281],["70","433",1540448662297],["75","433",1540448662314],["78","433",1540448662331],["80","433",1540448662349],["84","434",1540448662365],["89","434",1540448662381],["99","434",1540448662398],["101","435",1540448662416],["104","435",1540448662433],["106","435",1540448662448],["108","435",1540448662465],["110","435",1540448662482],["112","436",1540448662498],["113","436",1540448662515],["113","437",1540448662531],["116","437",1540448662549],["120","438",1540448662564],["123","438",1540448662581],["125","438",1540448662597],["127","438",1540448662614],["128","438",1540448662631],["129","438",1540448662648],["132","438",1540448662664],["134","438",1540448662682],["135","438",1540448662698],["136","438",1540448662715],["137","438",1540448662732],["138","438",1540448662748],["139","438",1540448662770],["140","438",1540448662786],["140","438",1540448662809],["141","438",1540448662882],["143","438",1540448663198],["144","438",1540448663216],["144","438",1540448663237],["144","438",1540448663631]]));