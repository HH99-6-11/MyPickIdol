from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hekwi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.vlive.tv/channels', headers=headers)
# content > div.channel_wrap > div > div.inner > ul > li:nth-child(1) > a > div > span.thumb.-no_default_img > img
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
idoles = soup.select('#content > div.channel_wrap > div > div.inner > ul > li')
for idol in idoles:
    id = idol.select_one('a')['href'].split('/')[2]
    name = idol.select_one('div > span > strong').text
    image = idol.select_one('a > div >span.thumb.-no_default_img > img')['src']

    doc = {
        'id': id,
        'name': name,
        'image': image,

    }
    db.imge.insert_one(doc)


@app.route('/')
def home():
    return render_template('main.html')


@app.route("/idol", methods=["GET"])
def idol_get():
    all_idol = list(db.imge.find({}, {'_id': False}))
    return jsonify({'idolse': all_idol})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
