from Singleton import Singleton


class Fault:
    """
    故障类
    """

    def __init__(self, name, id):
        # 故障名
        self.name = name
        self.id = id
        instance = Singleton.getInstance()
        sql = """insert p_fault(id,fault_name) values (%s, '%s');""" % (self.id, self.name)
        instance.cursor.execute(sql)
        instance.conn.commit()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

