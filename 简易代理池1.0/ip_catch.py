import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from mogodb_queue import mogo_queue
#ip_queue = mogo_queue('ip_database','proxy_collection')

class ip_catch(object):
    ip_queue = mogo_queue('ip_database', 'proxy_collection')

    def __init__(self, page=3):
        self.page = 4
        self.effective_ip_list = []
        self.url = 'https://www.baidu.com'

    def proxy_catch(self):
        proxy_list = []
        ip_url = ['http://www.xicidaili.com/nn/{}'.format(str(i)) for i in range(self.page)]
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24(KHTML, like Gecko) Chrome / 19.0.1055.1Safari / 535.24"
        }
        for url in ip_url:
            data = requests.get(url, headers=header)
            soup = BeautifulSoup(data.text, 'lxml')
            for i in soup.find_all('tr', class_='odd'):
                ip = i.find_all('td')[1].get_text()
                port = i.find_all('td')[2].get_text()
                proxy = (ip + ':' + port).strip()
                proxy_list.append(proxy)
        return proxy_list

    def catch_effictive_ip(self):
        proxy_list = self.proxy_catch()
        for proxy in proxy_list:
            try:
                html = requests.get(self.url, proxies=proxy, timeout=1)#检验代理是否正常使用
                self.effective_ip_list.append(proxy)
                print('网页返回状态码', html, proxy, '代理有效')
                ip = proxy.split(':')[0]#这是IP
                port = proxy.split(':')[1]#这是端口
                self.ip_queue.push_ip(ip, port, proxy)#插入数据库
            except:
                print(proxy, '代理无效')

    def test_proxy(self):
        proxy_list = self.ip_queue.find_proxy()
        for proxy in proxy_list:
            try:
                html = requests.get(self.url, proxies=proxy, timeout=1)
                self.effective_ip_list.append(proxy)
                print('网页返回状态码：', html, proxy, '代理依然有效')

            except:
                self.ip_queue.delete_proxy(proxy)
                print(proxy, '该代理已经无效,删除')

    def main_method(self):
        self.test_proxy()#启用该主函数时，启动检验代理有效性，将无效的删除
        proxy_list = self.ip_queue.find_proxy()
        while True:
            if len(proxy_list) > 100:
                print('可用代理超过100，无需再爬取')
                break
            else:
                print('可用代理少于100，需要重新爬取')
                self.catch_effictive_ip()
ip_list = ip_catch()
ip_list.main_method()



