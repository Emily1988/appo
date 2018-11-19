from appo.common import logger
from appo.case.media.ZB.test_audio import Audio


log = logger.model_logger('zb_test_audio_press')
class AudioPress(Audio):

    #进入音频播放音乐
    def test_scanAudio_press(self,num):
        i = 0
        while True: #循环播放音频
            log.info('循环播放第%s次'%i)
            self.test_scanAudio(num)
            self.driver.press_keycode(23)
            i = i+1

if __name__ == '__main__':
    p = AudioPress()
    print(AudioPress.mro())
    p.setUp()
    audiolist = ['APE-32', 'flac-19', 'm4a-11', 'mp1-2', 'mp2-20', 'MP3音频（带字幕）-7',
                 'MP3音频-63', 'OGG音频-19', 'WAV-27', 'WMA音频-19']
    p.test_scanAudio_press(len(audiolist))

