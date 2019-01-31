from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import random

class Get_Proxy(object):
    def __init__(self):
        self.proxy_list = []
    def crawl(self):
        self.proxy_catch_one()
        self.proxy_catch_two()
        self.proxy_catch_three()
        self.proxy_catch_four()
        self.proxy_catch_five()
        proxy_list = np.unique(self.proxy_list)
        print(len(proxy_list))
        return proxy_list
    def proxy_catch_one(self):
        url_list = [
            'http://www.xicidaili.com/nn/{}',  # 高匿
            'http://www.xicidaili.com/nt/{}',  # 透明
        ]
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24(KHTML, like Gecko) Chrome / 19.0.1055.1Safari / 535.24"
        }
        for url in url_list:
            ip_url = [url.format(str(i)) for i in range(1, 50)]
            for real_url in ip_url:
                data = requests.get(real_url, headers=header)
                soup = BeautifulSoup(data.text, 'lxml')
                for i in soup.find_all('tr', class_='odd'):
                    ip = i.find_all('td')[1].get_text()
                    port = i.find_all('td')[2].get_text()
                    proxy = (ip + ':' + port).strip()
                    self.proxy_list.append(proxy)
        return self.proxy_list

    def proxy_catch_two(self):
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/{}/', 'https://www.kuaidaili.com/free/intr/{}/']
        for url in url_list:
            ip_url = [url.format(str(i)) for i in range(1, 50)]
            for real_url in ip_url:
                data = requests.get(real_url)
                soup = BeautifulSoup(data.text, 'lxml')
                for tr in soup.tbody.find_all('tr'):
                    ip = tr.find_all(name='td')[0].get_text()
                    port = tr.find_all(name='td')[1].get_text()
                    proxy = ip + ':' + port
                    self.proxy_list.append(proxy)
                time.sleep(1)
        return self.proxy_list

    def proxy_catch_three(self):
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/?stype=1&page={}', 'http://www.ip3366.net/free/?stype=2&page={}']
        for url in urls:
            ip_url = [url.format(str(i)) for i in range(1, 3)]
            for real_url in ip_url:
                data = requests.get(real_url)
                soup = BeautifulSoup(data.text, 'lxml')
                for tr in soup.tbody.find_all('tr'):
                    ip = tr.find_all(name='td')[0].get_text()
                    port = tr.find_all(name='td')[1].get_text()
                    proxy = ip + ':' + port
                    self.proxy_list.append(proxy)
        return self.proxy_list

    def proxy_catch_four(self):
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        for url in urls:
            data = requests.get(url)
            soup = BeautifulSoup(data.text, 'lxml')
            for tr in soup.table.find_all('tr')[1:]:
                ip = tr.find_all(name='td')[0].get_text().strip()
                port = tr.find_all(name='td')[1].get_text().strip()
                proxy = ip + ':' + port
                self.proxy_list.append(proxy)
        return self.proxy_list

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




