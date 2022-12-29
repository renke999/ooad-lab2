import pymysql


class Singleton:
    __instance__ = None

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='2000825lxr', charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute("use property")

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_index_dict(self):
        index_dict = dict()
        index = 0
        for desc in self.cursor.description:
            index_dict[desc[0]] = index
            index = index + 1
        return index_dict

    def get_dict_data_select(self, query):
        self.cursor.execute(query)
        raw_list = self.cursor.fetchall()
        index_dict = self.get_index_dict()
        dst_list = []
        for raw_item in raw_list:
            dst_item = dict()
            for index in index_dict:
                dst_item[index] = raw_item[index_dict[index]]
            dst_list.append(dst_item)
        return dst_list

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

    # instance.cursor.execute("create database property;")
    # instance.conn.commit()

    # 新建故障种类表
    sql = """
    create table if not exists fault(
        fault_name varchar(20) primary key,
        fault_desc varchar(50)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 创建业主数据表
    sql = """
    create table if not exists user(
        user_id int primary key,
        phone varchar(11),
        wechat varchar(21)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建维修工数据表
    sql = """
    create table if not exists worker(
        worker_id int primary key,
        fault_name varchar(20),
        schedule_id int,
        is_free bool,
        foreign key (fault_name) references fault(fault_name)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建调度员表
    sql = """
    create table if not exists scheduler(
        scheduler_id int primary key
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    sql = """
    create table if not exists manager(
        manager_id int primary key
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建报修记录表
    sql = """
    create table if not exists repair(
        repair_id int auto_increment primary key,
        repair_time datetime,
        repair_state varchar(30),
        fault_name varchar(20),
        user_id int,
        source varchar(21),
        repair_content varchar(50),
        complex_repair bool,
        remaining_step int,
        foreign key (fault_name) references fault(fault_name),
        foreign key (user_id) references user(user_id)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建调度记录表
    sql = """
    create table if not exists schedule(
        schedule_id int auto_increment primary key,
        scheduler_id int,
        worker_id int,
        repair_id int,
        is_right bool,
        foreign key (scheduler_id) references scheduler(scheduler_id),
        foreign key (worker_id) references worker(worker_id),
        foreign key (repair_id) references repair(repair_id)        
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 新建维修记录数据表
    sql = """
    create table if not exists work_record(
        work_record_id int auto_increment primary key,
        schedule_id int,
        start_time datetime,
        end_time datetime,
        work_content varchar(200),
        foreign key (schedule_id) references schedule(schedule_id)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    sql = """
    alter table worker add constraint fk_sid foreign key(schedule_id) references schedule(schedule_id);
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 创建评价数据表
    sql = """
    create table if not exists feedback(
        feedback_id int auto_increment primary key,
        repair_id int,
        time_score int,
        attitude_score int,
        satisfy_score int,
        foreign key (repair_id) references repair(repair_id)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 创建投诉数据表
    sql = """
    create table if not exists complaint(
        complaint_id int auto_increment primary key,
        repair_id int,
        complaint_content varchar(20),
        is_done bool,
        foreign key (repair_id) references repair(repair_id)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    # 创建投诉数据表
    sql = """
    create table if not exists reply(
        reply_id int auto_increment primary key,
        complaint_id int,
        scheduler_id int,
        worker_id int,
        reply_content varchar(20),
        foreign key (complaint_id) references complaint(complaint_id),
        foreign key (scheduler_id) references scheduler(scheduler_id),
        foreign key (worker_id) references worker(worker_id)
    );
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    sql = """
    insert into fault (fault_name, fault_desc) values 
    ('电梯', '################'), ('断电', '################'), ('下水道', '################');
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    sql = """
    insert into user (user_id, phone, wechat) values (1, 'p1', 'vx1'), (2, 'p2', 'vx2'), (3, 'p3', 'vx3');
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    sql = """
    insert into worker (worker_id, fault_name, is_free) values (1, '电梯', true), (2, '断电', true), (3, '下水道', true);
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    sql = """
    insert into scheduler (scheduler_id) values (1);
    """
    instance.cursor.execute(sql)
    instance.conn.commit()

    sql = """
    insert into manager (manager_id) values (1);
    """
    instance.cursor.execute(sql)
    instance.conn.commit()


