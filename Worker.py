import datetime

from Singleton import Singleton
from util import get_fault_and_content

from Repair import Repair
from Schedule import Schedule
from WorkRecord import WorkRecord


class Worker:

    def __init__(self, **kwargs):
        self.worker_id = kwargs['worker_id'] if 'worker_id' in kwargs else None
        self.fault_name = kwargs['fault_name'] if 'fault_name' in kwargs else None
        self.schedule_id = kwargs['schedule_id'] if 'schedule_id' in kwargs else None
        self.is_free = kwargs['is_free'] if 'is_free' in kwargs else None
        self.instance = Singleton.getInstance()

    def handle_schedule(self):
        print("您的待完成报修：")
        if self.is_free is True or self.schedule_id is None:
            print("\t空")
            return
        repair_schedule = self.instance.get_dict_data_select("""select * from repair join schedule on repair.repair_id = schedule.repair_id where schedule_id = %d;""" % self.schedule_id)[0]
        print('\t', repair_schedule)
        repair = Repair(**repair_schedule)
        schedule = Schedule(**repair_schedule)
        is_right = int(input("维修开始，请首先确认报修类型是否正确\n正确报修请按'1'，错误报修请按'0'：\n>>>"))
        if is_right == 0:
            self.handle_schedule_wrong(schedule, repair)
        elif repair.complex_repair:
            self.handle_schedule_complex(schedule, repair)
        else:
            self.handle_schedule_simple(schedule, repair)

    def handle_schedule_wrong(self, schedule: Schedule, repair: Repair):
        schedule.wrong_schedule()
        repair.switch_state(repair_state='待调度')
        fault_name, repair_content = get_fault_and_content()
        repair.change_fault(fault_name=fault_name, repair_content=repair_content)
        self.free_worker()

    def handle_schedule_simple(self, schedule: Schedule, repair: Repair):
        self.do_schedule(schedule)
        repair.switch_state(repair_state='已调度')
        self.free_worker()
        print("辛苦了，该维修工作已完成\n")

    def handle_schedule_complex(self, schedule: Schedule, repair: Repair):
        self.do_schedule(schedule)
        work_count = self.instance.get_dict_data_select("""select count(*) from work_record where schedule_id = %d;""" % self.schedule_id)[0]['count(*)']
        if work_count < repair.remaining_step:
            print("辛苦了，完成进度 %d / %d\n" % (work_count, repair.remaining_step))
        else:
            repair.switch_state(repair_state='已调度')
            self.free_worker()
            print("辛苦了，该维修工作已完成\n")

    def free_worker(self):
        sql = """update worker set schedule_id = null, is_free = true where worker_id = %d;""" % self.worker_id
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.schedule_id = None
        self.is_free = True

    def busy_worker(self, schedule_id):
        sql = """update worker set schedule_id = %d, is_free = False where worker_id = %d""" % (schedule_id, self.worker_id)
        self.instance.cursor.execute(sql)
        self.instance.conn.commit()
        self.schedule_id = schedule_id
        self.is_free = False

    def do_schedule(self, schedule: Schedule):
        start_time = datetime.datetime.now()
        work_content = input("开始工作，请输入工作内容\n>>>")
        work_record = WorkRecord(schedule_id=schedule.schedule_id, start_time=start_time, work_content=work_content)
        work_record.commit_work_record()

    def handle_feedback(self):
        print('handle_feedback')
        pass


if __name__ == '__main__':

    singleton = Singleton.getInstance()
    print("维修工列表：")

    worker_lst = singleton.get_dict_data_select("""select * from worker;""")
    print("".join(['\t' + str(dct) + '\n' for dct in worker_lst]))

    worker = None
    worker_id = int(input("请根据'worker_id'选择调度员：\n>>>"))
    while worker is None:
        try:
            worker = list(filter(lambda x: x['worker_id'] == worker_id, worker_lst))[0]
        except IndexError:
            worker_id = int(input("输入'worker_id'错误，请重新输入：\n>>>"))

    worker = Worker(**worker)

    worker_control_lst = ['worker.handle_schedule', 'worker.handle_feedback', ]

    idx = int(input("处理报修请按'1'，处理反馈请按'2'，退出请按'3'：\n>>>"))
    while idx != 3:
        try:
            eval(worker_control_lst[idx - 1])()
        except (NameError, IndexError):
            print('请输入正确的指令编号！')
        idx = int(input("处理报修请按'1'，处理反馈请按'2'，退出请按'3'：\n>>>"))
