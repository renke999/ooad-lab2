from Repair import Repair
from Complaint import Complaint

from datetime import datetime


# 数据库，存放所有业主信息
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='2000825lxr', charset='utf8')
cursor = conn.cursor()


class User:
    """
    业主类
    """

    def __init__(self,
                 id: int,
                 phone: str = None,
                 wechat: str = None,
                 ):
        """

        :param phone: 用户电话
        :param wechat: 用户微信
        """
        self.id = id
        self.phone = phone
        self.wechat = wechat
        self.repair_list = []
        self.complaint_list = []

        # TODO 实现数据库 ok
        # 用户的id
        cursor.execute("use property")
        sql = """insert p_user(id,phone,wechat) values (%s, '%s', '%s');""" % (self.id, self.phone, self.wechat)
        cursor.execute(sql)
        conn.commit()

    def init_repair(self, fault, source: str):
        """

        :param fault: Fault类,用户报修所对应的故障
        :param source: 用户的报修来源
        :return:
        """
        time = datetime.now()
        repair = Repair(time=time, fault=fault, user=self, source=source)
        self.repair_list.append(repair)

        # TODO 更新sql数据库 ok
        # 更新报修的用户id
        # cursor.execute("insert p_repair(user_id) values (%s)" % self.id)
        # conn.commit()
        return repair

    def make_feedback(self, feedback):
        """

        :param feedback: Feedback类,维修工完成后,调度类会传一个评价记录表给用户
        :return:
        """

        print('\n*********************************************')
        print("用户>>> 您的维修已完成，请对服务进行评价")
        time_score = input("用户>>> 请输入响应及时度：")
        attitude_score = input("用户>>> 请输入维修工态度：")
        satisfy_score = input("用户>>> 请输入满意度：")
        print("用户>>> 评价已完成")
        print('*********************************************\n')
        feedback.set_feedback(time_score, attitude_score, satisfy_score)


    def make_complaint(self, complaint_repair):
        complaint_content = input("用户>>> 输入投诉内容：")
        complaint = Complaint(id=Complaint.complaint_count, repair=complaint_repair, user=self, done=False, repair_content=complaint_content)
        Complaint.complaint_count += 1

    def get_id(self):
        return self.id

