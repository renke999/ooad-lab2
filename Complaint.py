# from User import User
# from Repair import Repair

Complaint_DICT = {}
# TODO 创建一个新的sql投诉记录表
# 投诉数据库
import pymysql
# 评价记录数据库
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='2000825lxr', charset='utf8')
cursor = conn.cursor()


class Complaint:
    """
    投诉类
    """

    # 类变量，用于统计当前complaint数量
    complaint_count = 0

    def __init__(self,
                 id,
                 repair,
                 user,
                 done=False,
                 repair_content=None
                 ):
        """

        :param repair: Repair类，用户的报修
        :param user: User类，用户
        :param done: bool，是否解决
        :param repair_content: 用户的投诉
        """
        self.id = id
        self.repair = repair
        self.user = user
        self.done = done
        self.repair_content = repair_content
        Complaint_DICT[self.id] = self
        cursor.execute("use property")
        sql = """insert p_complaint(id, repair_id, user_id, done, repair_content) values (%s, %s, %s, %s, '%s');""" % (
        self.id, self.repair.get_id(), self.user.get_id(),  self.done, self.repair_content)
        cursor.execute(sql)
        conn.commit()

    def is_done(self):
        return self.done

    def get_repair(self):
        return self.repair

    def set_done(self, done):
        self.done = done
        cursor.execute("use property")
        cursor.execute("update p_complaint set done=%s where id=%s" % (self.done, self.id))
        conn.commit()

    def get_id(self):
        return self.id

