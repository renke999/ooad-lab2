from Test.TestBase import *
from copy import deepcopy

from Reply import Reply


class TestReply(MockTest):

    def testCommitReply(self):
        reply_dct = {'complaint_id': 3, 'scheduler_id': 1, 'worker_id': 1, 'reply_content': None, }
        reply = Reply(**reply_dct)
        reply_id_1, reply_id_2 = reply.commit_reply()
        reply_dct1, reply_dct2 = deepcopy(reply_dct), deepcopy(reply_dct)
        reply_dct1['reply_id'] = reply_id_1
        reply_dct1['worker_id'] = None
        self.assertEqual(self.instance.get_dict_data_select("""select * from reply where reply_id = %d;""" % reply_id_1),
                         [reply_dct1])
        reply_dct2['reply_id'] = reply_id_2
        reply_dct2['scheduler_id'] = None
        self.assertEqual(self.instance.get_dict_data_select("""select * from reply where reply_id = %d;""" % reply_id_2),
                         [reply_dct2])

