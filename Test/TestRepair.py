from Test.TestBase import *
import datetime

from Repair import Repair


class TestRepair(MockTest):

    def testCommitRepair(self):
        repair_dct = {'repair_time': datetime.datetime.now().replace(microsecond=0), 'repair_state': '待调度', 'fault_name': '下水道',
                      'user_id': 1, 'source': 'phone', 'repair_content': '测试用例', 'complex_repair': 0, 'remaining_step': 0, }
        repair = Repair(**repair_dct)
        repair_id = repair.commit_repair()
        repair_dct['repair_id'] = repair_id
        self.assertEqual(self.instance.get_dict_data_select("""select * from repair where repair_id = %d;""" % repair_id),
                         [repair_dct])

