from appo.common import logger
from appo.case.media.test_audio import Audio


log = logger.model_logger('test_picture')
class AudioPress(Audio):

    #进入音频播放音乐
    def test_scanAudio_press(self):
        self.test_scanAudio()
        while(1): #循环播放音频
            self.handle_walk_smple(1)  # 13种格式的音频格式文件
            self.driver.press_keycode(23)


if __name__ == '__main__':
    p = AudioPress()
    print(AudioPress.mro())
    p.setUp()
    p.test_scanAudio_press()

