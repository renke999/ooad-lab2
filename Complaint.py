from Singleton import Singleton


class Complaint:

    def __init__(self, **kwargs):

        self.complaint_id = kwargs['complaint_id'] if 'complaint_id' in kwargs else None
        self.repair_id = kwargs['repair_id'] if 'repair_id' in kwargs else None
        self.complaint_content = kwargs['complaint_content'] if 'complaint_content' in kwargs else None
        self.is_done = kwargs['is_done'] if 'is_done' in kwargs else None

        self.instance = Singleton.getInstance()

    def commit_complaint(self):
        sql = """insert complaint(repair_id, complaint_content, is_done) 
        values (%s, '%s', %s);""" % (self.repair_id, self.complaint_content, self.is_done)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.complaint_id = self.instance.cursor.lastrowid
        return self.complaint_id

    def close_complaint(self):
        sql = """update complaint set is_done = true where complaint_id = %d;""" % self.complaint_id
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.is_done = True
