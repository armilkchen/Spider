from pymongo import MongoClient, errors
from _datetime import datetime,timedelta

class mogo_queue():
    def __init__(self, db, collection):
        self.client = MongoClient()
        self.database = self.client[db]#连接数据库
        self.db = self.database[collection]#链接数据库里的表

    def push_ip(self, ip, port, proxy):
        try:
            self.db.insert({'_id': ip, 'port': port, 'proxy': proxy})
            print(proxy, '代理插入成功')
        except errors.DuplicateKeyError as e:#对于重复的ip不能插入
            print(proxy, '已经存在队列中')
    def find_proxy(self):
        proxy_list = []#用来接收从数据库查找到的所有代理
        for i in self.db.find():
            proxy = i['proxy']
            proxy_list.append(proxy)
        return proxy_list
    def delete_proxy(self, proxy):
        self.db.remove({'proxy': proxy})
        print(proxy, '无效代理删除成功')
