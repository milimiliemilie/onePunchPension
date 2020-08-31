import requests
from bs4 import BeautifulSoup
import re, demjson
from pymongo import MongoClient
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

listSet = [
    {'companySet': 'BNK경남은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': '퇴직연금 전용 정기예금(DB)',
     'product_dc': '퇴직연금 전용 정기예금(DC/IRP)'
     },
    {'companySet': 'DB생명',
     'coNum': '',
     'product_floatRate': '무배당 동부 자산관리 퇴직연금보험 금리연동형(DB)',
     'product_db': '무배당 동부 자산관리 퇴직연금보험 이율보증형(DB)',
     'product_dc': '무배당 동부 자산관리 퇴직연금보험 이율보증형(DC)'
     },
    {'companySet': 'DB손보',
     'coNum': '',
     'product_floatRate': '프로미 금리연동형보험(DB)',
     'product_db': '프로미 원리금보장형보험(DB)',
     'product_dc': '프로미 원리금보장형보험(DC)'
     },
    {'companySet': 'IBK기업은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': 'IBK퇴직연금 정기예금(DB)',
     'product_dc': 'IBK퇴직연금정기예금(DC/IRP)'
     },
    {'companySet': 'IBK연금보험',
     'coNum': '',
     'product_floatRate': '',
     'product_db': 'IBK연금보험 이율보증형(DB)',
     'product_dc': 'IBK연금보험 이율보증형(DC)'
     },
    {'companySet': 'KB국민은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': 'KB퇴직연금정기예금(DB)',
     'product_dc': 'KB퇴직연금정기예금(DC/IRP)'
     },
    {'companySet': 'KB손보',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': 'KB손보 이율보증형(DB)',
     'product_dc': 'KB손보 이율보증형(DC)'
     },
    {'companySet': 'KDB산업은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': 'KDBpension정기예금(DB)',
     'product_dc': 'KDBpension정기예금(DC/IRP)'
     },
    {'companySet': 'KDB생명',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': 'KDB생명 이율보증형(DB)',
     'product_dc': '금리연동형(DB)'
     },
    {'companySet': 'KEB하나은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': '퇴직연금용 정기예금(DB)',
     'product_dc': '퇴직연금용 정기예금(DC/IRP)'
     },
    {'companySet': 'NH농협은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': '퇴직연금정기예금(DB)',
     'product_dc': '퇴직연금정기예금(DC/IRP)'
     },
    {'companySet': '광주은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': '퇴직연금전용정기예금(DB)',
     'product_dc': '퇴직연금전용정기예금(DC/IRP)'
     },
    {'companySet': '교보생명',
     'coNum': '',
     'product_floatRate': '(무)교보 금리연동형(DB)',
     'product_db': '교보생명 이율보증형보험(DB)',
     'product_dc': '교보생명 이율보증형보험(DC)'
     },
    {'companySet': '동양생명',
     'coNum': '',
     'product_floatRate': '동양생명 금리연동형(DB)',
     'product_db': '동양생명 이율보증형(DB)',
     'product_dc': '동양생명 이율보증형(DC)'
     },
    {'companySet': '롯데손보',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '롯데손보 이율보증형(DB)',
     'product_dc': '롯데손보 이율보증형(DC)'
     },
    {'companySet': '미래에셋생명',
     'coNum': '',
     'product_floatRate': '(무)미래에셋생명금리연동형(DB)',
     'product_db': '미래에셋생명 이율보증형(DB)',
     'product_dc': '미래에셋생명 이율보증형(DC)'
     },
    {'companySet': '삼성생명',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '삼성생명 이율보증형(DB)',
     'product_dc': '삼성생명 이율보증형(DC)'
     },
    {'companySet': '삼성화재',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '삼성화재 이율보증형(DB)',
     'product_dc': '삼성화재 이율보증형(DC)'
     },
    {'companySet': '신한생명',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '신한생명 이율보증형(DB)',
     'product_dc': '신한생명 이율보증형(DC)'
     },
    {'companySet': '신한은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': 'Tops퇴직플랜정기예금(DB)',
     'product_dc': 'Tops퇴직플랜정기예금(DC/IRP)'
     },
    {'companySet': '우리은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': '퇴직연금 전용 정기예금(DB)',
     'product_dc': '퇴직연금 전용 정기예금(DC/IRP)'
     },
    {'companySet': '전북은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': '퇴직연금정기예금(DB)',
     'product_dc': '퇴직연금정기예금(DC/IRP)'
     },
    {'companySet': '제주은행',
     'coNum': '',
     'product_floatRate': '',
     'product_db': '퇴직연금정기예금(DB)',
     'product_dc': '퇴직연금정기예금(DC/IRP)'
     },
    {'companySet': '하나생명',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '이율보증형(DB)',
     'product_dc': '이율보증형(DC)'
     },
    {'companySet': '한화생명',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '한화생명 이율보증형(DB)',
     'product_dc': '한화생명 이율보증형(DC)'
     },
    {'companySet': '한화손보',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '한화손보 이율보증형(DB)',
     'product_dc': '한화손보 이율보증형(DC)'
     },
    {'companySet': '현대라이프',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '현대라이프 이율보증형(DB)',
     'product_dc': '현대라이프 이율보증형(DC)'
     },
    {'companySet': '현대해상',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '현대해상 이율보증형(DB)',
     'product_dc': '현대해상 이율보증형(DC)'
     },
    {'companySet': '흥국생명',
     'coNum': '',
     'product_floatRate': '금리연동형(DB)',
     'product_db': '흥국생명 이율보증형(DB)',
     'product_dc': '흥국생명 이율보증형(DC)'
     }
]


