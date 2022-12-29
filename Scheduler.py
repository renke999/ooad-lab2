
from Singleton import Singleton

from Repair import Repair
from Schedule import Schedule
from Worker import Worker
from Reply import Reply


class Scheduler:

    def __init__(self, **kwargs):

        self.scheduler_id = kwargs['scheduler_id'] if 'scheduler_id' in kwargs else None
        self.instance = Singleton.getInstance()

    def handle_schedule(self):
        print("待调度报修列表：")
        repair_lst = self.instance.get_dict_data_select("""select * from repair where repair_state = '待调度';""")
        print("\n".join(['\t' + str(dct) for dct in repair_lst]) if len(repair_lst) else "\t空")
        repair_id = int(input("请根据'repair_id'选择任务，退出请输入'0'：\n>>>"))
        while repair_id != 0:
            try:
                repair = list(filter(lambda x: x['repair_id'] == repair_id, repair_lst))[0]
                repair = Repair(**repair)
                self.handle_schedule_worker(repair)
            except IndexError:
                print("输入'repair_id'错误，请重新输入：\n")
                continue
            repair_id = int(input("请根据'repair_id'选择任务，退出请输入'0'：\n>>>"))

    def handle_schedule_worker(self, repair: Repair):
        print("可调度维修工列表：")
        worker_lst = self.instance.get_dict_data_select("""select * from worker where is_free = true and fault_name = '%s';""" % repair.fault_name)
        print("\n".join(['\t' + str(dct) for dct in worker_lst]) if len(worker_lst) else "\t空")
        worker_id = int(input("请根据'worker_id'选择维修工，输入其他数字自动退出：\n>>>"))
        worker = list(filter(lambda x: x['worker_id'] == worker_id, worker_lst))
        if worker:
            worker = Worker(**worker[0])
            schedule = Schedule(scheduler_id=self.scheduler_id, worker_id=worker_id, repair_id=repair.repair_id)
            schedule_id = schedule.commit_schedule()
            repair.switch_state(repair_state='调度中')
            worker.busy_worker(schedule_id=schedule_id)
        else:
            print("输入'worker_id'错误，已自动回退，请重新选择报修调度\n")

    def handle_complaint(self):
        print("待回复投诉列表：")
        reply_lst = self.instance.get_dict_data_select(
            """select * from reply where reply_content is null and scheduler_id = %d;""" % self.scheduler_id)
        print("\n".join(['\t' + str(dct) for dct in reply_lst]) if len(reply_lst) else "\t空")
        complaint_id = int(input("请根据'complaint_id'选择，退出请输入'0'：\n>>>"))
        while complaint_id != 0:
            try:
                reply = list(filter(lambda x: x['complaint_id'] == complaint_id, reply_lst))[0]
                reply = Reply(**reply)
                reply_content = input("开始回复，请输入回复内容\n>>>")
                reply.update_reply(reply_content=reply_content)
            except IndexError:
                print("输入'complaint_id'错误，请重新输入：\n")
                continue
            complaint_id = int(input("请根据'complaint_id'选择任务，退出请输入'0'：\n>>>"))


if __name__ == '__main__':

    singleton = Singleton.getInstance()
    print("调度员列表：")

    scheduler_lst = singleton.get_dict_data_select("""select * from scheduler;""")
    print("".join(['\t' + str(dct) + '\n' for dct in scheduler_lst]))

    scheduler = None
    scheduler_id = int(input("请根据'scheduler_id'选择调度员：\n>>>"))
    while scheduler is None:
        try:
            scheduler = list(filter(lambda x: x['scheduler_id'] == scheduler_id, scheduler_lst))[0]
        except IndexError:
            scheduler_id = int(input("输入'scheduler_id'错误，请重新输入：\n>>>"))

    scheduler = Scheduler(scheduler_id=scheduler['scheduler_id'])

    scheduler_control_lst = ['scheduler.handle_schedule', 'scheduler.handle_complaint', ]

    idx = int(input("处理报修请按'1'，处理投诉请按'2'，退出请按'3'：\n>>>"))
    while idx != 3:
        try:
            eval(scheduler_control_lst[idx - 1])()
        except (NameError, IndexError):
            print('请输入正确的指令编号！')
        idx = int(input("处理报修请按'1'，处理投诉请按'2'，退出请按'3'：\n>>>"))
