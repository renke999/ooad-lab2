from datetime import datetime

# TODO 初始化一个work_record数据表
# 初始化一个内存中的WORK_RECORD_DICT数据库
import pymysql

from Singleton import Singleton


class WorkRecord:
    """
    维修记录类，应该用数据库代替
    """

    work_record_count = 0

    def __init__(self,
                 worker,
                 start_time: str = None,
                 end_time: str = None,
                 work_content: str = None):
        """
        拓展流程中第二条，有多次执行的活动需要完成时，维修工每开始一次活动就需要统计维修相关信息
        :param worker: Worker类成员,维修记录对应的维修工人
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param work_content: 维修内容
        :return:
        """
        self.id = WorkRecord.work_record_count
        self.worker = worker
        self.worker_id = worker.get_id()
        self.start_time = start_time
        self.end_time = end_time
        self.work_content = work_content
        WorkRecord.work_record_count += 1
        # TODO 用sql加入到数据库里 OK
        singleton = Singleton.getInstance()
        sql = """insert p_workrecord(id, worker_id, start_time, end_time, work_content) values (%s, %s, '%s', '%s', 
        '%s')""" % (self.id, self.worker_id, self.start_time, self.end_time, self.work_content)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def set_record(self,
                   start_time: str,
                   end_time: str,
                   work_content: str):
        self.start_time = start_time
        self.end_time = end_time
        self.work_content = work_content
        # TODO 更新sql状态 OK
        singleton = Singleton.getInstance()
        singleton.cursor.execute("""update p_workrecord set start_time='%s',end_time='%s',work_content='%s' where id=%s""" % (self.start_time, self.end_time, self.work_content, self.id))
        singleton.conn.commit()
    
    def get_id(self):
        return self.id