from Singleton import Singleton
import datetime


state_dct = {'待调度': 'TodoState', '调度中': 'DoingState', '已调度': 'DoneState'}


def select_one_repair(sql):
    print("已调度报修列表：")
    instance = Singleton.getInstance()
    repair_lst = instance.get_dict_data_select(sql)
    print("\n".join(['\t' + str(dct) for dct in repair_lst]) if len(repair_lst) else "\t空")
    repair_id = int(input("请根据'repair_id'选择报修，退出请输入'0'：\n>>>"))
    repair = None
    while repair_id != 0:
        try:
            repair = list(filter(lambda x: x['repair_id'] == repair_id, repair_lst))[0]
            repair = Repair(**repair)
        except IndexError:
            repair_id = int(input("输入'repair_id'错误，请重新输入：\n>>>"))
            continue
        repair_id = int(input("请根据'repair_id'选择报修，退出请输入'0'：\n>>>"))
    return repair


class Repair:

    def __init__(self, **kwargs):

        self.repair_id = kwargs['repair_id'] if 'repair_id' in kwargs else None
        self.repair_time = kwargs['repair_time'] if 'repair_time' in kwargs else datetime.datetime.now()
        self.repair_state = kwargs['repair_state'] if 'repair_state' in kwargs else '待调度'
        self.fault_name = kwargs['fault_name'] if 'fault_name' in kwargs else None
        self.user_id = kwargs['user_id'] if 'user_id' in kwargs else None
        self.source = kwargs['source'] if 'source' in kwargs else 'phone'

        self.repair_content = kwargs['repair_content'] if 'repair_content' in kwargs else None
        self.complex_repair = kwargs['complex_repair'] if 'complex_repair' in kwargs else False
        self.remaining_step = kwargs['remaining_step'] if 'remaining_step' in kwargs else 0
        self.instance = Singleton.getInstance()
        self.state = eval(state_dct[self.repair_state])()

    def commit_repair(self):
        sql = """insert repair(repair_time, repair_state, fault_name, user_id, source, repair_content) 
        values ('%s', '%s', '%s', %s, '%s', '%s');""" % (str(self.repair_time), self.repair_state, self.fault_name, self.user_id, self.source, self.repair_content)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.repair_id = self.instance.cursor.lastrowid
        return self.repair_id

    def switch_state(self, repair_state='待调度'):
        self.state = self.state.switch_state(self.repair_id, repair_state)
        self.repair_state = self.state.get_repair_state()

    def change_fault(self, fault_name, repair_content):
        sql = """update repair set fault_name = '%s', repair_content = '%s' where repair_id = %d""" % (fault_name, repair_content, self.repair_id)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.fault_name = self.fault_name
        self.repair_content = self.repair_content


class RepairState:

    def __init__(self):
        self.instance = Singleton.getInstance()

    def switch_state(self, repair_id, repair_state):
        pass

    def get_repair_state(self):
        pass


class TodoState(RepairState):

    def switch_state(self, repair_id, repair_state='调度中'):
        is_complex = int(input("设为复杂任务请按'1'，设为简单任务请按'2'：\n>>>")) == 1
        remaining_step = 0 if not is_complex else int(input("请设置复杂任务的工时个数：\n>>>"))
        sql = """update repair set repair_state = '%s', complex_repair = %s, remaining_step = %d where repair_id = %d""" \
              % ('调度中', is_complex, remaining_step, repair_id)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        return DoingState()

    def get_repair_state(self):
        return '待调度'


class DoingState(RepairState):

    def switch_state(self, repair_id, repair_state):
        sql = """update repair set repair_state = '%s' where repair_id = %d""" % (repair_state, repair_id)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        return eval(state_dct[repair_state])()

    def get_repair_state(self):
        return '调度中'


class DoneState(RepairState):

    def switch_state(self, repair_id, repair_state):
        pass

    def get_repair_state(self):
        return '已调度'


