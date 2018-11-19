from appo.common import logger
from appo.case.media.ZB.test_video import Video


log = logger.model_logger('zb_test_video_press')
class VideoPress(Video):

    #进入音频播放音乐
    def test_scanAudio_press(self,num):
        i = 0
        while True: #循环播放音频
            log.info('循环播放第%s次'%i)
            self.test_scanVideo(num)
            i = i+1

if __name__ == '__main__':
    p = VideoPress()
    print(VideoPress.mro())
    p.setUp()
    audiolist = ['ASF视频文件','AVI视频文件','DAT视频文件','FLV视频文件','MKV']
    p.test_scanAudio_press(len(audiolist))

