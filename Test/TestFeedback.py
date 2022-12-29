from Test.TestBase import *

from Feedback import Feedback


class TestFeedback(MockTest):

    def testCommitFeedback(self):
        feedback_dct = {'repair_id': 1, 'time_score': 5, 'attitude_score': 5, 'satisfy_score': 5, }
        feedback = Feedback(**feedback_dct)
        feedback_id = feedback.commit_feedback()
        feedback_dct['feedback_id'] = feedback_id
        self.assertEqual(self.instance.get_dict_data_select("""select * from feedback where feedback_id = %d;""" % feedback_id),
                         [feedback_dct])

