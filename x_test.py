
from User import *
from Scheduler import *
from Worker import *
from Feedback import *
from WorkRecord import *
from Manager import Manager


class Fault:
    """
    故障类
    """

#    fault_count = 0

    def __init__(self, name, id):
        # 故障名
        self.name = name
        self.id = id
        

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id


fault1 = Fault("电", 1)
fault2 = Fault("水", 2)
fault3 = Fault("燃", 3)


user = User(id=1, phone="p1", wechat="vx1")


worker1 = Worker(id=1, fault=fault1)
worker2 = Worker(id=2, fault=fault2)
worker3 = Worker(id=3, fault=fault3)

worker1.set_free(False)
