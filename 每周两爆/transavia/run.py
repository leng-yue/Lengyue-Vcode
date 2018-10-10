"""
Author: Lengyue
Date: 2018-10-06
Project: Crack transavia
https://www.transavia.com/en-EU/book-a-flight/flights/search/
"""

import requests
import re
import execjs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}
_JS = execjs.compile(open("./transavia.js", "r").read()) # 初始化JS
s = requests.Session()


# Step 1, Get xpid
response = s.get(
    "https://www.transavia.com/en-EU/book-a-flight/flights/search/",
    headers=headers
)
xpid = re.findall(r'xpid:"(.*?)"', response.text)[0]
print("xpid", xpid)

# Step 2, Get ajaxHeader
response = s.get(
    "https://www.transavia.com/cczkbrpmtnvieywa.js",
)
ajaxHeader = re.findall(r'ajax_header:"(.*?)"', response.text)[0]
print("ajaxHeader", ajaxHeader)

# Step 3, Post data
headers.update({
    "X-Distil-Ajax": ajaxHeader,
    "X-Newrelic-Id": xpid
})

response = s.post(
    "https://www.transavia.com/cczkbrpmtnvieywa.js?PID=AE0B5200-B697-3A18-A6EE-B30DF08C55FA",
    headers=headers,
    data="p=" + _JS.call("generateFingerprint")
)
print(response.status_code)
print(response.cookies)

