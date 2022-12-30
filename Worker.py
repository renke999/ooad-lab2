import datetime

from Singleton import Singleton
from util import get_fault_and_content

from Repair import Repair
from Schedule import Schedule
from Reply import Reply


class Worker:

    def __init__(self, **kwargs):
        self.worker_id = kwargs['worker_id'] if 'worker_id' in kwargs else None
        self.fault_name = kwargs['fault_name'] if 'fault_name' in kwargs else None
        self.schedule_id = kwargs['schedule_id'] if 'schedule_id' in kwargs else None
        self.is_free = kwargs['is_free'] if 'is_free' in kwargs else None
        self.instance = Singleton.get_instance()

    def handle_schedule_frontend(self):
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
            schedule.wrong_schedule()
            self.handle_schedule_wrong(repair)
        elif repair.complex_repair:
            schedule.right_schedule()
            self.handle_schedule_complex(repair)
        else:
            schedule.right_schedule()
            self.handle_schedule_simple(repair)

    def handle_schedule_wrong(self, repair: Repair):
        repair.switch_state(repair_state='待调度')
        fault_name, repair_content = get_fault_and_content()
        repair.change_fault(fault_name=fault_name, repair_content=repair_content)
        self.free_worker()

    def handle_schedule_simple(self, repair: Repair):
        repair.switch_state(repair_state='已调度')
        self.free_worker()
        print("辛苦了，该维修工作已完成\n")

    def handle_schedule_complex(self, repair: Repair):
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

    def handle_complaint_frontend(self):
        print("待回复投诉列表：")
        reply_lst = self.instance.get_dict_data_select(
            """select * from reply join complaint on reply.complaint_id = complaint.complaint_id
             where reply_content is null and worker_id = %d;""" % self.worker_id)
        print("\n".join(['\t' + str(dct) for dct in reply_lst]) if len(reply_lst) else "\t空")
        complaint_id = int(input("请根据'complaint_id'选择，退出请输入'0'：\n>>>"))
        if complaint_id != 0:
            try:
                reply = list(filter(lambda x: x['complaint_id'] == complaint_id, reply_lst))[0]
                reply = Reply(**reply)
                reply_content = input("开始回复，请输入回复内容\n>>>")
                reply.update_reply(reply_content=reply_content)
            except IndexError:
                print("输入'complaint_id'错误，请重新发起投诉处理请求：\n")


if __name__ == '__main__':

    singleton = Singleton.get_instance()
    print("维修工列表：")

    worker_lst = singleton.get_dict_data_select("""select * from worker;""")
    print("".join(['\t' + str(dct) + '\n' for dct in worker_lst]))

    worker = None
    worker_id = int(input("请根据'worker_id'选择维修工：\n>>>"))
    while worker is None:
        try:
            worker = list(filter(lambda x: x['worker_id'] == worker_id, worker_lst))[0]
        except IndexError:
            worker_id = int(input("输入'worker_id'错误，请重新输入：\n>>>"))

    worker = Worker(**worker)

    worker_control_lst = ['worker.handle_schedule_frontend', 'worker.handle_complaint_frontend', ]

    idx = int(input("处理报修请按'1'，处理投诉请按'2'，退出请按'3'：\n>>>"))
    while idx != 3:
        try:
            eval(worker_control_lst[idx - 1])()
        except (NameError, IndexError):
            print('请输入正确的指令编号！')
        idx = int(input("处理报修请按'1'，处理投诉请按'2'，退出请按'3'：\n>>>"))
