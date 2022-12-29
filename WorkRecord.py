from Singleton import Singleton
import datetime


class WorkRecord:

    def __init__(self, **kwargs):

        self.work_record_id = kwargs['work_record_id'] if 'work_record_id' in kwargs else None
        self.schedule_id = kwargs['schedule_id'] if 'schedule_id' in kwargs else None
        self.start_time = kwargs['start_time'] if 'start_time' in kwargs else datetime.datetime.now()
        self.end_time = kwargs['end_time'] if 'end_time' in kwargs else None
        self.work_content = kwargs['work_content'] if 'work_content' in kwargs else None

        self.instance = Singleton.get_instance()

    def commit_work_record(self, end_time: datetime.datetime = None):
        self.end_time = end_time if end_time else datetime.datetime.now()

        sql = """insert work_record(schedule_id, start_time, end_time, work_content) 
        values (%d, '%s', '%s', '%s');""" % (self.schedule_id, str(self.start_time), str(self.end_time), self.work_content)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.work_record_id = self.instance.cursor.lastrowid
        return self.work_record_id
