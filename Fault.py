# TODO 创建一个新的sql故障类型表
# 故障类型数据库
FAULT_DICT = {}


class Fault:
    """
    故障类
    """

    fault_count = 0

    def __init__(self, name):
        # 故障名
        self.name = name

        # TODO 用sql insert加入到数据库中
        self.id = Fault.fault_count
        FAULT_DICT[self.id] = self
        Fault.fault_count += 1

    def get_name(self):
        return self.name
