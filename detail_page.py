from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
#
from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://test:sparta@cluster0.hekwi.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=certifi.where())
db = client.dbsparta

# 리스트 가져오는것 씀
imgses = list(db.imgs.find({}, {'_id': False}))
for i in imgses:
    id = i['id']
    name = i['name']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.vlive.tv/channel/' + id, headers=headers)
    # 나중에 id값 변수로 설정해서 find로 찾음
    soup = BeautifulSoup(data.text, 'html.parser')
    # meta 태그를 이용하여 아이돌 메인 사진 가져옴
    mainImg = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'name': name,
        'mainImg': mainImg
    }

    # print(doc)
    db.vlive.insert_one(doc)

@app.route('/')
def detail():
    dist = request.args.get('dist');
    return render_template('detail_page.html', dist=dist)
#
@app.route('/detail', methods=["GET"])
def listing() :
   searchDist = request.args.get("district")
   rows = list(db.vlive.find({}, {'_id':False}))
   return jsonify({'all_rows':rows})

@app.route('/')
def offi_site():
    return render_template('detail_page.html')

@app.route('/detail', methods=['GET'])
def listing():
    rows = list(db.vlive.find({}, {'_id': False}))
    return jsonify({'all_rows':rows})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)