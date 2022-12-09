from Schedule import Schedule_DICT
from Complaint import Complaint_DICT

# TODO 在数据库中完成查找

# 不设置Manager表了，假设只有1个manager
class Manager:
    def __init__(self):
        pass

    def handle_complaint(self):
        for complaint in Complaint_DICT.values():
            # 1. 遍历所有投诉记录，找到没有处理的解决
            if not complaint.is_done():
                print("\n==================================================")
                print("经理>>> 发现投诉，开始联系维修工和调度员进行处理")
                repair = complaint.get_repair()
                repair_id = repair.get_id()
                # 2. 找到该投诉记录对应的调度
                for schedule in Schedule_DICT.values():
                    if repair_id == schedule.get_repair().get_id():
                        # 3. 找到该调度对应的维修工和调度员
                        # TODO 在数据库中找维修工和调度员
                        worker = schedule.get_worker()
                        scheduler = schedule.get_scheduler()
                        # 4. 维修工和调度员对投诉进行回应
                        worker.handle_complaint()
                        scheduler.handle_complaint()
                        # 5. 经理关闭投诉
                        complaint.set_done(True)
                        print("经理>>> 投诉处理成功，关闭投诉")
                        print("==================================================\n")
