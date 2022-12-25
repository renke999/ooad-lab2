from WorkRecord import WorkRecord
from Fault import Fault
from datetime import datetime
import time

from Singleton import Singleton


class Worker:
    """
    维修工
    和调度、故障、维修记录相关联
    """

    def __init__(self,
                 id,
                 fault,
                 schedule = None,
                 free: bool = True):

        """
        :param id: Worker类成员的id,为维修员数据表的主键
        :param fault_id: Fault类成员的id,维修工对应的故障类型
        :param schedule_id: Schedule类成员的id,维修工对应的调度
        :param free: 维修工的空闲状态
        """
        self.id = id
        self.fault = fault
        self.fault_id = fault.get_id()
        self.schedule = schedule
        if self.schedule:
            self.schedule_id = self.schedule.get_id()
        else:
            self.schedule_id = -1   # -1表示还未被调度
        self.is_free = free
        # WORKER_DICT[self.id] = self

        singleton = Singleton.getInstance()
        sql = """insert p_worker(id,fault_id,schedule_id,is_free) values (%s, %s, %s, %s);""" % (self.id, self.fault_id, self.schedule_id, self.is_free)
        singleton.cursor.execute(sql)
        singleton.conn.commit()


    def get_free(self):
        """
        getter
        :return: 维修工当前的空闲状态
        """
        return self.is_free

    def set_free(self, free):
        """
        setter 设置维修工的空闲状态
        :param free: 维修工的空闲状态
        :return:
        """
        self.is_free = free
        # 更新数据库中维修工的状态
        # TODO 更新sql数据库中维修工状态 ok
        singleton = Singleton.getInstance()
        singleton.cursor.execute("update p_worker set is_free=%s where id=%s" % (self.is_free, self.id))
        singleton.conn.commit()

    def get_fault(self):
        """
        getter
        :return: 维修工能处理的故障类型
        """
        return self.fault

    def set_schedule(self, schedule):
        """
        setter 设置维修工对应的调度
        :param schedule: Schedule类成员,
        :return:
        """
        self.schedule = schedule
        self.schedule_id = schedule.get_id()
        # WORKER_DICT[self.id] = self
        # 更新内存中的数据库
        # TODO 更新sql OK
        singleton = Singleton.getInstance()
        singleton.cursor.execute("update p_worker set schedule_id=%s where id=%s" % (self.schedule_id, self.id))
        singleton.conn.commit()

    def get_id(self):
        return self.id

    def handle_complaint(self):
        input("维修工>>> 请对投诉记录进行回复：")

    def work(self):
        """
        :return:
        """
        # case 1. 工种不匹配，修改报修的故障类型，并将状态由报修中重置为待调度（拓展流程1）
        if not self.schedule.is_fault_matched():
            # TODO 这里随便修改一个故障类型，实际上应该由维修工在数据库中选择一个，可以不用实现这个TODO，不重要
            actual_fault = self.fault
            self.schedule.set_repair_fault(actual_fault)
            print("维修工>>> 维修工工种不匹配，重新调度")
            self.schedule.reset_schedule()
            return

        # 模拟维修工维修过程，记录维修的开始时间和结束时间等信息，加入维修记录数据库中
        start_time = datetime.now()
        time.sleep(1)
        end_time = datetime.now()
        work_content = input('维修工>>> 请输入本次维修内容：')
        work_record = WorkRecord(worker=self)
        work_record.set_record(start_time=str(start_time)[0:18], end_time=str(end_time)[0:18], work_content=work_content)

        # case 2. 如果是个复杂的报修任务，则需要多次完成。如果没有完成，则将状态由报修中重置为待调度
        if not self.schedule.is_completed():
            print("维修工>>> 任务需要多次调度，剩余{}次调度，重新调度".format(self.schedule.get_remaining_step()))
            self.schedule.reset_schedule()
            return

        # case 3. 成功处理完报修，将状态由报修中转为已报修，并生成评价记录表给用户填写
        self.schedule.end_schedule()



