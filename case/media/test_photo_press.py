from appo.case.basecase import BaseCase
import unittest
from appo.common import logger
import time


log = logger.model_logger('test_picture_press')
class Photo(unittest.TestCase,BaseCase):

    def setUp(self):
        caps = self.package_activity_main('xm_home')
        self.startUp(caps)
        self.common_case_type1()

    def tearDown(self):
        self.endDown()

    #图片轮播
    def test_toggleimage_press(self):
        self.driver.find_element_by_name('【多媒体】图片测试库').click()
        self.driver.press_keycode(23)
        # 2次20的key目的是显示所有的group_title
        self.driver.press_keycode(20)
        time.sleep(1)
        self.driver.press_keycode(20)
        filelist = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title') #图片文件夹
        while True:
            for file in filelist:  # file子文件夹
                subfilecount = file.text.split('-')[1]
                print(file.text)
                file.click()  # 点击进入图片列表
                imagelist = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title')  # 图片列表
                imagelist[0].click()  # 点击第一张图片开始轮播
                for i in range(int(subfilecount)):
                    self.driver.press_keycode(22)
                    time.sleep(1)
                self.driver.press_keycode(4)
                time.sleep(2)
                self.driver.press_keycode(4)


if __name__ == '__main__':
    p = Photo()
    p.setUp()
    p.test_toggleimage_press()

