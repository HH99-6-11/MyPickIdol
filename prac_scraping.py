from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


driver = webdriver.Chrome('./chromedriver')

driver.get("https://www.vlive.tv/channel/FE619")
sleep(3)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')
# href가 들어있는 태그를 먼저 찾고, 그 위 부분의 공통태그를 찾음
images = soup.select(".post_inner--2nG1X .link_post--1FLFt")

for image in images:
    href = image["href"]
    print(href)