# 금리적용기간 등은... 공통으로 들어있는 정보라서, 그냥 DB 기준으로 잡았따.

# 이제 db에 저장해보자.
# - DB : db.sparta.penrate
# - doc 에 저장해야 하는딩 ... print 한방에 하는 것처럼 ...

def to_float(rawRate):
    try:
        return float(rawRate)
    except ValueError:
        return 0


# print(to_float('1.1'))
# print(to_float(''))

def insert_rate(data):
    for i in range(0, len(listSet)):
        for d in data:
            if d['company'] == listSet[i]['companySet']:
                if listSet[i]['product_floatRate'] != "":
                    if d['product'] == listSet[i]['product_floatRate']:
                        floatRate = float(d['rate'])
                else:
                    floatRate = 0
                if d['product'] == listSet[i]['product_db']:
                    db1y = to_float(d['val12'])
                    db2y = to_float(d['val24'])
                    db3y = to_float(d['val36'])
                    db5y = to_float(d['val60'])

                    gubun = d['gubun']
                    period = d['period']
                    bank_check = d['bank_check']

                    # period 예시: 20.08.01~20.08.31
                    # srchYear: to_float('20' + period의 앞 두글자)
                    srchYear = int('20' + d['period'][:2])
                    # srchMonth: to_float(period의 중간 두글자 (네번째부터 두 개))
                    srchMonth = int(d['period'][3:5])

                if d['product'] == listSet[i]['product_dc']:
                    dc1y = to_float(d['val12'])
                    dc2y = to_float(d['val24'])
                    dc3y = to_float(d['val36'])
                    dc5y = to_float(d['val60'])
        doc = {
            'coNum': listSet[i]['coNum'],
            'coName': listSet[i]['companySet'],
            'floatRate': floatRate,
            'db1y': db1y,
            'db2y': db2y,
            'db3y': db3y,
            'db5y': db5y,
            'dc1y': dc1y,
            'dc2y': dc2y,
            'dc3y': dc3y,
            'dc5y': dc5y,
            'gubun': gubun,
            'period': period,
            'bank_check': bank_check,
            'srchYear': srchYear,
            'srchMonth': srchMonth
        }
        # db.penrate.insert_one(doc)
        print(doc)

# 이 아래로 크롤링

url = "https://www.moel.go.kr/pension/finance/rate2.do"

years = list(range(2017, 2020))  # 2017 ~ 2019
months = list(range(1, 13))  # 1 ~ 12

# for srchYear in years:
#     for srchMonth in months:
#         print(srchYear, srchMonth)


# 2016. 2 ~ 12 월 : 별도 수행
# 2020. 1 ~ 8 월 : 별도 수행

for srchYear in [2020]:
    for srchMonth in list(range(1, 9)):
        payload = 'srchMonth=' + str(srchMonth) + '&srchWord=&srchYear=' + str(srchYear) + '&url=on'

        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://www.moel.go.kr',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        p = re.compile(r'var mydata = (.*?);', re.DOTALL)
        script = soup.select_one('script[type="text/javascript"]:last-child')
        m = p.findall(response.text)

        data = demjson.decode(m[0])

        insert_rate(data)

        print(str(srchYear) + '.' + str(srchMonth) + '. 완료')



# 숫자로 만드는 게 또 관건이네 ...

