from Test.TestBase import *
import datetime

from WorkRecord import WorkRecord


class TestWorkRecord(MockTest):

    def testCommitWorkRecord(self):
        work_record_dct = {'schedule_id': 10, 'start_time': datetime.datetime.now().replace(microsecond=0),
                           'end_time': datetime.datetime.now().replace(microsecond=0), 'work_content': '测试用例', }
        work_record = WorkRecord(**work_record_dct)
        work_record_id = work_record.commit_work_record()
        work_record_dct['work_record_id'] = work_record_id
        self.assertEqual(self.instance.get_dict_data_select("""select * from work_record where work_record_id = %d;""" % work_record_id),
                         [work_record_dct])

