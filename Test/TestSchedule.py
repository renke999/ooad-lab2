from Test.TestBase import *

from Schedule import Schedule


class TestSchedule(MockTest):

    def testCommitSchedule(self):
        schedule_dct = {'scheduler_id': 1, 'worker_id': 1, 'repair_id': 10, 'is_right': 1, }
        schedule = Schedule(**schedule_dct)
        schedule_id = schedule.commit_schedule()
        schedule_dct['schedule_id'] = schedule_id
        self.assertEqual(self.instance.get_dict_data_select("""select * from schedule where schedule_id = %d;""" % schedule_id),
                         [schedule_dct])

