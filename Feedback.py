# TODO 创建一个新的sql评价记录表
# 评价记录数据库
FEEDBACK_DICT = {}


class Feedback:
    """
    评价类
    和报修以及业主相关联
    """

    # 类变量，用于统计当前feedback数量
    feedback_count = 0

    def __init__(self,
                 repair,
                 user,
                 time_score=None,
                 attitude_score=None,
                 satisfy_score=None):
        """

        :param repair: Repair类，评价记录对应的报修
        :param user: User类，评价记录对应的用户
        :param time_score: 用户给出的时间及时度打分
        :param attitude_score: 用户给出的态度打分
        :param satisfy_score: 用户给出的满意度打分
        """

        self.repair = repair
        self.user = user
        self.time_score = time_score
        self.attitude_score = attitude_score
        self.satisfy_score = satisfy_score

        # 评价的id，用于查内存数据库，用sql则不需要此变量
        self.id = Feedback.feedback_count
        FEEDBACK_DICT[self.id] = self
        Feedback.feedback_count += 1


    def set_feedback(self, time_score, attitude_score, satisfy_score):
        self.time_score = time_score
        self.attitude_score = attitude_score
        self.satisfy_score = satisfy_score

        # TODO 更新数据库中的一条信息
        # 更新FEEDBACK_DICT
        FEEDBACK_DICT[self.id] = self




