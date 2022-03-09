import requests
from bs4 import BeautifulSoup

url = 'https://www.vlive.tv/channel/FE619'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

title = soup.select_one('meta[property="og:image"]')['content']

name = soup.select_one('meta[name="twitter:image"]')['content']

# 아이돌 상세페이지1의 동영상 href 추출을 위한 copy-slector
#root > div > div.layout_main--2iozc > div.layout_content--3-hGQ > div.home--2CVCj > div:nth-child(4) > ul > li:nth-child(1) > div > a


# 아이돌 상세페이지2의 copy-selector
#root > div.modal--1N199 > div > div > div.modal_content--1N9Ky > div > dl > div:nth-child(2) > dd > input

print(name)