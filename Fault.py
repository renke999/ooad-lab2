# TODO 创建一个新的sql故障类型表

# 故障类型数据库

import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='2000825lxr', charset='utf8')
cursor = conn.cursor()

class Fault:
    """
    故障类
    """

    def __init__(self, name, id):
        # 故障名
        self.name = name
        self.id = id
        cursor.execute("use property")
        sql = """insert p_fault(id,fault_name) values (%s, '%s');""" % (self.id, self.name)
        cursor.execute(sql)
        conn.commit()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

