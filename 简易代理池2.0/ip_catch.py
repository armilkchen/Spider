import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from mogodb_queue import mogo_queue
from get_proxy import Get_Proxy
#ip_queue = mogo_queue('ip_database','proxy_collection')

class ip_catch(object):
    ip_queue = mogo_queue('ip_database', 'proxy_collection')

    def __init__(self):
        self.effective_ip_list = []
        self.url = 'http://2017.ip138.com/ic.asp'
        self.get_proxy = Get_Proxy()


    def catch_effictive_ip(self):
        proxy_list = self.get_proxy.crawl()
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



