import requests
import pymysql
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import time
import random
import channel   #这是我们第一个程序爬取的链接信息

headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3)AppleWebKit/537.36(KHTML,like Gecko)Chrome/65.0.3325.162 Safari/537.36',
}
max_page = 10

db = pymysql.connect(host='localhost', user='root', password='25015557', db="spiders", port=3306)
cursor = db.cursor()
cursor.execute('DROP TABLE IF EXISTS allbooks')  # 如果数据库中有allbooks的表则删除
sql = """CREATE TABLE allbooks(
        title CHAR(255) NOT NULL,
        score CHAR(255),
        author CHAR(255),
        translator CHAR(255),
        publish CHAR(255),
        time CHAR(255),
        price CHAR(255),
        brief CHAR(255),
        tag CHAR(255)
 )"""
cursor.execute(sql)  # 执行sql语句，新建一个allbooks的数据table

def parse_page(url):

    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, "lxml")
    tag = url.split("/")[4].split("?")[0]
    for items in soup.find_all(attrs={'class': 'subject-item'}):
        data = []
        try:
            title = items.find('h2').a.find(text=True).strip()
            detail = items.find(class_='pub').find(text=True).strip()
            detail = detail.split("/")
            if len(detail) == 4:
                detail.insert(1, " ")
            author = detail[0]
            translator = detail[1]
            publish = detail[2]
            time = detail[3]
            price = detail[4]
            score = items.find(class_='rating_nums').find(text=True).strip() if True else ""
            brief = items.find('p').find(text=True).strip()


        except (IndexError, TypeError, AttributeError):
            continue
        data.append([title, score, author, translator, publish, time, price, brief, tag])
        sql = "INSERT INTO allbooks values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 这是一条sql插入语句
        cursor.executemany(sql, data)  # 执行sql语句，并用executemary()函数批量插入数据库中
        db.commit()
        print(data)
    return data
def get_page(page,base_url):
        parms = {
            'start': page,
            'type': 'T',
        }
        url = base_url + urlencode(parms)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return url
        except requests.ConnectionError as e:
            print('Error', e.args)



if __name__ == '__main__':
    start = time.perf_counter()
    for urls in channel.channels:
        for page in range(0, max_page + 1):
            url = get_page(page * 20, urls+"?")
            result = parse_page(url)
            time.sleep(int(format(random.randint(2, 8)))) # 设置随机等待时间

    end = time.perf_counter()  # 设置一个时钟，这样我们就能知道我们爬取了多长时间了
    print('Time Usage:', end - start)  # 爬取结束，输出爬取时间
    count = cursor.execute('select * from allbooks')
    print('has %s record' % count)  # 输出爬取的总数目条数
    # 释放数据连接
    if cursor:
        cursor.close()
    if db:
        db.close()


