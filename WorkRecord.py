from datetime import datetime

# TODO 初始化一个work_record数据库
# 初始化一个内存中的WORK_RECORD_DICT数据库
WORK_RECORD_DICT = {}

class WorkRecord:
    """
    维修记录类，应该用数据库代替
    """

    work_record_count = 0

    def __init__(self,
                 worker,
                 start_time: datetime = None,
                 end_time: datetime = None,
                 work_content: str = None):
        """
        拓展流程中第二条，有多次执行的活动需要完成时，维修工每开始一次活动就需要统计维修相关信息
        :param worker: Worker类成员，维修记录对应的维修工人
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param work_content: 维修内容
        :return:
        """
        self.worker = worker
        self.start_time = start_time
        self.end_time = end_time
        self.work_content = work_content

        # TODO 用sql加入到数据库里
        self.id = WorkRecord.work_record_count
        WORK_RECORD_DICT[self.id] = self
        WorkRecord.work_record_count += 1

    def set_record(self,
                   start_time: datetime,
                   end_time: datetime,
                   work_content: str):
        self.start_time = start_time
        self.end_time = end_time
        self.work_content = work_content
        # TODO 更新sql状态
        WORK_RECORD_DICT[self.id] = self