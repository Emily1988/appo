from appo.common import logger
from appo.case.media.test_audio import Audio


log = logger.model_logger('test_picture')
class AudioPress(Audio):

    #进入音频播放音乐
    def test_scanAudio_press(self,num):
        self.test_scanAudio(num)
        while True: #循环播放音频
            self.handle_walk_smple(num)
            self.driver.press_keycode(23)


if __name__ == '__main__':
    p = AudioPress()
    print(AudioPress.mro())
    p.setUp()
    num = 1  # 1种格式的音频格式文件
    p.test_scanAudio_press(num)

