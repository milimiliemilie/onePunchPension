import requests
from bs4 import BeautifulSoup
import re, demjson
from pymongo import MongoClient

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'WMONID=sitKQOWTfNO; JSESSIONID=2DirULBpnQ3mq0EzrZvrtvDxupkca50WF3Jt50H6gsJH5QPyVCaVgojVs2avyMwK.amV1c19kb21haW4vbXM0'
}
response = requests.request("GET", 'https://www.moel.go.kr/pension/finance/table-popup-2.do', headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
p = re.compile(r'var mydata = (.*?);', re.DOTALL)
script = soup.select_one('script[type="text/javascript"]:last-child')
m = p.findall(str(script))
data = demjson.decode(m[0])  # data에 금리정보 있음
import pprint

client = MongoClient('localhost', 27017)
db = client.dbsparta

# data 는 각 라인들(=d)을 원소로 갖는 list 이다.
# print(data)

# 위 그림을 예쁘게 보이려고 pprint를 써본다.
# pprint.pprint(data)

# d 는 각각 한 라인이다.
# for d in data:
#     print(d)

# 각 라인에서 company, product 만 빼와보자.
# for d in data:
#     print(d['company'], d['product'])

# KB손보만 제대로 가져와보자.
# 필요한것 : 금리연동형, DB 1/2/3/5, DC/IRP 1/2/3/5

# company name 으로만 검색해보면 이렇다
# - "" / "" / "" / 1.8 / 1.8 / 1.8 이렇게 6개가 다나옴...
# for d in data:
#     if d['company'] == 'KB손보' :
#         floatRate = d['rate']
#         print(floatRate)

# (company name, 상품명) 둘 다 묶어야겠다
# for d in data:
#     if d['company'] == 'KB손보':
#         if d['product'] == '금리연동형(DB)':
#             floatRate = d['rate']
#             print(floatRate)

# 금리연동형들만 뽑아보자. (3개 정도?)
# - KB 손보 / 금리연동형(DB) : 1.8
# - KDB생명 / 금리연동형(DB) : 1.45
# - 교보생명 / (무)교보 금리연동형(DB) : 1.52
# 나온 결과: 1.8 / 1.45 / 1.52
# for d in data:
#     if d['company'] == 'KB손보' and d['product'] == '금리연동형(DB)':
#         floatRate = d['rate']
#         print(floatRate)
#     if d['company'] == 'KDB생명' and d['product'] == '금리연동형(DB)':
#         floatRate = d['rate']
#         print(floatRate)
#     if d['company'] == '교보생명' and d['product'] == '(무)교보 금리연동형(DB)':
#         floatRate = d['rate']
#         print(floatRate)

# listSet = [{'companySet': 'KB손보',
#             'productSet': '금리연동형(DB)'
#             },
#            {'companySet': 'KDB생명',
#             'productSet': '금리연동형(DB)'
#             },
#            {'companySet': '교보생명',
#             'productSet': '(무)교보 금리연동형(DB)'
#             }
#            ]

# 아래의 결과 : KB손보
# print(listSet[0]['companySet'])

# KB손보 금리연동형 금리 나오게 해보자
# for d in data:
#     if d['company'] == listSet[0]['companySet'] \
#             and d['product'] == listSet[0]['productSet']:
#         floatRate = d['rate']
#         print(floatRate)

# 1, 2, 3, 돌아가면서 하려면 어쩌지? ==> range, i 를 쓴다.
# 원하는 결과: 1.8 / 1.45 / 1.52
# for d in data:
#     for i in range(0, 3):
#         if d['company'] == listSet[i]['companySet'] \
#                 and d['product'] == listSet[i]['productSet']:
#             floatRate = d['rate']
#             print(floatRate)

# listSet을 더 정교하게 만들어야겠다.
# - product_floatRate, product_db1y, product_db2y, ... 이런 식으로.

# listSet을 floatRate에 대해서 만들어보자.
# - KB손보를 기준으로 만들어보자.

listSet = [{'companySet': 'KB손보',
            'product_floatRate': '금리연동형(DB)',
            'product_db': 'KB손보 이율보증형(DB)',
            'product_dc': 'KB손보 이율보증형(DC)'
            }
           ]

# 금리적용기간 등은... 공통으로 들어있는 정보라서, 그냥 DB 기준으로 잡았따.

# 이제 db에 저장해보자.
# - DB : db.sparta.penrate
# - doc 에 저장해야 하는딩 ... print 한방에 하는 것처럼 ...

for d in data:
    for i in range(0, 1):
        if d['company'] == listSet[i]['companySet']:
            if d['product'] == listSet[i]['product_floatRate']:
                floatRate = d['rate']

            if d['product'] == listSet[i]['product_db']:
                db1y = d['val12']
                db2y = d['val24']
                db3y = d['val36']
                db5y = d['val60']

                gubun = d['gubun']
                period = d['period']
                bank_check = d['bank_check']

            if d['product'] == listSet[i]['product_dc']:
                dc1y = d['val12']
                dc2y = d['val24']
                dc3y = d['val36']
                dc5y = d['val60']
            print(floatRate)

# print(floatRate만 잘 되면...
# doc = {
#     'floatRate': floatRate,
#     'db1y': db1y,
#     'db2y': db2y
# }
# 이런 식으로 바꿔넣어서...
# db ... insert_one(doc) 해야지..