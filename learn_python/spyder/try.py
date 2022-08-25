import requests
import json

headers = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
post_data = {
    'query': '我爱你啊',
    'from': 'zh',
    'to': 'en',
    'token': '4a870736fce5eb0c373fc2719b1190e6',
    # 'sign': '47194.285547'
}

post_url = 'https://fanyi.baidu.com/basetrans'

r = requests.post(post_url, data=post_data, headers=headers)

# dict_ret = json.loads(r.content.decode())
# ret = dict_ret[]
print(r.json())
