from RepairState import RepairState, TodoState, DoingState, DoneState
from Feedback import Feedback

from datetime import datetime
from Singleton import Singleton

# 建在内存中的报修数据库
# REPAIR_DICT = {}


class Repair:
    """
    维修类
    """
    # lazy import for type hint

    repair_count = 0

    def __init__(self, time: str, fault, user, source: str, state: RepairState = TodoState(),
                 complex_repair: bool = False, remaining_step: int = 1):
        """

        :param time: 报修时间
        :param fault: Fault，报修对应故障类型
        :param user: User类，报修人
        :param source: 报修来源（微信，电话）
        :param state: 目前报修的处理状态：待调度、报修中、已报修，初始化一个报修时，默认是待调度状态
        :param complex_repair: 是否是个复杂任务（拓展流程中，复杂任务需要多次进行调度）
        :param remaining_step: 如果是个复杂任务，剩余需要调度的次数（拓展流程中，复杂任务需要多次进行调度）
        """

        self.time = time
        self.fault = fault
        self.source = source
        self.user = user
        self.state = state
        self.complex_repair = complex_repair
        self.remaining_step = remaining_step
        self.id = Repair.repair_count
        # REPAIR_DICT[self.id] = self
        Repair.repair_count += 1
        singleton = Singleton.getInstance()
        sql = """insert p_repair(id,repair_time,fault_id,user_id,source,state_id,complex_repair,remaining_step) 
        values (%s, '%s', %s, %s, '%s', %s, %s, %s)""" % (self.id, str(self.time)[0:18],
                                                       self.fault.get_id(), self.user.get_id(),
                                                       self.source, self.state.get_id(),
                                                       self.complex_repair, self.remaining_step)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def set_complex_repair_and_remaining_step(self, complex_repair, remaining_step):
        """
        调度员可能认为这是个复杂任务，设置复杂任务为true以及需要处理的步骤
        :param complex_repair: 是否是个复杂任务
        :param remaining_step: 如果是个复杂任务，剩余需要调度的次数
        :return:
        """
        self.complex_repair = complex_repair
        self.remaining_step = remaining_step

    def generate_feedback(self):
        """
        生成一个评价记录给用户
        :return:
        """
        self.feedback = Feedback(id=Feedback.feedback_count, repair= self, user = self.user)
        Feedback.feedback_count += 1
        # 通知用户进行评价
        self.user.make_feedback(self.feedback)

    def is_completed(self):
        """
        维修工人完成了一次维修，判断是否是一个需要多次完成的维修任务（拓展流程），如果是的话，是否已经完成？
        :return: bool，是否已经完成
        """
        self.remaining_step -= 1
        if not self.complex_repair:
            return True
        if self.complex_repair and self.remaining_step == 0:
            return True
        return False

    def get_state(self):
        """
        getter
        :return: 当前报修状态
        """
        return self.state

    def is_todo_state(self):
        """
        getter，Scheduler会调用这个函数判断报修的状态
        :return: 当前报修状态是否是待调度
        """
        return isinstance(self.state, TodoState)

    def is_doing_state(self):
        """
        getter，Scheduler会调用这个函数判断报修的状态
        :return: 当前报修状态是否是报修中
        """
        return isinstance(self.state, DoingState)

    def get_remaining_step(self):
        return self.remaining_step

    def get_fault(self):
        """
        getter
        :return: 报修的故障类型
        """
        return self.fault

    def set_fault(self, fault):
        """
        setter
        :return:
        """
        self.fault = fault
        # 更新内存中的数据库
        # TODO 更新sql
        # REPAIR_DICT[self.id] = self
        singleton = Singleton.getInstance()
        sql = """update p_repair set fault_id = %s where id=%s""" % (self.fault.get_id(), self.id)
        # 更新：fault("XXX", 1)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def switch_state(self):
        """
        切换状态
        :return: None
        """
        self.state.switch_state(self)
        # 更新内存中的数据库
        # TODO 更新sql
        # REPAIR_DICT[self.id] = self
        singleton = Singleton.getInstance()
        sql = """update p_repair set state_id = %s where id=%s""" % (self.state.get_id(), self.id)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def set_state(self, repair_state):
        """

        :param repair_state: TodoState, DoingState, DoneState
        :return:
        """
        self.state = repair_state
        # 更新内存中的数据库
        # TODO 更新sql
        # REPAIR_DICT[self.id] = self
        singleton = Singleton.getInstance()
        sql = """update p_repair set state_id = %s where id=%s""" % (self.state.get_id(), self.id)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def reset_state(self):
        self.state = TodoState()
        # 更新内存中的数据库
        # TODO 更新sql
        # REPAIR_DICT[self.id] = self
        singleton = Singleton.getInstance()
        sql = """update p_repair set state_id = %s where id=%s""" % (self.state.get_id(), self.id)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def get_id(self):
        """
        getter
        :return: 报修的id
        """
        return self.id
