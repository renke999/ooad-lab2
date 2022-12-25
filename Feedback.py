# TODO 创建一个新的sql评价记录表
from Singleton import Singleton


class Feedback:
    """
    评价类
    和报修以及业主相关联
    """

    # 类变量，用于统计当前feedback数量
    feedback_count = 0

    def __init__(self,
                 id,
                 repair,
                 user,
                 time_score: int = -1,
                 attitude_score: int = -1,
                 satisfy_score: int = -1):
        """

        :param repair_id: 评价记录对应的报修id
        :param user_id: 评价记录对应的用户id
        :param time_score: 用户给出的时间及时度打分
        :param attitude_score: 用户给出的态度打分
        :param satisfy_score: 用户给出的满意度打分 -1表示尚未打分
        """
        self.id = id
        self.repair_id = repair.get_id()
        self.user_id = user.get_id()
        self.time_score = time_score
        self.attitude_score = attitude_score
        self.satisfy_score = satisfy_score
        singleton = Singleton.getInstance()
        sql = """insert p_feedback(id, repair_id, user_id, time_score, attitude_score, satisfy_score) values (%s, %s, %s, %s, %s, %s);""" % (
        self.id, self.repair_id, self.user_id, self.time_score, self.attitude_score, self.satisfy_score)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def set_feedback(self, time_score, attitude_score, satisfy_score):
        self.time_score = time_score
        self.attitude_score = attitude_score
        self.satisfy_score = satisfy_score

        # TODO 更新数据库中的一条信息
        # 更新FEEDBACK_DICT
        #FEEDBACK_DICT[self.id] = self
        singleton = Singleton.getInstance()
        sql = """update p_feedback set time_score = %s, attitude_score = %s, satisfy_score = %s where id = %s""" % (time_score, attitude_score, satisfy_score, self.id)
        singleton.cursor.execute(sql)
        singleton.conn.commit()





