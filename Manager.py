
from Singleton import Singleton

from Schedule import Schedule
from Complaint import Complaint
from Reply import Reply


class Manager:

    def __init__(self, **kwargs):

        self.manager_id = kwargs['manager_id'] if 'manager_id' in kwargs else None
        self.instance = Singleton.get_instance()

    def handle_complaint_frontend(self):
        print("待处理投诉列表：")
        complaint_lst = self.instance.get_dict_data_select("""select * from complaint where is_done = false;""")
        print("\n".join(['\t' + str(dct) for dct in complaint_lst]) if len(complaint_lst) else "\t空")
        complaint_id = int(input("请根据'complaint_id'选择投诉，退出请输入'0'：\n>>>"))
        if complaint_id != 0:
            try:
                complaint = list(filter(lambda x: x['complaint_id'] == complaint_id, complaint_lst))[0]
                complaint = Complaint(**complaint)
                self.handle_complaint_backend(complaint)
            except IndexError:
                print("输入'complaint_id'错误，请重新发起投诉处理请求：\n")

    def handle_complaint_backend(self, complaint: Complaint):
        schedule_lst = self.instance.get_dict_data_select("""select * from schedule where is_right = true and repair_id = %d;""" % complaint.repair_id)
        schedule = Schedule(**schedule_lst[0])
        reply = Reply(complaint_id=complaint.complaint_id, scheduler_id=schedule.scheduler_id, worker_id=schedule.worker_id)
        reply.commit_reply()

    def close_complaint_frontend(self):
        print("已回复投诉列表：")
        complaint_lst = self.instance.get_dict_data_select(
            """select * from complaint join reply on complaint.complaint_id = reply.complaint_id 
            where reply_content is not null and is_done is false;""")
        print("\n".join(['\t' + str(dct) for dct in complaint_lst]) if len(complaint_lst) else "\t空")
        complaint_id = int(input("请根据'complaint_id'关闭投诉，退出请输入'0'：\n>>>"))
        if complaint_id != 0:
            try:
                complaint = list(filter(lambda x: x['complaint_id'] == complaint_id, complaint_lst))[0]
                complaint = Complaint(**complaint)
                complaint.close_complaint()
            except IndexError:
                print("输入'complaint_id'错误，请重新发起关闭投诉请求：\n")


if __name__ == '__main__':

    singleton = Singleton.get_instance()
    print("物业经理列表：")

    manager_lst = singleton.get_dict_data_select("""select * from manager;""")
    print("".join(['\t' + str(dct) + '\n' for dct in manager_lst]))

    manager = None
    manager_id = int(input("请根据'manager_id'选择物业经理：\n>>>"))
    while manager is None:
        try:
            manager = list(filter(lambda x: x['manager_id'] == manager_id, manager_lst))[0]
        except IndexError:
            manager_id = int(input("输入'manager_id'错误，请重新输入：\n>>>"))

    manager = Manager(manager_id=manager['manager_id'])

    manager_control_lst = ['manager.handle_complaint_frontend', 'manager.close_complaint_frontend', ]

    idx = int(input("处理投诉请按'1'，关闭投诉请按'2'，退出请按'3'：\n>>>"))
    while idx != 3:
        try:
            eval(manager_control_lst[idx - 1])()
        except (NameError, IndexError):
            print('请输入正确的指令编号！')
        idx = int(input("处理投诉请按'1'，关闭投诉请按'2'，退出请按'3'：\n>>>"))
