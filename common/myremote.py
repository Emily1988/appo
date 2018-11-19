from appo.common import logger
from appo.common import deviceinfo
from appium import webdriver
from  appo.common import global_var as gl


log = logger.model_logger('remote')
def remote(url,packageandactivity):
    '''远程连接'''
    log.info('package=%s,activity=%s',packageandactivity[0],packageandactivity[1])
    desired_caps = {
        "platformName": "Android",
        "deviceName":deviceinfo.getdevicename(),
        "platformVersion":deviceinfo.getandroidversion(),
        "appPackage": packageandactivity[0],
        "appActivity": packageandactivity[1],
        'automationName': 'uiautomator2',  # 适配Android7之上版本
        'newCommandTimeout':200
    }

    # 连接到远程服务器进行自动化测试
    try:
        driver = webdriver.Remote(url, desired_caps)
        log.info(driver)
        return driver
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    ip = gl.configFile['ip']['ip1']
    print(ip)
    # ip = '192.168.0.154'
    # con.connect(ip)
    # appium.startAppium()
    # selenium_grid_url = 'http://localhost:4723/wd/hub'  # 本地启动selenium grid
    # d = remote(selenium_grid_url)
    # # try:
    # presskey(d)
    # d.quit()
