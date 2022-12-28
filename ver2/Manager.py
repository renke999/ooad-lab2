import Schedule
import Complaint

# TODO 在数据库中完成查找
from Singleton import Singleton


# 假设只有1个manager,故不新建表
class Manager:
    def __init__(self):
        pass

    def handle_complaint(self):
        singleton = Singleton.getInstance()
        sql = """select * from p_complaint"""
        singleton.cursor.execute(sql)
        allComplaint_db_result = singleton.cursor.fetchall()

        singleton.cursor.execute("use property")
        sql = """select * from p_schedule"""
        singleton.cursor.execute(sql)
        allSchedule_db_result = singleton.cursor.fetchall()
        for db_complaint in allComplaint_db_result:
            # 1. 遍历所有投诉记录，找到没有处理的解决
            if not db_complaint[3]:
                print("\n==================================================")
                print("经理>>> 发现投诉，开始联系维修工和调度员进行处理")
                repair_id = db_complaint[1]

                # 2. 找到该投诉记录对应的调度,比较repair_id
                for db_schedule in allSchedule_db_result:
                    if repair_id == db_schedule[3]:
                        # 3. 找到该调度对应的维修工和调度员
                        # TODO 在数据库中找维修工和调度员
                        # 如果找到对应的repair实例对象，直接在这里回复了（取巧了）
                        # worker = schedule.get_worker()
                        # scheduler = schedule.get_scheduler()
                        # 4. 维修工和调度员对投诉进行回应
                        input("维修工>>> 请对投诉记录进行回复：")
                        input("调度员>>> 请对投诉记录进行回复：")
                        # scheduler.handle_complaint()
                        # 5. 经理关闭投诉
                        # complaint.set_done(True)
                        singleton.cursor.execute("update p_complaint set done=%s where id=%s" % (True,db_complaint[0]))
                        print("经理>>> 投诉处理成功，关闭投诉")
                        print("==================================================\n")
        singleton.conn.commit()
