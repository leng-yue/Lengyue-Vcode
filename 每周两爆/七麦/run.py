"""
Author: Lengyue
Date: 2018-10-15
Project: Crack Qimai
https://www.qimai.cn/rank/index/brand/free/genre/36/device/iphone/country/cn/date/2018-10-15
"""

import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}

# Step 1, Init params
params = {
    "brand": "all",
    "device": "iphone",
    "country": "cn",
    "genre": "36",
    "date": "2018-10-15"
}
url = "/rank/indexPlus/brand_id/0"
# Lengyue JS Online execute
js_code = "qimaiEncrypt('%s',%s)" % (url, json.dumps(params))
print(js_code)
response = requests.post(
    "https://lengyue.me/api/execute.php?type=qimai",
    data={
        "eval": js_code
    }
)

params["analysis"] = response.text

# Step 2 requests
response = requests.get(
    "https://api.qimai.cn" + url,
    headers=headers,
    params=params
)
print("Response", response.text)
