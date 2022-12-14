from Schedule import Schedule
# from Repair import REPAIR_DICT
# from Worker import WORKER_DICT


from Singleton import Singleton

# # TODO 创建sql数据库
# SCHEDULER_DICT = {}


class Scheduler:
    """
    调度员
    和报修、维修工、调度相关联
    """

    def __init__(self, id):  # repair=None, worker=None, schedule=None
        """

        :param repair: Repair类成员，报修
        :param worker: Worker类成员，调度员根据报修派遣的维修工
        :param schedule: Schedule类成员，调度员对应的调度
        """
        self.id = id
        # self.repair = repair
        # self.worker = worker
        # self.schedule = schedule

        #SCHEDULER_DICT[self.id] = self
        singleton = Singleton.getInstance()
        sql = """insert p_scheduler(id) values (%s);""" % (self.id)
        singleton.cursor.execute(sql)
        singleton.conn.commit()

    def get_id(self):
        return self.id

    def handle_complaint(self):
        input("调度员>>> 请对投诉记录进行回复：")

    def set_complex_repair_and_remaining_step(self, repair, complex_repair, remaining_step):
        """
        调度员可能认为这是个复杂任务，设置复杂任务为true以及需要处理的步骤
        :param repair: 报修记录
        :param complex_repair: 是否是个复杂任务
        :param remaining_step: 如果是个复杂任务，剩余需要调度的次数
        :return:
        """
        repair.set_complex_repair_and_remaining_step(complex_repair, remaining_step)

    def start_schedule(self):
        """

        :return:
        """

        # 1. 判断系统中是否存在调度中的报修，如果存在则不能调度（扩展流程要求只能有1个活跃的调度）
        # for repair in REPAIR_DICT.values():
        #     if repair.is_doing_state():
        #         print("调度员>>> 系统中存在调度中的报修，不能继续调度")
        #         return
        singleton = Singleton.getInstance()
        sql = """select * from p_repair where state_id = 1"""
        singleton.cursor.execute(sql)
        if singleton.cursor.fetchone():
            print("调度员>>> 系统中存在调度中的报修，不能继续调度")
            return

        # 2. 在REPAIR_DICT（报修数据库）中选择一个时间最早且调度状态为未调度的repair
        # self.repair = None
        # for repair in REPAIR_DICT.values():
        #     if repair.is_todo_state():
        #         self.repair = repair
        sql = """select * from p_repair where state_id = 0"""
        singleton.cursor.execute(sql)
        row_repair = singleton.cursor.fetchone()
        if not row_repair:
        #if not self.repair:
            print("调度员>>> 系统中暂无待调度的报修")
            return

        # 3. 调用repair.get_fault()方法，得到故障类型
        fault = row_repair[2]

        # TODO 在数据库中查询
        # 4. 在WORKER_DICT（维修工数据库）中选择一个和故障类型匹配且空闲的维修工，将这个报修分配给他
        sql = """select * from p_worker where is_free = True and fault_id = %s""" % (fault)
        singleton.cursor.execute(sql)
        row_worker = singleton.cursor.fetchone()
        # for worker in WORKER_DICT.values():
        #     if worker.get_fault() == fault and worker.get_free():
        #         self.worker = worker
        #         break
        if not row_worker:
            print("无合适或空闲工人可调用")
            return
        # 4. 将维修工的空状态设置为False
        WORKER_DICT[row_worker[0]].set_free(False)
        #self.worker.set_free(False)

        # 5. 创建一个schedule类（调度类）
        schedule = Schedule(scheduler=self, worker=WORKER_DICT[row_worker[0]], repair=REPAIR_DICT[row_repair[0]])

        # 6. 将维修任务分配给维修工，维修状态由待调度转为报修中，维修工处理任务并返回处理结果
        schedule.start_schedule()

        # 7. 更新数据库中调度员信息
        # SCHEDULER_DICT[self.id] = self
