from appo.common import logger
import time
from appo.case.media.ZB.test_photo import Phote

log = logger.model_logger('zb_test_picture_press')
class PhotoPress(Phote):

    def setUp(self):
        caps = self.package_activity_main('zb_fileexplorer')  # zb_fileexplorer
        self.startUp(caps)
        self.zb_common_casetype_media()

    def tearDown(self):
        self.endDown()

    #图片轮播
    def test_toggleimage_press(self,picturelist):
        self.driver.find_element_by_xpath("//android.widget.TextView[@text='【多媒体】图片测试库']").click()
        i = 0
        while True:
            log.info('循环播放第%s次'%i)
            self.move_up_until_element_appear(picturelist[0])  #复原，使可以显示出列表种的第一个元素
            for picturefile in picturelist:
                self.move_down_until_element_appear(picturefile)
                # self.loggle_imagle(picturefile)
                print(picturefile)
                subfilecount = picturefile.split('-')[1]
                xpath = "//*[@text='{}']".format(picturefile)
                print(xpath)
                self.driver.find_element_by_xpath(xpath).click()
                self.driver.press_keycode(23)
                # 复原选择框,保证图片是从第一张开始播放
                self.restore_selectbox()

                self.driver.press_keycode(23)  # 点击第一张图片开始轮播
                if self.element_contain_pagesource('始终'):
                    self.driver.find_element_by_xpath("//*[@text='始终']").click()
                if self.element_contain_pagesource('一律採用'):
                    self.driver.find_element_by_xpath("//*[@text='一律採用']").click()

                for i in range(int(subfilecount)):
                    self.driver.press_keycode(22)
                    time.sleep(1)
                self.driver.press_keycode(4)

                time.sleep(2)
                self.driver.press_keycode(4)
            print('#########################################')
            i = i+1


if __name__ == '__main__':
    p = PhotoPress()
    p.setUp()
    picturelist = ['bmp-230', 'GIF-41', 'JPE-6', 'JPEG-2', 'jpg-475', 'PCX-4', 'png-57', 'psd-1', 'pxr-1', 'raw-1',
                   'tga-1', 'tif-17', 'tiff-16', 'WBMP-2']
    p.test_toggleimage_press(picturelist)

