from Singleton import Singleton


def get_fault_and_content():
    instance = Singleton.getInstance()
    lst = instance.get_dict_data_select("""select * from fault;""")
    prt = "，".join(["%s报修请按\'%d\'" % (dct['fault_name'], i + 1) for i, dct in enumerate(lst)])
    fault_name = lst[int(input(prt + '：\n>>>')) - 1]['fault_name']
    repair_content = input("请大致描述下需要报修的内容：\n>>>")
    return fault_name, repair_content

