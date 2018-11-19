from appo.common import connect as con
from appo.common import logger
from appo.common import mydriver
from appo.common import tools
from appo.common import global_var as gl
import datetime
import shutil


log = logger.model_logger('basecase')
class BaseCase:
    '''
        测试用例基类
    '''
    appium = tools.AppiumServer()
    driver = None
    ip = gl.configFile['ip']['ip5']
    port = gl.configFile['appium']['port1']
    log.info('ip = %s ; appium_port = %s' %(ip,port))

    # 字典映射
    xm = gl.configFile['xm']
    fm = gl.configFile['fm']
    zb = gl.configFile['zb']
    def switcher(self,casetype):
        switch = {
            'xm_home': [self.xm['package']['xm_home'], self.xm['activity']['homeactivity']],  #XM主界面
            'fm_media': [self.fm['package']['fm_media'], self.fm['activity']['media_explorer']],#FM多媒体，文件浏览界面
            'fm_home':[self.fm['package']['fm_home'], self.fm['activity']['homeactivity']], #FM主界面
            'zb_home':[self.zb['package']['zb_home'],self.zb['activity']['homeactivity']],  #ZB Home界面
            'zb_fileexplorer':[self.zb['package']['zb_fileexplorer'],self.zb['activity']['main']] #ZB 多媒体，文件浏览界面
        }
        return switch.get(casetype,'nothing')

    def package_activity_main(self,type):
        try:
            return self.switcher(type)
        except ValueError as e:
            log.exception('参数%s错误',type)

    def startUp(self,caps):
        '''
        :param caps: driver构建内容
        :return:
        1. 启动appium
        2. 连接设备
        3. 远程连接，建立driver
        '''
        self.appium.startAppium()
        con.connect(self.ip) #连接设备
        self.driver = mydriver.driver(caps)

    def screenshots(self,filepath):
        try:
            if self.driver.save_screenshot(filepath):
                log.info('url = 截屏幕成功%s'%filepath)
            else:
                log.error('截图失败')
        except Exception as exc:
            log.exception(exc)  #driver=None/退出

    def simple_screenshots(self,filename):
        self.screenshots(filename)

    def standard_screenshots(self):
        current_t = datetime.datetime.now()
        str_time = current_t.strftime('%Y-%m-%d-%H_%M_%S_%f')
        filepath = 'D:/pycode/appo/result/screenshots/'+str_time+'.png'
        self.screenshots(filepath)

    # 删除保存的图片
    def delImage(self,path):
        shutil.rmtree(path)

    '''
        微投系列公共的测试用例：
        1.多媒体，外接设备入口-图片/音频/视频
        2.应用商店主页
        ...
    '''
    def common_case_type1(self):
        self.driver.implicitly_wait(3)
        # self.driver.find_element_by_name('文件浏览').click()
        self.driver.find_element_by_xpath('//android.widget.GridLayout/android.widget.RelativeLayout[2]').click()
        self.driver.press_keycode(23)
        # self.driver.find_element_by_name('udisk0').click()
        self.driver.find_element_by_xpath('//android.widget.LinearLayout/android.widget.RelativeLayout[2]').click()
        self.driver.find_element_by_id('com.xming.xmexplorer:id/file_layout').click()

    '''
            FM系列公共的测试用例：
            fm_common_case_type_media.多媒体，外接设备入口-图片/音频/视频
            fm_common_case_type_shop.应用商店主页
            ...
    '''
    def fm_common_case_type_media(self):
        self.driver.implicitly_wait(3)
        self.driver.press_keycode(21)
        self.driver.find_element_by_name('SONY_16X').click()
        self.driver.press_keycode(23)

    '''
            泽宝系列公共的测试用例：
            zb_common_casetype_media.多媒体，外接设备入口-图片/音频/视频
            zb_common_casetype_media.应用商店主页
            ...
    '''
    def zb_common_casetype_media(self):
        self.driver.implicitly_wait(3)
        # self.driver.find_element_by_name('SONY_16X').click()
        self.driver.find_element_by_xpath("//*[@text='SONY_16X']").click()
        # self.driver.find_element_by_xpath("//*[@text='大白菜U盘']").click()
        # self.driver.find_element_by_xpath('//android.widget.LinearLayout/=android.widget.RelativeLayout[2]').click()
        # self.driver.find_element_by_id('com.xming.xmexplorer:id/linear').click()
        self.driver.find_element_by_xpath("//android.widget.LinearLayout[@resource-id='com.xming.xmexplorer:id/file_layout']/android.widget.LinearLayout[1]").click()
        self.driver.press_keycode(19)

    #通过键值进入外接硬盘
    def common_keypress_case_type1(self):
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_xpath('//android.widget.GridLayout/android.widget.RelativeLayout[2]').click()
        self.driver.press_keycode(23)
        three_res = False
        for i in range(1,4):
            xpath = '//android.widget.LinearLayout/android.widget.RelativeLayout{}'.format([i])
            res = self.driver.find_element_by_xpath(xpath).get_attribute('focused')
            if res == 'true':
                three_res = True
                if i == 1:
                    self.driver.press_keycode(22)
                    self.driver.press_keycode(23)
                elif i == 2:
                    self.driver.press_keycode(23)
                    break
                else:
                    self.driver.press_keycode(21)
                    self.driver.press_keycode(23)
        if three_res == False:
            self.driver.press_keycode(22)
            self.driver.press_keycode(23)
            self.driver.press_keycode(23)
        else:
            self.driver.press_keycode(23)

    def common_case_type2(self):
        pass

    def element_contain_pagesource(self,ele):
        if self.driver.page_source.find(ele) != -1:
            return True
        else:
            return False

    #下翻直到元素出现
    def move_down_until_element_appear(self,ele):
        # eles = self.driver.find_element_by_name(ele)
        while True:
            print(self.driver.page_source.find(ele))
            if self.driver.page_source.find(ele) != -1:
                break
            else:
                self.driver.press_keycode(20)

    #上翻直到元素出现
    def move_up_until_element_appear(self,ele):
        # eles = self.driver.find_element_by_name(ele)
        while True:
            if self.driver.page_source.find(ele) != -1:
                break
            else:
                self.driver.press_keycode(19)

    # 向下移动直到某个元素消失不见
    def move_down_until_element_disappear(self, ele):
        eles = self.driver.find_element_by_name(ele)
        while True:
            if eles is None:
                break
            else:
                self.driver.press_keycode(20)

    def endDown(self):
        if self.driver is not None:
            self.driver.quit()
        con.disconnect(self.ip)

    def __del__(self):
        self.appium.stopAppium()
        print('__del__')
