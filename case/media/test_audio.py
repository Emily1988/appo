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

    #此方法用于处理元素遮挡，通过键值显示所有元素,奇数行通过22向右移动，偶数行通过21,向左移动，5的整数行，通过20向下移动
    def handle_walk_smple(self,num):
        templist = []
        evenlist = []
        audiolist1 = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title')  # 获取到音频列表
        for audio in audiolist1:
            i = audiolist1.index(audio)
            if i in [0, 1, 2, 3, 4]:  # 奇数行
                if audio.text not in templist:
                    templist.append(audio.text)
            elif i in [5, 6, 7, 8, 9]:  # 偶数行
                if i == 5:
                    break
                if evenlist[i].text in templist:
                    break
                else:
                    templist.append(evenlist[i].text)
            else:
                print('排序出错')

        hander = Handle()
        hander.generate_list(num)
        hander.separate_odd_even()
        hander.find_evenlist_startIndex()
        print('handle_walk_smple %s' %hander.odd)
        print('handle_walk_smple %s' %hander.even)
        print('handle_walk_smple %s' %hander.even_start)
        try:
            for i in range(0, num):
                print(templist[i])
                count = templist[i].rsplit('-')[1]
                if i in hander.odd and (i + 1) % 5 != 0:  # 奇数行
                    self.driver.press_keycode(23)
                    self.handle_walk_for_noaudio(int(count))
                    print('right')
                    self.driver.press_keycode(22)
                if i in hander.even and (i + 1) % 5 != 0:  # 偶数行
                    self.driver.press_keycode(23)
                    self.handle_walk_for_noaudio(int(count))
                    print('left')
                    self.driver.press_keycode(21)
                if (i + 1) % 5 == 0:  # 换行
                    self.driver.press_keycode(23)
                    self.handle_walk_for_noaudio(int(count))
                    print('down')
                    self.driver.press_keycode(20)
                    audiolist1 = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title')  # 获取到音频列表
                    if i+1 in hander.even_start:
                        audiolist1.reverse()
                        for audio in audiolist1:
                            j = audiolist1.index(audio)
                            if audiolist1[j].text not in templist:
                                templist.append(audiolist1[j].text)
                            else:
                                break
                    else:
                        for audio in audiolist1:
                            j = audiolist1.index(audio)
                            if audiolist1[j].text not in templist:
                                templist.append(audiolist1[j].text)

                    print('音频格式%s'%templist)
            log.info('音频格式列表%s' %templist)
            time.sleep(1)
            self.driver.press_keycode(4)  # 返回到音频列表
            time.sleep(1)
        except Exception as e:
            print(e)

    #此方法用于处理元素遮挡，通过键值显示所有元素,奇数行通过22向右移动，偶数行通过21,向左移动，5的整数行，通过20向下移动
    #处理非音频的文件
    def handle_walk_for_noaudio(self,num):
        templist = []
        evenlist = []
        audiolist1 = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title')  # 获取到音频列表
        for audio in audiolist1:
            i = audiolist1.index(audio)
            if i in [0, 1, 2, 3, 4]:  # 奇数行
                if audio.text not in templist:
                    templist.append(audio.text)
            else:
                break

        hander = Handle()
        hander.generate_list(num)
        hander.separate_odd_even()
        hander.find_evenlist_startIndex()
        print('handle_walk_for_noaudio %s'%hander.odd)
        print('handle_walk_for_noaudio%s'%hander.even)
        print('handle_walk_for_noaudio%s'%hander.even_start)

        try:
            for i in range(0, num):
                print(templist[i])
                lrc = templist[i].rfind('.lrc')
                txt = templist[i].rfind('.txt')
                if i in hander.odd and (i + 1) % 5 != 0:  # 奇数行
                    if lrc == -1 and txt == -1:  # 如果是视频文件打开
                        self.driver.press_keycode(23)
                        self.goto_music_player()
                        # print('goto_music_player')
                    print('right')
                    self.driver.press_keycode(22)
                if (i + 1) % 5 == 0:  # 换行
                    if lrc == -1 and txt == -1:  # 如果是视频文件打开
                        self.driver.press_keycode(23)
                        self.goto_music_player()
                        # print('goto_music_player')

                    print('down')
                    self.driver.press_keycode(20)
                    audiolist1 = self.driver.find_elements_by_id('com.xming.xmexplorer:id/group_title')  # 获取到音频列表
                    if i+1 in hander.even_start:  #偶数行
                        print(i+1)
                        audiolist1.reverse()
                        for audio in audiolist1:
                            j = audiolist1.index(audio)
                            if audiolist1[j].text not in templist:
                                templist.append(audiolist1[j].text)
                            else:
                                break
                    else:
                        print(i+1)
                        for audio in audiolist1:
                            j = audiolist1.index(audio)
                            if audiolist1[j].text not in templist:
                                templist.append(audiolist1[j].text)

                    print('音频文件%s'%templist)
                if i in hander.even and (i + 1) % 5 != 0:  # 偶数行
                    if lrc == -1 and txt == -1:
                        # print('goto_music_player')
                        self.driver.press_keycode(23)
                        self.goto_music_player()
                    print('left')
                    self.driver.press_keycode(21)

            log.info('所播音频文件列表%s' %templist)
            self.driver.press_keycode(4)  # 返回到音频列表
            time.sleep(1)
        except Exception as e:
            print(e)

    #进入音频播放音乐
    def test_scanAudio(self,num):
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
                self.handle_walk_smple(num)   #13种格式的音频格式文件
            else:
                log.info('不是选中的第一个元素')
                # 做下面的操作让其必须在第一个位置
                self.driver.long_press_keycode(19)
                self.driver.long_press_keycode(21)
                self.driver.long_press_keycode(21)
                self.driver.long_press_keycode(21)
                self.handle_walk_smple(num)   #13种格式的音频格式文件
        except Exception as exc:
            log.info('程序异常，没有进入udisk0文件夹')



class Handle:
    num = 28
    odd = []   # 奇数行
    even = []  # 偶数行
    com = []
    even_start = [] #偶数行的起始位置

    def __init__(self):
        self.com = []
        self.odd = []
        self.even = []
        self.even_start = []

    #根据文件个数生成序列
    def generate_list(self,num):
        for i in range(0, num):
            self.com.append(i)

    #根据生成的序列，找出奇数行、偶数行
    def separate_odd_even(self):
        for i in range(0, 10):
            for j in range(0, 5):
                r = (10 * i) + j
                l = (10 * i) + j + 5
                if r in self.com:
                    self.odd.append(r)
                if l in self.com:
                    self.even.append(l)

        # 找到偶数行起始数据
    def find_evenlist_startIndex(self):
        for i in self.even:
            if i % 5 == 0:
                self.even_start.append(i)


if __name__ == '__main__':
    p = Audio()
    p.setUp()
    audiolist = ['WMA音频-25']
    # num = 1
    p.test_scanAudio(len(audiolist))  #n种音频格式
    # h = Handle()
    # h.generate_list(72)
    # h.separate_odd_even()
    # print(h.odd)
    # print(h.even)

