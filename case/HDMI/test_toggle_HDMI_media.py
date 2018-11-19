from appo.common import logger
from appo.case.basecase import BaseCase
import unittest
import time


log = logger.model_logger('test_picture')
class Toggle_HDMI_Media(unittest.TestCase,BaseCase):

    def setUp(self):
        caps = self.package_activity_main('zb_home') 
        self.startUp(caps)

    def tearDown(self):
        self.endDown()

    def into_hdmi(self):
        self.driver.find_element_by_xpath("//android.widget.RelativeLayout[@resource-id='xmlauncher.appo.com.xmlauncher4:id/more']/android.widget.ImageView[1]").click()

    # // android.widget.RelativeLayout[ @ resource - id = 'xmlauncher.appo.com.xmlauncher4:id/more'] /
    # android.widget.ImageView[1]
    # // android.widget.RelativeLayout[ @ resource - id = 'xmlauncher.appo.com.xmlauncher4:id/more']
    #进入音频播放音乐
    def zb_common_hdmi_case(self):
        self.driver.find_element_by_xpath("//android.widget.RelativeLayout[@resource-id='xmlauncher.appo.com.xmlauncher4:id/more']").click()
        # self.driver.implicitly_wait(3)

    def test_toggle_hdmi(self,type):
        self.into_hdmi()
        print("######################################################################")
        # 通道HDMI1
        if type == 'press_first_for' or type == 'not_press': #第一次进去时候，需要先定位到更多，然后keypress=23
            self.driver.press_keycode(23)
        self.driver.find_element_by_xpath("//*[@resource-id='appo.com.tvsource:id/sginal_hmdi1_icon']").click()
        self.driver.press_keycode(23)
        time.sleep(5)
        self.driver.press_keycode(3)
        time.sleep(2)

        self.into_hdmi()
        # 通道HDMI2
        self.driver.find_element_by_xpath("//*[@resource-id='appo.com.tvsource:id/sginal_hmdi2_icon']").click()
        self.driver.press_keycode(23)
        time.sleep(5)
        self.driver.press_keycode(3)
        time.sleep(2)

        self.into_hdmi()
        # 通道HDMI3
        self.driver.find_element_by_xpath(
            "//android.widget.ImageView[@resource-id='appo.com.tvsource:id/sginal_hmdi3_icon']").click()
        self.driver.press_keycode(23)
        time.sleep(5)
        self.driver.press_keycode(3)
        time.sleep(2)

        self.into_hdmi()
        # 通道AV
        self.driver.find_element_by_xpath(
            "//android.widget.ImageView[@resource-id='appo.com.tvsource:id/sginal_av_icon']").click()
        self.driver.press_keycode(23)
        time.sleep(5)
        self.driver.press_keycode(3)
        time.sleep(2)


if __name__ == '__main__':
    t = Toggle_HDMI_Media()
    t.setUp()
    t.test_toggle_hdmi('not_press')




