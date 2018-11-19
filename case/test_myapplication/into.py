import unittest
from appo.lib import HTMLTestRunner3
import os


class Into(unittest.TestCase):
    a = 1
    b = 2
    c = [1, 2, 3]
    def test_a_plus_b(self):
        """ a + b = 3 这个用例应该通过"""
        print('a + b = 3')
        self.assertEqual(self.a+self.b, 3)

    def test_a_minus_b(self):
        """ a - b = 3 这个用例应该失败 """
        print('a - b = 3')
        self.assertEqual(self.a-self.b, 3)

    def test_a_multi_b(self):
        """ a * b = 2 这个用例应该成功"""
        print('a * b = 2')
        self.assertEqual(self.a*self.b, 2)

    def test_a_divide_c(self):
        """ a / c = 1 这是个有subTest的用例"""
        for i in self.c:
            with self.subTest(i=i):
                print('a / c = 1')
                self.assertEqual(self.a / i, 1)

    def test_a_error_case(self):
        """ 除零异常 """
        print('1/0')
        self.assertEqual(self.a/0, 1)

class ExampleCase1(unittest.TestCase):
    """此class包含两个用例：add - ok， minus - FAIL"""
    a = 1
    b = 2
    c = [1, 2, 3]
    def setUp(self):
        self.a = 4
        self.b = 3

    def test_add(self):
        """用例1，add，此用例成功通过"""
        self.assertEqual(self.a + self.b, 7)

    def test_minus(self):
        """用例2，minus，此用例执行失败，4-3！=2"""
        print('中文方法反反复复凤飞飞反复')
        self.assertEqual(self.a - self.b, 2)


class ExampleCase2(unittest.TestCase):
    a = 1
    b = 2
    c = [1, 2, 3]
    """此class包含一个用例：plus - ERROR"""
    def setUp(self):
        self.a, self.b = 4, 3

    def test_plus(self):
        """用例3，plus，此用例执行出错，因为c未定义"""
        self.assertEqual(self.a * self.b, c)


class ExampleCase3(unittest.TestCase):
    a = 1
    b = 2
    c = [1, 2, 3]
    """此class包含一个用例：divide - ok"""
    def setUp(self):
        self.a, self.b = 4, 2

    def test_devide(self):
        """用例4，divide，此用例执行成功"""
        print('我要打印输出')
        self.assertEqual(self.a / self.b, 2)


# def execution_path():
#     driver.press_keycode(22)
#     driver.press_keycode(22)
#     driver.press_keycode(22)
#     driver.press_keycode(23)
#     driver.press_keycode(36)

if __name__ == '__main__':
    report_title = 'Example用例执行报告'
    desc = '用于展示修改样式后的HTMLTestRunner'
    # report_file = 'ExampleReport.html'
    report_file = os.path.join('D:/pycode/appo/result/report/report.html')
    print(report_file)
    testsuite = unittest.TestSuite()
    testsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(Into))
    testsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(ExampleCase1))
    testsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(ExampleCase2))
    testsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(ExampleCase3))

    with open(report_file, 'wb') as report:
        runner = HTMLTestRunner3.HTMLTestRunner(stream=report, title=report_title, description=desc)
        runner.run(testsuite)