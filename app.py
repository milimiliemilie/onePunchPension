from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from bs4 import BeautifulSoup
import re, demjson

app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

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

pprint.pprint(data)
