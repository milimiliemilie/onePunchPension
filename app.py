import pprint

import pymongo
from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from bs4 import BeautifulSoup

app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/rates', methods=['GET'])
def show_rates():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    # 조건 없이 다 검색한다 ==> {}
    # _id 는 다 뺴고 가져와라 ==> {'_id': 0}
    rates = list(db.penrate.find({}, {'_id': 0}).sort("db1y", pymongo.DESCENDING))

    # 2. articles라는 키 값으로 articles 정보 보내주기
    result = {
        'result': 'success',
        'rates': rates,
    }
    return jsonify(result)

@app.route('/rates/filtered', methods=['GET'])
def show_rates_filtered():
    # 아래대로 하면 ...
    # URL : localhost:5000/query?product_receive=floatRate ... 라고 직접 입력했을 때
    # floatRate 순서대로 내려가게 될 것인디...
    # request.args['product']에 들어갈게 floatRate이라고 끌어올 방법이 없을까?
    # (URL에 직접 치지 말고, 드롭다운에서 선택해서)

    field = request.args['product_give']
    print(field)
    # condition 하나 만들어 보고...
    # 잘 되면, condition에 pair를 하나 더 추가해야겠다.
    # condition = {
    #     'year': year_receive,
    #     'month': month_receive,
        # 'gubun': gubun_receive,
        # 'product': product_receive
    # }

    # '머 = 머' 인 값을 찾아오라, 이게 아니라
    # '머' 를 기준으로 소팅해라, 이건뎅...
    rates = list(db.penrate.find({}, {'_id': 0}).sort(field, pymongo.DESCENDING))

    # 2. articles라는 키 값으로 articles 정보 보내주기
    result = {
        'result': 'success',
        'rates': rates,
    }
    pprint.pprint(result)

    return jsonify(result)

# 이 아래는 제일 밑으로.
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

