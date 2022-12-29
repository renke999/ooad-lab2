from Test.TestBase import *
import datetime

from Worker import Worker
from Repair import Repair


class TestRepair(MockTest):

    def testSimpleSchedule(self):
        repair_dct = {'repair_id': 12, 'repair_time': datetime.datetime(2022, 12, 29, 19, 50, 50), 'repair_state': '调度中', 'fault_name': '下水道',
                      'user_id': 1, 'source': 'phone', 'repair_content': '测试用例', 'complex_repair': 0, 'remaining_step': 0, }
        repair = Repair(**repair_dct)
        worker_dct = {'worker_id': 3, 'fault_name': '下水道', 'is_free': 0, }
        worker = Worker(**worker_dct)

        worker.handle_schedule_simple(repair=repair)

        repair_dct['repair_state'] = '已调度'
        self.assertEqual(self.instance.get_dict_data_select("""select * from repair where repair_id = %d;""" % repair_dct['repair_id']),
                         [repair_dct])
        worker_dct['is_free'] = 1
        worker_dct['schedule_id'] = None
        self.assertEqual(self.instance.get_dict_data_select("""select * from worker where worker_id = %d;""" % worker_dct['worker_id']),
                         [worker_dct])
