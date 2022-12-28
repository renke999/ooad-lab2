from Repair import Repair

from Singleton import Singleton
from util import get_fault_and_content


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
        print(self.user_id, 'complaint')


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

    user_control_lst = ['user.ask_for_repair', 'user.ask_for_feedback', 'user.ask_for_complaint', ]

    idx = int(input("报修请按'1'，反馈请按'2'，投诉请按'3'，退出请按'4'：\n>>>"))
    while idx != 4:
        try:
            eval(user_control_lst[idx - 1])()
        except (NameError, IndexError):
            print('请输入正确的指令编号！')
        idx = int(input("报修请按'1'，反馈请按'2'，投诉请按'3'，退出请按'4'：\n>>>"))
