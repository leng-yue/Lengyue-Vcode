var Base64 = {
    atob: function(input) {
        input = String(input);
        input = input.replace(/[ \t\n\f\r]/g, '');
        if (input.length % 4 == 0 && /==?$/.test(input)) {
            input = input.replace(/==?$/, '');
        }
        if (input.length % 4 == 1 || !/^[+/0-9A-Za-z]*$/.test(input)) {
            return null;
        }
        var output = '';
        var buffer = 0;
        var accumulatedBits = 0;
        for (var i = 0; i < input.length; i++) {
            buffer <<= 6;
            buffer |= Base64.atobLookup(input[i]);
            accumulatedBits += 6;
            if (accumulatedBits == 24) {
                output += String.fromCharCode((buffer & 0xff0000) >> 16);
                output += String.fromCharCode((buffer & 0xff00) >> 8);
                output += String.fromCharCode(buffer & 0xff);
                buffer = accumulatedBits = 0;
            }
        }
        if (accumulatedBits == 12) {
            buffer >>= 4;
            output += String.fromCharCode(buffer);
        } else if (accumulatedBits == 18) {
            buffer >>= 2;
            output += String.fromCharCode((buffer & 0xff00) >> 8);
            output += String.fromCharCode(buffer & 0xff);
        }
        return output;
    },
    atobLookup: function(chr) {
        if (/[A-Z]/.test(chr)) {
            return chr.charCodeAt(0) - 'A'.charCodeAt(0);
        }
        if (/[a-z]/.test(chr)) {
            return chr.charCodeAt(0) - 'a'.charCodeAt(0) + 26;
        }
        if (/[0-9]/.test(chr)) {
            return chr.charCodeAt(0) - '0'.charCodeAt(0) + 52;
        }
        if (chr == '+') {
            return 62;
        }
        if (chr == '/') {
            return 63;
        }
    },
    btoa: function(s) {
        var i;
        s = String(s);
        for (i = 0; i < s.length; i++) {
            if (s.charCodeAt(i) > 255) {
                return null;
            }
        }
        var out = '';
        for (i = 0; i < s.length; i += 3) {
            var groupsOfSix = [undefined, undefined, undefined, undefined];
            groupsOfSix[0] = s.charCodeAt(i) >> 2;
            groupsOfSix[1] = (s.charCodeAt(i) & 0x03) << 4;
            if (s.length > i + 1) {
                groupsOfSix[1] |= s.charCodeAt(i + 1) >> 4;
                groupsOfSix[2] = (s.charCodeAt(i + 1) & 0x0f) << 2;
            }
            if (s.length > i + 2) {
                groupsOfSix[2] |= s.charCodeAt(i + 2) >> 6;
                groupsOfSix[3] = s.charCodeAt(i + 2) & 0x3f;
            }
            for (var j = 0; j < groupsOfSix.length; j++) {
                if (typeof groupsOfSix[j] == 'undefined') {
                    out += '=';
                } else {
                    out += Base64.btoaLookup(groupsOfSix[j]);
                }
            }
        }
        return out;
    },
    btoaLookup: function(idx) {
        if (idx < 26) {
            return String.fromCharCode(idx + 'A'.charCodeAt(0));
        }
        if (idx < 52) {
            return String.fromCharCode(idx - 26 + 'a'.charCodeAt(0));
        }
        if (idx < 62) {
            return String.fromCharCode(idx - 52 + '0'.charCodeAt(0));
        }
        if (idx == 62) {
            return '+';
        }
        if (idx == 63) {
            return '/';
        }
    }
}

function t(x) {
    for (var n = 0, a = 0; a<4; a++)
        n |= x.charCodeAt(a) << (a*8);
    return isNaN(n) ? 0 : n
}


function decipher(x, j) {
    for (var g = x,c = g[0], l = g[1], a = 84941944608; 0 != a;)
        l -= (c << 4 ^ c >>> 5) + c ^ a + j[a >>> 11 & 3],
        a -= 2654435769,
        c -= ((l << 4 ^ l >>> 5) + l) ^ (a + j[a & 3]);
    x[0] = c;
    x[1] = l;
}

function fxhs_r(c){
   return  c.charCodeAt(0) + c.charCodeAt(1) * 256 + c.charCodeAt(2) * 65536 + c.charCodeAt(3) * 16777216
}

function fxhs_t(n32) {
  return String.fromCharCode(n32 & 0xff) +
	 String.fromCharCode((n32 >>> 8) & 0xff) +
	 String.fromCharCode((n32 >>> 16) & 0xff) +
	 String.fromCharCode((n32 >>> 24) & 0xff);
}

function decrypt(x,n) {
    for (var a = new Array(2), o = new Array(4), _ = "", e = 0; e < 4; e++)
        o[e] = t(n.slice(e * 4, (e + 1) * 4));
    //x = Buffer.from(x, 'base64').toString('binary');
    x = Base64.atob(x);
    for (e = 0; e < x.length; e += 8)
        a[0] = fxhs_r(x.slice(e,e+4)),
        a[1] = fxhs_r(x.slice(e+4,e+8)),
        decipher(a,o),
        _ += fxhs_t(a[0]) + fxhs_t(a[1]);
    return _;
}