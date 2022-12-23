from Fault import *
from User import *
from Scheduler import *
from Worker import *
from Feedback import *
from WorkRecord import *
from Manager import Manager



if __name__ == '__main__':

    # 0. 预定义一些故障类别
    fault1 = Fault("电", 1)
    fault2 = Fault("水", 2)
    fault3 = Fault("燃", 3)


    # 1. 创建业主，调度员，经理，处理电、水、燃故障的维修工
    user = User(id=1, phone='p1', wechat='vx1')
    scheduler = Scheduler(1)
    manager = Manager()

    worker1 = Worker(id=1, fault=fault1)
    worker2 = Worker(id=2, fault=fault2)
    worker3 = Worker(id=3, fault=fault3)

    # 2. 业主发起两个"电"故障的报修，报修来源是微信
    repair1 = user.init_repair(fault=fault1, source="wechat")

    # 3. 调度员在合适的时间进行调度，将报修分配给维修工，维修工完成后通知业主完成了，业主给出评价
    scheduler.start_schedule()

    # 4. 业主发起"水"故障的报修，报修来源是手机
    repair2 = user.init_repair(fault=fault1, source="wechat")

    # 5. 调度员认为这是个复杂的，需要调度3步的任务
    scheduler.set_complex_repair_and_remaining_step(repair2, complex_repair=True, remaining_step=3)

    # 6. 调度员开始调度
    scheduler.start_schedule()

    # 7. 系统中没有调度任务了，调度员此次调度会提示没有调度任务
    scheduler.start_schedule()

    # 8. 用户对repair1发起投诉
    user.make_complaint(repair1)

    # 9. 经理处理所有投诉
    manager.handle_complaint()




    # 查看内存数据库存储的内容，测试一下
    #print(FEEDBACK_DICT[0].time_score)
    #print(WORK_RECORD_DICT[0].work_content)
