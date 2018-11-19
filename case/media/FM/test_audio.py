from appo.case.basecase import BaseCase
import unittest
from appo.common import logger
import time
import random

'''
使用此文件时，需要修改test_scanAudio()中的
self.handle_walk_smple(num)   
num 代表音频格式的数目，例如有5个不同的音频格式文件夹，则num=5
'''
log = logger.model_logger('test_picture')
class Audio(unittest.TestCase,BaseCase):

    result = False
    def setUp(self):
        caps = self.package_activity_main('xm_home')
        self.startUp(caps)
        self.common_keypress_case_type1()

    def tearDown(self):
        self.endDown()

    '''
        op :代表用户操作，forward快进，reback快退
        num :随机执行的次数
        type1:随机快进->随机播放1~6s->随机快退   
        type2:随机数5：随机快进->随机暂停1~6s->随机快进   
        type3:随机数6：随机快退->随机播放1~6s->随机快进   
    '''
    def keyevent(self,driver,num,op):
        if op == 'forward':
            for n in (1,num):
                self.driver.long_press_keycode(22)
        elif op == 'reback':
            for n in (1,num):
                self.driver.long_press_keycode(21)
        elif op == 'type1':
            for n in (1,num):
                self.driver.long_press_keycode(22)
            for n in(1,num):
                time.sleep(num)
            for n in (1, num):
                self.driver.long_press_keycode(21)
        elif op == 'type2':
            for n in (1,num):
                self.driver.long_press_keycode(22)
            for n in(1,num):
                time.sleep(num)
            for n in (1, num):
                self.driver.long_press_keycode(22)
        elif op == 'type3':
            for n in (1,num):
                self.driver.long_press_keycode(21)
            for n in(1,num):
                time.sleep(num)
            for n in (1, num):
                self.driver.long_press_keycode(22)
        else:
            print('出错')

    '''
       进入到播放音乐界面
       播放20秒，快进，继续播放5秒，快退，暂停3s再播放接着退出音频播放，接着播放下一个音频
       随机数1：快进 key=22   forward
       随机数2：快退 key=21   reback
       随机数3：暂停 key=23
       随机数4：随机快进->随机播放1~6s->随机快退   type1
       随机数5：随机快进->随机暂停1~6s->随机快进   type2
       随机数6：随机快退->随机播放1~6s->随机快进   type3
    '''
    def goto_music_player(self):
        try:
            print('goto_music_player')
            time.sleep(5)
            p = random.randint(1, 6)
            print('随机数是%s' % p)
            if p == 1:
                self.driver.press_keycode(20)
                self.keyevent(self.driver, p, 'forward')
            elif p == 2:
                self.driver.press_keycode(20)
                self.keyevent(self.driver, p, 'reback')
            elif p == 3:
                self.driver.press_keycode(23)
                time.sleep(3)
                self.driver.press_keycode(23)
            elif p == 4:
                self.driver.press_keycode(20)
                self.keyevent(self.driver, p, 'type1')
            elif p == 5:
                self.driver.press_keycode(20)
                self.keyevent(self.driver, p, 'type2')
            else:
                self.driver.press_keycode(20)
                self.keyevent(self.driver, p, 'type3')
        finally:
            self.driver.press_keycode(4)  # 退出播放音乐
            time.sleep(1)

    #进入音频播放音乐
    def test_scanAudio(self,audiolist):
        xpath = "//android.widget.GridView[@resource-id='com.xming.xmexplorer:id/main_grid']/android.widget.LinearLayout[1]"
        res = self.driver.find_element_by_xpath(xpath).get_attribute('selected')
        try:
            if res:
                #进入音频测试
                self.driver.press_keycode(20)
                time.sleep(0.3)
                self.driver.press_keycode(22)
                time.sleep(0.3)
                self.driver.press_keycode(22)
                time.sleep(0.3)
                self.driver.press_keycode(22)
                time.sleep(0.3)
                self.driver.press_keycode(23)
            else:
                log.info('不是选中的第一个元素')
                # 做下面的操作让其必须在第一个位置
                self.driver.long_press_keycode(19)
                self.driver.long_press_keycode(21)
                self.driver.long_press_keycode(21)
                self.driver.long_press_keycode(21)
        except Exception as exc:
            log.info('程序异常，没有进入udisk0文件夹')

if __name__ == '__main__':
    p = Audio()
    p.setUp()
    audiolist = ['AAC音频-14', 'AC3-2', 'amr-5', 'APE-32', 'flac-19', 'm4a-11', 'mp1-2', 'mp2-20', 'MP3音频（带字幕）-7', 'MP3音频-63',
     'OGG音频-19', 'WAV-27', 'WMA音频-19']
    p.test_scanAudio(audiolist)


