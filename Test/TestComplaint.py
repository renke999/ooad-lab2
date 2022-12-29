from Test.TestBase import *

from Complaint import Complaint


class TestComplaint(MockTest):

    def testCommitFeedback(self):
        complaint_dct = {'repair_id': 1, 'complaint_content': '测试用例', 'is_done': False, }
        complaint = Complaint(**complaint_dct)
        complaint_id = complaint.commit_complaint()
        complaint_dct['complaint_id'] = complaint_id
        self.assertEqual(self.instance.get_dict_data_select("""select * from complaint where complaint_id = %d;""" % complaint_id),
                         [complaint_dct])

