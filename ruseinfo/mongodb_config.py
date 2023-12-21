import time
import urllib.parse

from pymongo import MongoClient

from ruseinfo.auction import logtool


class Mongo(object):
    def __init__(self, db):
        # config = configparser.ConfigParser()
        # config.read(config_file, encoding='utf-8')
        self.host = "118.195.246.81"
        self.port = 27018
        self.user = "admin"
        self.password = "duoyb#@!3a"
        self.database = db
        self.db_conn = None
        self._conn()

    def _conn(self):
        try:
            logtool.info(
                f"读取环境：{self.database}，连接信息：主机ip：{self.host},端口：{self.port},用户：{self.user},连接数据库：{self.database}")
            username = urllib.parse.quote_plus(self.user)
            password = urllib.parse.quote_plus(self.password)
            self.conn = MongoClient('mongodb://%s:%s@%s:%s' % (username, password, self.host, self.port))
            self.db_conn = self.conn[self.database]
            if self.conn.server_info():
                logtool.info(f"数据库: {self.database}初始化连接成功")
                return True
        except  Exception as e:
            logtool.error(f"数据库: {self.database}初始化连接失败，错误：{e}")
            return False

    # MongoDB数据库关闭
    def close(self):
        self.conn.close()
        logtool.info(f"数据库关闭成功")

    # 查询调用状态
    def get_state(self):
        return self.conn is not None  # and self.db_conn is not None

    def _reConn(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        #logtool.info(f"检查数据库{self.database}连通性,连接IP：{self.host}")
        while _status and _number <= num:
            try:
                self.conn.server_info()  # 检查数据库是否正常连通
                _status = False
                #logtool.info(f"数据库{self.database}连接============正常,连接IP：{self.host} ")
            except:
                if self._conn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                logtool.info(f"数据库{self.database}连接============失败,连接IP：{self.host} ")
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def insert_one(self, collection, data):
        self._reConn()
        if self.get_state():
            ret = self.db_conn[collection].insert_one(data)
            return ret.inserted_id
        else:
            return ""

    def copy_to(self, src_collection, dest_collection):
        self._reConn()
        if self.get_state():
            documents = self.db_conn[src_collection].find()
            self.db_conn[dest_collection].insert_many(documents)
            return True
        else:
            return False

    def drop_table(self, collection):
        self._reConn()
        if self.get_state():
            self.db_conn[collection].drop()
            return True
        else:
            return False

    def insert_many(self, collection, data):
        self._reConn()
        if self.get_state():
            self.db_conn[collection].insert_many(data)
        else:
            return ""

    def update(self, collection, data):
        # data format:
        # {key:[old_data,new_data]}
        data_filter = {}
        data_revised = {}
        for key in data.keys():
            data_filter[key] = data[key][0]
            data_revised[key] = data[key][1]
        if self.get_state():
            return self.db_conn[collection].update_many(data_filter, {"$set": data_revised}).modified_count
        return 0

    def find(self, col, condition, column=None):
        """
        查询数据代码
        :param col: 数据库中的集合
        :param condition: 查询条件,查询条件必须是个字典
        :param column: find 的第二个参数是可选的，可以指定需要返回的键。这个特别的 "$slice" 运算符可以返回一个数组键中元素的子集。
        :return: list 返回查询到记录的列表
        """
        # print(col, condition)
        # data= self.db_conn["sms_log"]
        # data=self.db_conn["sms_log"].find({"status":"2","createTime":{"$gte": "2022/07/12 22:18:26"}},{"status":1,"channelCode":1,"_id":0})
        # data = self.db_conn["authCode"].find({"use": False,"createdTime": {"$gte": 1657865035}})
        # print(list(data))
        self._reConn()
        if self.get_state():
            if column is None:
                return list(self.db_conn[col].find(condition))
            else:
                return list(self.db_conn[col].find(condition, column))
        else:
            return None

    def get_last_data(self, col, number=1):
        if self.get_state():
            # last_data = list(self.db_conn["authCode"].find().sort("_id", -1 ).limit(50))
            last_data = list(self.db_conn[col].find().sort("_id", -1).limit(number))
            return last_data

    def delete(self, col, condition):
        if self.get_state():
            return self.db_conn[col].delete_many(filter=condition).deleted_count
        return 0

    def aggregate(self, col, condition):
        if self.get_state():
            return list(self.db_conn[col].aggregate(condition))


