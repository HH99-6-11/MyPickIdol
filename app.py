import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

from pymongo import MongoClient
import certifi

SECRET_KEY = 'SPARTA'

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
def offi_site():
    return render_template('main_page.html')

# 채널불러오기
@app.route("/idol", methods=["GET"])
def idol_get():
    all_idol = list(db.imgs.find({}, {'_id': False}))
    return jsonify({'idols': all_idol})\

# 상세페이지 불러오기 구현못함

# 로그인페이지 불러오기
@app.route('/login')
def loginBtn():
    return render_template('login_page.html')

# 로그인,회원가입 기능
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('main_page.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login_page.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 비밀번호를 hash함수 이용해서 hash값을 만들어준다.
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    # username과 password로 일치되는 사람이 있는지 찾는다
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    # 있으면 토큰으로 값을 보낸다
    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60)  # 로그인 1시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 회원가입
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

# 아이디 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)