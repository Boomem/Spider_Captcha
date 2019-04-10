# -*- coding: utf-8 -*-
import base64
import zlib
import json
from urllib import parse
import requests
import re
import time


##### 解码_token,参数sign也可用
# token2 = "eJx1j0uPokAUhf9LbSFWAVX4SGYBDSp2gwiKSKcXgAxFKchLaHsy/32qE2cxi1mdc797cnLvL9BaZ7CQEJojJIIha8ECSBM0UYEI+o5vCMHKVCFzPJewCNJ/GEGYs6QNDLB4l/AciYqCPr6Jx8G7RBRVnKn4Q3xamVsZi98CEotHAO37ultAGHeTMiv6e1xN0lsJue9oAfkN/wkA3lDueQPXy1Pjp/Z/Z5v/wiu6Iq+4yzbjlXV3R2Pmzlu7FL861WB/ri231LYvKzockWZkqi7dMIzbc2jl1Jf10SpyJzptDTlYN02TH8axm0YBlfSZZl+uMhxjHUIJDn1NH8v87eFsUrqir3d2om+PzVFgO7k/REbtCdt1VF0CP2SpE21lrzaN3adQJI/harNDPWbDZXNcNcwJBMNnrrV0qrB8qeB0MF0yu5HuSgO7nVZ+s1QTozl9deZ4Prg/WZroZ03vhZYkrIzJqg299ojDvbJ3fM38AX7/Aaowk5A="
# #             eJx1j01vqkAARf+KOxY0Dh8zqE3eAgoqtiCCItJ0AUgZRkFgEGqb/vfHNGmbt3iLSc49c3Mz88E15pG7H4mCMBOEuxHXpc0QOXEsjBVuyC1ltwhBeSKjGZyJcJDJvxYJkNm48fVBP4twNizJsvDyJV3mnkUkK3ejqQIH+R0kFiTIzlfVZE0Ot21F7wGI6LhI8/YalePkUoCBKc4Be9N/GhwbKbZshNHph6Ifan+dxb7J1mielYzTVX8m9GqrxNi4SwfDR7vsrLel6RTq+mGBu72g6qmiiRcIouYYmBn2JK0388wOD2td8pd1XWe7vqeT0MeiNlWt01kCfaQBIIKurfBtnj3d7FWCF/jxSg746bba82QjtbtQr1x+vQzLk+8FJLHDteRWhr554/P41p0tsqv6tDut9oua2D6ve8Qx53YZFA8lmHSGg6YXRM/Yt5pJ6dVzJdbrwzs1+uPOeSVJrB1VreUbFJMiQosmcJs9DLby1vZU4w/3+ReV5JhE
#
# token = "eJwljsuNAjEQRHPh4KNnvMxHIPmAOCGhvW0ADe6B1o4/ardXIghS2BwIigNZYOD2VHqqqgUwws7ZVh1B8AMkl2/waB//1/vtphyFgLyNJchGhKujYhLyJW+jQ2tUZDpR+OHZnkVSXjcNZO2RpEDQx+ibyvlMjUpwevkJWGqjNV+DSjPIFNnXmCn/7vEP58o5slhVMr7nSqF6bDqYzsEwdUPfjcbBdABt+r5bjma5GrXRrW4XT3TNSAE="
# token = "eJx1j0tvgkAUhf/LbCHIMMMAJl0gaoqK+EBia1wgg7yRp6hN/3vHxC666Oo799yTk3u/QG1SMISiqIkiD65BDYYACqJAAA/ahm1kGauKoipY1TQe+H88GSHIg1PtjsHwALGGeUlEx6ezYcYByojwKsFH/iUlJiUWws+MySIgatuyGQ4GXiPkQdx2XiH4l3zAdBPFA3bDPwHAGnKHNTCmL3ovtr+zxX5hFU0cFkwFsz5LHNjpyWS96TQD01nd3O9NOu3DKo02XXQLE93/aM7KJhj1ZaSGrh/6drado1hfUZEEhUYkfeISw+IukzBVQ25/H8e2gjjuWpyzYLRLTU4uT6lpLeiO4eZ6K9szHvNkSecL9MAVjsuAvOteZW+XZkhc215zlJS7idutHsrIjYhIC+iWu6k862WtzEuUKTddPtvLk4Xh9sIpWZXgRY/odY1Hj7Hz2dHivTdg4Z2W18U+kfKqThyvXqGcbA3rDXz/AA65kvo="
# token = "eJwljT1uAjEQRu9C4dJrsyyskFwgqkhRuhxgjAcYsf7ReBwph8gVcgcOlSK3iAPd06en962AEV6CM+oEgk8g+XyDiO73++vnfleBUkI+5pbkIMLdUbkIxVaPOaCzKjNdKL3z4q4ipe6HAaqOSNIg6VOOQ+d6pUEVuPz7BVh60dn1VpUF5Jw59pmp3l7xA5fONbM41So+7lqj4Lw3dvQ4BzDTZudnHwC1nabNvLXj2mqrjTarP3m6SCM="
# token = parse.unquote(token)
# token_decode = base64.b64decode(token)
# print(token_decode)
# token_string = zlib.decompress(token_decode).decode()
# print(token_string)
# token_dict = json.loads(token_string)
# print(token_dict)
# for type in token_dict:
#     print(type, token_dict[type])


