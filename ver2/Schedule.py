# TODO 创建一个新的sql调度记录表
# 调度记录数据库
# Schedule_DICT = {}
from Singleton import Singleton


class Schedule:
    """
    调度
    和调度员、报修工、维修类相关联
    """

    schedule_count = 0

    def __init__(self, scheduler, worker, repair):
        """

        :param scheduler: Scheduler类成员，该调度对应的调度员
        :param worker: Worker类成员，该调度对应的维修工
        :param repair: Repair类成员，该调度对应的报修任务
        """
        self.id = Schedule.schedule_count
        self.scheduler = scheduler
        self.worker = worker
        self.repair = repair
        # 将维修工对应的调度设为当前调度
        self.worker.set_schedule(self)
        # Schedule_DICT[self.id] = self

        singleton = Singleton.getInstance()
        sql = """insert p_schedule(id, schedule_id, worker_id, repair_id) values (%s, %s, %s, %s)""" % (self.id, self.scheduler.get_id(), self.worker.get_id(), self.repair.get_id())
        singleton.cursor.execute(sql)
        singleton.conn.commit()
        
        Schedule.schedule_count += 1
    
    def get_id(self):
        return self.id

    def get_repair(self):
        return self.repair

    def get_worker(self):
        return self.worker

    def get_scheduler(self):
        return self.scheduler

    def set_repair_fault(self, fault):
        """
        维修工人发现自己的工种和故障不匹配时，重置故障的类型
        :param fault:
        :return:
        """
        self.repair.set_fault(fault)

    def is_fault_matched(self):
        """
        判断报修任务的故障类型和维修工的故障类型是否匹配
        :return:
        """
        return self.worker.get_fault() == self.repair.get_fault()

    def is_completed(self):
        """
        如果是个复杂的报修任务，则需要多次完成。如果没有完成，则将状态由报修中重置为待调度
        :return:
        """
        return self.repair.is_completed()

    def get_remaining_step(self):
        return self.repair.get_remaining_step()

    def start_schedule(self):
        """
        在待调度状态时，调度员开始一次调度，报修状态由待调度转为报修中
        :return:
        """
        # 1. 将报修状态由待调度转为报修中
        self.repair.switch_state()
        print("调度员>>> 调度成功")
        # 2. 让维修工人根据报修任务去工作
        self.worker.work()

    def reset_schedule(self):
        """
        case1. 在报修中状态时，维修工人发现自己的工种不匹配时，进行重新调度，报修状态由报修中转为待调度
        case2. 这个任务需要多次调度
        :return:
        """
        # 1. 将报修状态由报修中转为待调度
        self.repair.reset_state()
        # 2. 通知调度员重新开始一个调度
        self.scheduler.start_schedule()

    def end_schedule(self):
        """
        在报修中状态时，维修工人完成了一次维修，结束一次调度，报修状态由报修中转为已报修，生成一个评价记录给用户
        :return:
        """
        # 1. 将报修状态转为已报修
        self.repair.switch_state()
        print("调度员>>> 调度结束，生成评价记录")
        # 2. 报修记录生成对应的评价记录，让用户进行评价
        self.repair.generate_feedback()
