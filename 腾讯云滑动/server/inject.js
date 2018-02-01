function getList(a,b){
	var ans=[];
	var sb={};
    for(var i=0; i < a.length; i++){
        ans.push([a[i],b[i],{%replace%}(a[i],b[i])]);
        sb[a[i]] = {%replace%}(a[i],b[i]);
    }
	return [ans,sb];
}
function getFPS(raw) {
    var w = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    for (var x = [], n = 0; n < raw.length; n++)
        raw[n] && (x[Math.floor(n / 6)] ^= 1 << (n % 6));
    for (n = 0; n < x.length; n++)
        x[n] = w.charAt(x[n] || 0);
    return x.join("")
}