import unittest

from Component import Singleton
from Command import Invoker

from util import update_sys_argv


validList = [(None, '个⼈收藏'), ('个⼈收藏', '课程'),
             ('课程', 'elearning'), ('课程', 'ehall'), ('个⼈收藏', '参考资料'), ('参考资料', '函数式'),
             ('函数式', 'JFP'), ('参考资料', '⾯向对象'), ('个⼈收藏', '待阅读'), ('待阅读', 'Category Theory')]


class TestOpen(unittest.TestCase):

    def setUp(self):
        self.invoker = Invoker()
        update_sys_argv(['open', 'test.bmk'])
        self.invoker.open()

    def testOpen(self):
        tempList = [(component.getRoot(), component.getName()) for component in Singleton.__instance__.getAllComponents()]
        self.assertEqual(validList, tempList)
