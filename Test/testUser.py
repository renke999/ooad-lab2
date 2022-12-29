import io
import sys

from util import update_sys_argv
from Test.testBase import TestOpen

addValid = '├── 个⼈收藏\n' \
           '│   ├── 课程\n' \
           '│   │   ├── elearning\n' \
           '│   │   └── ehall\n' \
           '│   ├── 参考资料\n' \
           '│   │   ├── 函数式\n' \
           '│   │   │   └── JFP\n' \
           '│   │   └── ⾯向对象\n' \
           '│   └── 待阅读\n' \
           '│       └── Category Theory\n└── 读书笔记\n'
deleteValid = '└── 个⼈收藏\n' \
              '    ├── 课程\n' \
              '    │   ├── elearning\n' \
              '    │   └── ehall\n' \
              '    ├── 参考资料\n' \
              '    │   ├── 函数式\n' \
              '    │   │   └── JFP\n' \
              '    │   └── ⾯向对象\n' \
              '    └── 待阅读\n' \
              '        └── Category Theory\n'


class TestAddTitle(TestOpen):

    def setUp(self) -> None:
        super().setUp()

    def testAddTitle(self):
        sys.stdout = io.StringIO()
        update_sys_argv(['open', 'test.bmk'])
        self.invoker.open()
        update_sys_argv(['add-title', '读书笔记'])
        self.invoker.addTitle()
        update_sys_argv(['show-tree'])
        self.invoker.showTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(addValid, content)

    def testDeleteTitle(self):
        sys.stdout = io.StringIO()
        update_sys_argv(['delete-title', '读书笔记'])
        self.invoker.deleteTitle()
        update_sys_argv(['show-tree'])
        self.invoker.showTree()
        content = str(sys.stdout.getvalue())
        self.assertEqual(deleteValid, content)
