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
    rates = list(db.penrate.find({}, {'_id': 0}).sort("floatRate", pymongo.DESCENDING))

    # filter_receive = request.args['product']

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

