from Singleton import Singleton


class Feedback:

    def __init__(self, **kwargs):

        self.feedback_id = kwargs['feedback_id'] if 'feedback_id' in kwargs else None
        self.repair_id = kwargs['repair_id'] if 'repair_id' in kwargs else None

        self.time_score = kwargs['time_score'] if 'time_score' in kwargs else None
        self.attitude_score = kwargs['attitude_score'] if 'attitude_score' in kwargs else None
        self.satisfy_score = kwargs['satisfy_score'] if 'satisfy_score' in kwargs else None
        self.instance = Singleton.get_instance()

    def commit_feedback(self):
        sql = """insert feedback(repair_id, time_score, attitude_score, satisfy_score) 
        values (%d, %d, %d, %d);""" % (self.repair_id, self.time_score, self.attitude_score, self.satisfy_score)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.feedback_id = self.instance.cursor.lastrowid
        return self.feedback_id
