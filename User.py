from Singleton import Singleton
from util import get_fault_and_content

from Repair import Repair, select_one_repair
from Complaint import Complaint


class User:

    def __init__(self, **kwargs):

        self.user_id = kwargs['user_id'] if 'user_id' in kwargs else None
        self.phone = kwargs['phone'] if 'phone' in kwargs else None
        self.wechat = kwargs['wechat'] if 'wechat' in kwargs else None

        self.instance = Singleton.getInstance()

    def ask_for_repair(self):
        fault_name, repair_content = get_fault_and_content()
        source = ['phone', 'wechat'][int(input("电话报修请按'1'，微信报修请按'2'：\n>>>")) - 1]
        repair = Repair(fault_name=fault_name, user_id=self.user_id, source=source, repair_content=repair_content)
        repair.commit_repair()

    def ask_for_feedback(self):
        print(self.user_id, 'feedback')

    def ask_for_complaint(self):
        print("已调度报修列表：")
        repair_lst = self.instance.get_dict_data_select("""select * from repair where repair_state = '已调度' and user_id = %d;""" % self.user_id)
        print("\n".join(['\t' + str(dct) for dct in repair_lst]) if len(repair_lst) else "\t空")
        repair_id = int(input("请根据'repair_id'选择投诉，退出请输入'0'：\n>>>"))
        while repair_id != 0:
            try:
                repair = list(filter(lambda x: x['repair_id'] == repair_id, repair_lst))[0]
                repair = Repair(**repair)
                complaint_content = input("请大致描述下需要投诉的内容：\n>>>")
                complaint = Complaint(repair_id=repair.repair_id, complaint_content=complaint_content, is_done=False)
                complaint.commit_complaint()
            except IndexError:
                print("输入'repair_id'错误，请重新输入：\n")
                continue
            repair_id = int(input("请根据'repair_id'选择投诉，退出请输入'0'：\n>>>"))

    def browse_reply(self):
        print("已回复投诉列表：")
        complaint_lst = self.instance.get_dict_data_select(
            """select * from complaint join repair on complaint.repair_id = repair.repair_id 
            where is_done = true and user_id = %d;""" % self.user_id)
        print("\n".join(['\t' + str(dct) for dct in complaint_lst]) if len(complaint_lst) else "\t空")
        complaint_id = int(input("请根据'complaint_id'选择投诉，退出请输入'0'：\n>>>"))
        while complaint_id != 0:
            try:
                complaint = list(filter(lambda x: x['complaint_id'] == complaint_id, complaint_lst))[0]
                reply_lst = self.instance.get_dict_data_select(
                    """select * from reply where complaint_id = %d;""" % complaint_id)
                print("\n".join(['\t' + str(dct) for dct in reply_lst]) if len(reply_lst) else "\t空")
            except IndexError:
                print("输入'complaint_id'错误，请重新输入：\n")
                continue
            complaint_id = int(input("请根据'complaint_id'选择投诉，退出请输入'0'：\n>>>"))


if __name__ == '__main__':

    singleton = Singleton.getInstance()
    print("用户列表：")

    user_lst = singleton.get_dict_data_select("""select * from user;""")
    print("".join(['\t' + str(dct) + '\n' for dct in user_lst]))

    user = None
    user_id = int(input("请根据'user_id'选择用户：\n>>>"))
    while user is None:
        try:
            user = list(filter(lambda x: x['user_id'] == user_id, user_lst))[0]
        except IndexError:
            user_id = int(input("输入'user_id'错误，请重新输入：\n>>>"))
    user = User(**user)

    user_control_lst = ['user.ask_for_repair', 'user.ask_for_feedback', 'user.ask_for_complaint', 'user.browse_reply', ]

    idx = int(input("报修请按'1'，反馈请按'2'，投诉请按'3'，投诉回复请按'4'，退出请按'5'：\n>>>"))
    while idx != 5:
        try:
            eval(user_control_lst[idx - 1])()
        except (NameError, IndexError):
            print('请输入正确的指令编号！')
        idx = int(input("报修请按'1'，反馈请按'2'，投诉请按'3'，投诉回复请按'4'，退出请按'5'：\n>>>"))
