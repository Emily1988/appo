from appo.case.basecase import BaseCase
import unittest
from appo.common import logger
from PIL import Image,ImageChops
from appo.common.tools import ShellCmd
import math
from functools import reduce
import operator
import time


log = logger.model_logger('test_picture')
class Phote(unittest.TestCase, BaseCase):

    result = False
    def setUp(self):
        caps = self.package_activity_main('xm_home')
        self.startUp(caps)
        self.common_case_type1()

    def tearDown(self):
        self.endDown()

    #滚动图片验证图片是否能打开
    def test_openimage(self):
        self.driver.find_element_by_name('【多媒体】图片测试库').click()
        self.driver.press_keycode(23)
        # 2次20的key目的是显示所有的group_title
        self.driver.press_keycode(20)
        time.sleep(1)
        self.driver.press_keycode(20)
        filelist = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title') #图片文件夹
        for file in filelist:  # file子文件夹
            subfilecount = file.text.split('-')[1]
            print(file.text)
            file.click()  #点击进入图片列表
            imagelist = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title') #图片列表
            imagelist[0].click()  #点击第一张图片开始轮播
            orginimage = 'D:\\pycode\\appo\\case\\media\\picture\\foo.png'
            targetimage = 'D:\\pycode\\appo\\case\\media\\picture\\target.png'
            for i in range(int(subfilecount)):
                try:
                    self.simple_screenshots(orginimage)
                    self.result = ImageHandle().image_is_same(orginimage, targetimage)
                    #subTest()只能在test模式下运行，正常模式下么有subtest()
                    with self.subTest(self.result):
                        self.assertTrue(self.result)
                finally:
                    self.driver.press_keycode(22)
                    time.sleep(1)
            self.driver.press_keycode(4)
            time.sleep(2)
            self.driver.press_keycode(4)

class ImageHandle:
    # 屏幕截图,保存在设备中
    def screenshots(self):
        cmd = 'adb shell /system/bin/screencap -p /sdcard/screencap.png'
        cmd1 = 'shell "rm /sdcard/screencap.png'
        shell = ShellCmd()
        try:
            p = shell.runcmd(cmd)
            print(p._stdout_buff[0].decode('utf-8'))
            if p.returncode == 0:
                log.info('截屏保存在/sdcard/')
            else:
                log.info('截屏失败')
        except Exception as exc:
            log.exception(exc)
        finally:
            shell.runcmd(cmd1)  # 从设备移除图片

    # 对比两张图片，如果两张图片不同，保存一张对比后不同点的图片（diff.png）
    def compare_images(self, image1, image2, diff_save_location):
        image1 = Image.open(image1)
        image2 = Image.open(image2)
        print(image1.format, image1.size, image1.mode)
        print(image2.format, image2.size, image2.mode)
        try:
            diff = ImageChops.difference(image1, image2)
            if diff.getbbox() is None:
                log.info('%s和%s完全相同' % (image1, image2))
            else:
                diff.save(diff_save_location)
        except ValueError as e:
            text = ("表示图片大小和box对应的宽度不一致，参考API说明：Pastes another image into this image."
                    "The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, "
                    "right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted "
                    "image must match the size of the region.使用2纬的box避免上述问题")
            print("【{0}】{1}".format(e, text))

    def image_contrast(self, image1, image2):
        img1 = Image.open(image1)
        img2 = Image.open(image2)
        h1 = img1.histogram()
        h2 = img2.histogram()
        result = math.sqrt(reduce(operator.add,
                                  list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return result

    def image_is_same(self, image1, image2):
        result = self.image_contrast(image1, image2)
        if result == 0.0:
            log.info('%s和%s完全相同' % (image1, image2))  # 说明图片不支持，打不开
            return False
        else:
            log.info('%s和%s不相同，他们的差值为：%s' % (image1, image2, result))
            return True

if __name__ == '__main__':
    print(Phote.mro())
    p = Phote()
    p.setUp()
    p.test_openimage()