# ip是一些固定参数和浏览器屏幕宽高等信息，不完整参数，关键参数sign在下面
ip = {
    "rId":100900,
    "ver":"1.0.6",
    "ts":int(time.time()*1000),
    "cts":int(time.time()*1000)+95,
    "brVD":[1490,330],
    "brR":[[1536,864],[1536,824],24,24],
    "bI":["https://as.meituan.com/meishi/","https://as.meituan.com/"],
    "mT":[],
    "kT":[],
    "aT":[],
    "tT":[],
    "aM":"",
}


headers = {
    # "Upgrade-Insecure-Requests": "1",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Host": "as.meituan.com",
    # "Accept": "application/json",
    "Referer": "https://as.meituan.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    # "Cookie": "_lxsdk_cuid=169e7c15059c8-0bd81d9bb9ab4-7a1437-144000-169e7c15059c8;uuid=bb013be8da0547b8bdae.1554861321.1.0.0; ci=151; rvct=151; iuuid=94BB725E734A5F5B5D9226DEFD90D35B90D0B1AB2304A8C9B17F7B0B4ACC00AE; cityname=%E9%9E%8D%E5%B1%B1; _lxsdk=94BB725E734A5F5B5D9226DEFD90D35B90D0B1AB2304A8C9B17F7B0B4ACC00AE; client-id=fb6d6bc3-9ead-4995-b33f-84f0dd171f63; mtcdn=K; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=149330441.1554371403989.1554800875918.1554861324493.9; _lxsdk_s=16a05d8bedb-13c-0b-f3%7C%7C4"
}

response = requests.get("https://as.meituan.com/meishi/",headers=headers)
# with open("a.html","w",encoding="utf-8") as f:
#     f.write(response.text)
uuid = re.findall('"uuid":"(.*?)"',response.text)[0]
print("uuid:",uuid)

# page,cityName等参数此处修改
params = {
    "cityName": "鞍山",
    "cateId": "0",
    "areaId": "0",
    "sort": "",
    "dinnerCountAttrId": "",
    "page": "2",
    "userId": "",
    "uuid": uuid,
    "platform": "1",
    "partner": "126",
    "originUrl": "https://as.meituan.com/meishi/",
    "riskLevel": "1",
    "optimusCode": "1",
}
url = "https://as.meituan.com/meishi/api/poi/getPoiList"
# url = "https://as.meituan.com/meishi/api/poi/getPoiList?cityName=%E9%9E%8D%E5%B1%B1&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=2&userId=&uuid={}&platform=1&partner=126&originUrl=https%3A%2F%2Fas.meituan.com%2Fmeishi%2F&riskLevel=1&optimusCode=1".format(uuid)
p = parse.unquote(url)
# print(p)

def url2jv(p):
    # pdic = {}
    # p2 = p.split("?")[1]
    # for i in p2.split("&"):
    #     # print(i)
    #     k, v = i.split("=")
    #     pdic[k] = v

    pp = []
    for k, v in sorted(p.items()):
        pp.append(k + "=" + v)
    # print(len(pp))

    return '"{}"'.format("&".join(pp))

jv = url2jv(params)
print("jv:",jv)

def string2base64(p):
    # 压缩，字符串时不需要转换为json去除空格
    if type(p) is str:
        t = zlib.compress(p.encode())
    else:
        # 容易出错，注重点
        # ip为字典，加密参数为json格式装换为字符串并转为二进制，使用json直接dumps会出现空格，所以要替换，
        t = zlib.compress(str(json.dumps(p)).replace(" ","").encode())
    # base64加密
    b = base64.b64encode(t)
    return b.decode()

# sign 通过 url 的参数字典排序后压缩并进行base64加密
sign = string2base64(jv)
print("sign:",sign)
# 将_token加密的参数补全
ip["sign"] = sign
print("ip:",ip)
# 生成_token，方法与sign相同
_token = string2base64(ip)
print("_token:",_token)
#### 注重点！！！！！！！！！！！！！！！！！！！！！_token必须为url编码
# url += "&_token={}".format(parse.quote(_token))
params["_token"] = parse.quote(_token)
# print(url)

# headers["Cookie"] += "; uuid={}".format(uuid)
res = requests.get(url,headers=headers,params=params)
print(res.text)