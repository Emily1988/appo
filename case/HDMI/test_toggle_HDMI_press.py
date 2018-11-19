from appo.common import logger
from appo.case.HDMI import test_toggle_HDMI_media

log = logger.model_logger('test_toggle_HDMI_press')
class Toggle_HDMI_Press(test_toggle_HDMI_media.Toggle_HDMI_Media):

    # 进入音频播放音乐
    def test_toggle_hdmi_press(self):
        i = 0
        while True:  # 循环进入退出hdmi通道
            if i == 0:    #第一次进去时候，需要先定位到更多
                self.test_toggle_hdmi('press_first_for')
            else:
                self.test_toggle_hdmi('press')
            i = i+1

if __name__ == '__main__':
    t = Toggle_HDMI_Press()
    t.setUp()
    t.test_toggle_hdmi_press()



