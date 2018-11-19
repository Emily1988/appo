from appo.common import logger
from appo.common import myremote
from appo.common import global_var as gl

log = logger.model_logger('mydriver')
port = gl.configFile['appium']['port1']
def driver(caps):
    selenium_grid_url = 'http://localhost:%s/wd/hub' %port
    log.info('appiumurl = %s' % selenium_grid_url)
    try:
        driver = myremote.remote(selenium_grid_url, caps)
        log.info('session=%s', driver)
        return driver
    except Exception as exc:
        log.exception(exc)