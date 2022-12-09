from Repair import Repair
from Complaint import Complaint

from datetime import datetime


# 数据库，存放所有业主信息
USER_DICT = {}

class User:
    """
    业主类
    """

    user_count = 0

    def __init__(self,
                 phone: str = None,
                 wechat: str = None,
                 ):
        """

        :param phone: 用户电话
        :param wechat: 用户微信
        """
        self.phone = phone
        self.wechat = wechat
        self.repair_list = []
        self.complaint_list = []

        # TODO 实现数据库
        # 用户的id
        self.id = User.user_count
        USER_DICT[self.id] = self
        User.user_count += 1

    def init_repair(self, fault, source: str):
        """

        :param fault: Fault类，用户报修所对应的故障
        :param source: 用户的报修来源
        :return:
        """
        time = datetime.now()
        repair = Repair(time=time, fault=fault, user=self, source=source)
        self.repair_list.append(repair)

        # TODO 更新sql数据库
        # 更新内存数据库
        USER_DICT[self.id] = self
        return repair

    def make_feedback(self, feedback):
        """

        :param feedback: Feedback类，维修工完成后，调度类会传一个评价记录表给用户
        :return:
        """
        # TODO 应该由用户输入，暂时先设定个默认值
        print('\n*********************************************')
        print("用户>>> 您的维修已完成，请对服务进行评价")
        time_score = input("用户>>> 请输入响应及时度：")
        attitude_score = input("用户>>> 请输入维修工态度：")
        satisfy_score = input("用户>>> 请输入满意度：")
        print("用户>>> 评价已完成")
        print('*********************************************\n')
        # time_score = 5
        # attitude_score = 5
        # satisfy_score = 5
        feedback.set_feedback(time_score, attitude_score, satisfy_score)


    def make_complaint(self, complaint_repair):
        complaint_content = input("用户>>> 输入投诉内容：")
        complaint = Complaint(complaint_repair, self, False, complaint_content)

