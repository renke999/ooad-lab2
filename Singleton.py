import pymysql


class Singleton:
    __instance__ = None

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='2000825lxr', charset='utf8')
        self.cursor = self.conn.cursor()

    @staticmethod
    def getInstance():
        if Singleton.__instance__ is None:
            Singleton.__instance__ = Singleton()
            return Singleton.__instance__
        else:
            return Singleton.__instance__


if __name__ == "__main__":

    # 新建数据库property
    instance = Singleton.getInstance()

    instance.cursor.execute("create database property")
    instance.conn.commit()

    # 创建业主数据表
    instance.cursor.execute("use property")
    sql = """
    create table p_user(
        id int primary key,
        phone varchar(11),
        wechat varchar(21)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()


    # 新建维修工数据表
    sql = """
    create table p_worker(
        id int primary key,
        fault_id int,
        schedule_id int,
        is_free bool
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()


    # 新建维修记录数据表
    sql = """
    create table p_workrecord(
        id int primary key,
        worker_id int,
        start_time datetime,
        end_time datetime,
        work_content varchar(200)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建报修记录表
    sql = """
    create table p_repair(
        id int primary key,
        repair_time datetime,
        fault_id int,
        user_id int,
        source varchar(21),
        state_id int,
        complex_repair bool,
        remaining_step int
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建调度记录表
    sql = """
    create table p_schedule(
        id int primary key,
        schedule_id int,
        worker_id int,
        repair_id int
    );
    """

    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建调度员表
    sql = """
    create table p_scheduler(
        id int primary key
    );
    """

    instance.cursor.execute(sql)
    instance.conn.commit()

    # 创建投诉数据表
    # cursor.execute("use property")
    sql = """
    create table p_complaint(
        id int primary key,
        repair_id int,
        user_id int,
        done bool,
        repair_content varchar(20)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()


    # 新建故障种类表
    # cursor.execute("use property")
    sql = """
    create table p_fault(
        id int primary key,
        fault_name varchar(10)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 创建评价数据表
    # cursor.execute("use property")
    sql = """
    create table p_feedback(
        id int primary key,
        repair_id int,
        user_id int,
        time_score int,
        attitude_score int,
        satisfy_score int
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    instance.cursor.close()
    instance.conn.close()
