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


@app.route('/filtered', methods=['GET'])
def show_rates_filtered():

    srchYear_receive = int(request.args['srchYear_give'])
    srchMonth_receive = int(request.args['srchMonth_give'])
    print(srchYear_receive)
    print(srchMonth_receive)


    product_receive = request.args['product_give']
    print(product_receive)

    # gubun: gubun_all / gubun_ins
    gubun_receive = request.args['gubun_give']
    print(gubun_receive)

    if gubun_receive == 'gubun_all':
        rates = list(
            db.penrate.find({'srchYear': srchYear_receive, 'srchMonth': srchMonth_receive}, {'_id': 0}).sort(product_receive, pymongo.DESCENDING))

        result = {
            'result': 'success',
            'rates': rates,
        }

        pprint.pprint(result)

        return jsonify(result)

    elif gubun_receive == 'gubun_ins':
        rates_ins = list(db.penrate.find({'gubun': {'$in': ['생보', '손보']}}, {'_id': 0}).sort(product_receive, pymongo.DESCENDING))
        rates_bank = list(db.penrate.find({'gubun': '은행'}, {'_id': 0}).sort(product_receive, pymongo.DESCENDING))

        result = {
            'result': 'success',
            'rates_ins': rates_ins,
            'rates_bank': rates_bank
        }

        pprint.pprint(result)

        return jsonify(result)

    else:
        print('에러입니다')


    # "gubun = 손보이거나 생보" 인 애들을 찾아와서 descending 하고 싶은데, 그게 안된다 힝
    rates = list(
        db.penrate.find({'gubun': {'$in': ['생보', '손보']}}, {'_id': 0}).sort(product_receive, pymongo.DESCENDING))

    result = {
        'result': 'success',
        'rates': rates,
    }
    pprint.pprint(result)

    return jsonify(result)


# 이 아래는 제일 밑으로.
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
