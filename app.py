from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://test:sparta@cluster0.hekwi.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=certifi.where())
db = client.dbsparta

# ## HTML을 주는 부분
# @app.route('/')
# def home():
#    return render_template('index.html')
#
# @app.route('/memo', methods=['GET'])
# def listing():
#     vlive = list(db.vlive.find({}, {'_id': False}))
#     return jsonify({'id':id})
#
# ## API 역할을 하는 부분
# @app.route('/memo', methods=['POST'])
# def saving():
#     url_receive = request.form['url_give']
#     comment_receive = request.form['comment_give']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.vlive.tv/channel/FE619', headers=headers)
# 나중에 id값 변수로 설정해서 find로 찾음

soup = BeautifulSoup(data.text, 'html.parser')

# meta 태그를 이용하여 아이돌 메인 사진 가져옴
imgUrl = soup.select_one('meta[property="og:image"]')['content']

doc ={
        'imgUrl':imgUrl
}
#몽고디비에 imgUrl로 저장
db.vlive.insert_one(doc)

# lis = soup.select('#content > div.channel_wrap > div > div.inner > ul > li')
# #
# for li in lis:
#         a_tag = li.select_one('a')
#         if a_tag is not None:
#                 id = li.select_one('div > span.info_area > strong').text
#                 imgUrl = li.select_one('div > span.thumb.-no_default_img > img')['data-img']
#                 doc = {
#                         'id': id,
#                         'imgUrl': imgUrl
#                 }
#                 db.vlive.insert_one(doc)



#root > div > div.layout_main--2iozc > div.layout_content--3-hGQ > div.home--2CVCj 브이앱전체
#root > div > div.layout_main--2iozc > div.layout_content--3-hGQ > div.home--2CVCj > div.channel_home_main_banner--MCl68 브이앱사진
#root > div > div.layout_main--2iozc > div.layout_content--3-hGQ > div.home--2CVCj > div:nth-child(4) > ul > li:nth-child(1) > div > a > div.content_area--2APUB > div > div > div 브이앱영상


# divs = soup.select('#root > div > div.layout_main--2iozc > div.layout_content--3-hGQ > div.home--2CVCj > div')
# #뷰티풀숩을 이용하여 아이돌별 브이라이브 채널의 사진과 동영상 페이지를 긁어 올 수 있는 코드 카피 셀렉터 함.
# for div in divs:
#         imgUrl = div.select_one('div.channel_home_main_banner--MCl68').style="background-image: url"
#         print(imgUrl)


        # videoUrl = div.select.one('div:nth-child(4) > ul > li:nth-child(1) > div > a > div.content_area--2APUB > div > div > div')['background-image: url("")']

        # doc = {
        #       'imgUrl': imgUrl,
        #       # 'videoUrl': videoUrl
        #       }
        #
        # db.vlive.insert_one(doc)


#       id = soup.select('#content > div.channel_wrap > div > div.inner > ul > li')
#     title = soup.select_one('meta[property="og:title"]')['content']
#     sequence = soup.select_one('meta[property=""]')['content']
#     videoUrl = soup.select_one('meta[property=""]')['content']

# idol = db.vlive.find_one({'id':'BTS'},{'_id':False})
# target_Url = idol['imgUrl']
#
# target_idols = list(db.vlive.find({'imgUrl':target_Url},{'_id':False}))
#
# for target in target_idols:
#         print(target['id'])



#     #
#     # return jsonify({'msg':'저장이 완료되었습니다!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)