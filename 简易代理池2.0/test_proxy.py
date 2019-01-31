from bs4 import BeautifulSoup
import requests
import time
import random

class text(object):
    def __init__(self):
        self.proxy_list = []

    def proxy_catch_five(self):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        免费代理库
        超多量
        :return:
        """
        urls = ['http://ip.jiangxianli.com/?page={}']
        for url in urls:
            ip_url = [url.format(str(i)) for i in range(1, 6)]
            for real_url in ip_url:
                data = requests.get(real_url)
                soup = BeautifulSoup(data.text, 'lxml')
                for tr in soup.tbody.find_all('tr'):
                    ip = tr.find_all(name='td')[0].get_text()
                    port = tr.find_all(name='td')[1].get_text()
                    proxy = ip + ':' + port
                    self.proxy_list.append(proxy)
        return self.proxy_list


result = text()
print(result.proxy_catch_five())

