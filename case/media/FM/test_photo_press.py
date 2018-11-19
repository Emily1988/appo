from appo.case.basecase import BaseCase
import unittest
from appo.common import logger
import time

log = logger.model_logger('test_picture')


class Phote(unittest.TestCase, BaseCase):
    result = False

    def setUp(self):
        # caps = self.package_activity_main('fm_home')
        caps = self.package_activity_main('fm_media')
        self.startUp(caps)
        self.fm_common_case_type_media()

    def tearDown(self):
        self.endDown()

    # 一直向下移动，直到界面出现n个相同的元素为止
    def move_down_until_nsame_element(self, text, n):
        while True:
            eles = self.driver.find_elements_by_name(text)
            if len(eles) == n:
                break
            else:
                self.driver.press_keycode(20)

    # 滚动图片验证图片是否能打开
    def test_openimage(self, picturelist):
        self.move_down_until_nsame_element('【多媒体】图片测试库', 2)
        # self.driver.find_element_by_name('【多媒体】图片测试库').click()进入图片媒体库，没有任何元素被选中
        self.driver.press_keycode(23)  # 进入图片媒体库，选中第一个元素
        while True:
            for index, pic_format in enumerate(picturelist):
                self.move_down_until_nsame_element(pic_format, 2)
                num = pic_format.rsplit('-')[1]
                self.driver.press_keycode(23)
                if self.driver.page_source.find('未发现可支持的视频、音乐、图片文件') != -1:
                    self.driver.press_keycode(4)  # 返回到图片分类列表
                    continue
                else:
                    for i in range(int(num)):
                        self.driver.implicitly_wait(3)
                        self.driver.press_keycode(22)
                    self.driver.press_keycode(4)  # 退出图片浏览
                    time.sleep(2)
                    self.driver.press_keycode(4)  # 返回到图片分类列表
                print('进去出来了')
                print(index, pic_format)
            print(picturelist)

if __name__ == '__main__':
    print(Phote.mro())
    p = Phote()
    p.setUp()
    picturelist = ['bmp-230', 'GIF-41', 'JPE-6', 'JPEG-2', 'jpg-475', 'PCX-4', 'png-57', 'psd-1', 'pxr-1', 'raw-1',
                   'tga-1', 'tif-17', 'tiff-16', 'WBMP-2']
    p.test_openimage(picturelist)

