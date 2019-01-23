import requests
from bs4 import BeautifulSoup

url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')
tags = soup.select("#content > div > div.article > div > div > table > tbody > tr > td > a")
#根据CSS路径查找标签信息，CSS路径获取方法，右键-检查-copy selector，tags返回的是一个列表

# for td in soup.find_all(name='td'):
#     for a in td.find_all(name='a'):
#         print(a.string)

channels = []
for tag in tags:
    tag = tag.get_text()
    helf = "https://book.douban.com/tag/"
    url = helf + str(tag)
    channels.append(url)

