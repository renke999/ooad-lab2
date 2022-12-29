from Singleton import Singleton


class Reply:

    def __init__(self, **kwargs):

        self.reply_id = kwargs['reply_id'] if 'reply_id' in kwargs else None
        self.complaint_id = kwargs['complaint_id'] if 'complaint_id' in kwargs else None
        self.scheduler_id = kwargs['scheduler_id'] if 'scheduler_id' in kwargs else None
        self.worker_id = kwargs['worker_id'] if 'worker_id' in kwargs else None
        self.reply_content = kwargs['reply_content'] if 'reply_content' in kwargs else None

        self.instance = Singleton.get_instance()

    def commit_reply(self):
        sql = """insert reply(complaint_id, scheduler_id, worker_id, reply_content) 
        values (%s, %d, null, null);""" % (self.complaint_id, self.scheduler_id)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.reply_id = self.instance.cursor.lastrowid
        sql = """insert reply(complaint_id, scheduler_id, worker_id, reply_content) 
        values (%s, null, %d, null);""" % (self.complaint_id, self.worker_id)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.reply_id = (self.reply_id, self.instance.cursor.lastrowid)
        return self.reply_id

    def update_reply(self, reply_content):
        sql = """update reply set reply_content = '%s' where reply_id = %d;""" % (reply_content, self.reply_id)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()

