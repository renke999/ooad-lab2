from Singleton import Singleton

from WorkRecord import WorkRecord

import datetime


class Schedule:

    def __init__(self, **kwargs):

        self.schedule_id = kwargs['schedule_id'] if 'schedule_id' in kwargs else None
        self.scheduler_id = kwargs['scheduler_id'] if 'scheduler_id' in kwargs else None
        self.worker_id = kwargs['worker_id'] if 'worker_id' in kwargs else None
        self.repair_id = kwargs['repair_id'] if 'repair_id' in kwargs else None
        self.is_right = kwargs['is_right'] if 'is_right' in kwargs else True

        self.instance = Singleton.get_instance()

    def commit_schedule(self):
        sql = """insert schedule(scheduler_id, worker_id, repair_id, is_right) 
        values (%s, %s, %s, %s);""" % (self.scheduler_id, self.worker_id, self.repair_id, self.is_right)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.schedule_id = self.instance.cursor.lastrowid
        return self.schedule_id

    def wrong_schedule(self):
        sql = """update schedule set is_right = false where schedule_id = %d;""" % self.schedule_id
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.is_right = False

    def right_schedule(self):
        start_time = datetime.datetime.now()
        work_content = input("维修工%d开始工作，请输入工作内容\n>>>" % self.worker_id)
        work_record = WorkRecord(schedule_id=self.schedule_id, start_time=start_time, work_content=work_content)
        work_record.commit_work_record()

