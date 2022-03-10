from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hekwi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


driver = webdriver.Chrome('./chromedriver')

url = "https://www.vlive.tv/channels"
driver.get(url)
sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(1)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')
idoles = soup.select('#content > div > div > div > ul > li')
# print(len(idoles))

for idol in idoles:
    id = idol.select_one('a')['href'].split('/')[2]
    name = idol.select_one('a > div > span.info_area > strong').text
    imgUrl = idol.select_one('a > div >span.thumb.-no_default_img > img')['data-img']
    doc = {
        'id': id,
        'name': name,
        'imgUrl': imgUrl
    }
    # print(doc)
    db.imgs.insert_one(doc)

@app.route('/')
def home():
    return render_template('main_page.html')

# 채널불러오기
@app.route("/idol", methods=["GET"])
def idol_get():
    all_idol = list(db.imgs.find({}, {'_id': False}))
    return jsonify({'idols': all_idol})\

# 상세페이지 불러오기

# 로그인페이지 불러오기
@app.route('/login')
def loginBtn():
    return render_template('login_page.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)