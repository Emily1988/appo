from appo.case.basecase import BaseCase
import unittest
from appo.common import logger
from PIL import Image,ImageChops
from appo.common.tools import ShellCmd
import math
from functools import reduce
import operator
import time


log = logger.model_logger('zb_test_picture')
class Phote(unittest.TestCase, BaseCase):

    result = False
    def setUp(self):
        caps = self.package_activity_main('zb_fileexplorer') #zb_fileexplorer
        self.startUp(caps)
        self.zb_common_casetype_media()

    def tearDown(self):
        self.endDown()

    def restore_selectbox(self):
        self.driver.press_keycode(21)
        self.driver.press_keycode(21)
        self.driver.press_keycode(21)
        self.driver.press_keycode(21)
        self.driver.press_keycode(21)
        self.driver.press_keycode(19)

    def loggle_imagle(self,picturefile):
        print(picturefile)
        subfilecount = picturefile.split('-')[1]
        xpath = "//*[@text='{}']".format(picturefile)
        print(xpath)
        # self.driver.find_element_by_xpath(xpath)
        # self.driver.find_element_by_xpath("//*[@text='bmp-230']").click()
        # self.driver.find_element_by_xpath("//android.widget.TextView[@text='bmp-230']").click()

        self.driver.find_element_by_android_uiautomator('text(\"'+picturefile+'\")').click()      # 点击进入图片列表
        self.driver.press_keycode(23)
        #复原选择框,保证图片是从第一张开始播放
        self.restore_selectbox()

        self.driver.press_keycode(23)  # 点击第一张图片开始轮播
        if self.element_contain_pagesource('始终'):
            self.driver.find_element_by_xpath("//*[@text='始终']").click()

        for i in range(int(subfilecount)):
            orginimage = 'D:\\pycode\\appo\\case\\media\\picture\\foo.png'
            targetimage = 'D:\\pycode\\appo\\case\\media\\picture\\target.png'
            try:
                self.simple_screenshots(orginimage)
                self.result = ImageHandle().image_is_same(orginimage, targetimage)
                # subTest()只能在test模式下运行，正常模式下么有subtest()
                # with self.subTest(self.result):
                #     self.assertTrue(self.result)
            finally:
                self.driver.press_keycode(22)
                time.sleep(1)
        self.driver.press_keycode(4)

        time.sleep(2)
        self.driver.press_keycode(4)

    #滚动图片验证图片是否能打开
    def test_openimage(self,picturelist):
        print(self.driver)
        # // *[ @ text = 'SONY_16X']
        # self.move_down_until_element_appear('【多媒体】图片测试库')
        self.driver.find_element_by_xpath("//*[text='Android']").click()
        self.driver.find_element_by_xpath("//*[text='Android']").click()

        for picture_file in picturelist:
            self.move_down_until_element_appear(picture_file)
            self.loggle_imagle(picture_file)

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
    picturelist = ['bmp-230', 'GIF-41', 'JPE-6', 'JPEG-2', 'jpg-475', 'PCX-4', 'png-57', 'psd-1', 'pxr-1', 'raw-1',
                   'tga-1', 'tif-17', 'tiff-16', 'WBMP-2']
    p.test_openimage(picturelist)

