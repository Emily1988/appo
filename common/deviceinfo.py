import re
import subprocess
from appo.common import connect
from appo.common import logger


log = logger.model_logger('deviceinfo')
"""获取设备信息"""
def getandroidversion():
    """正则获取安卓版本号"""
    try:
        # 获取系统设备系统信息
        sysinfo = subprocess.check_output('adb shell cat /system/build.prop').decode('utf-8')
        # 获取安卓版本号
        androidversion = re.findall('version.release=(\d\.\d.\d)*', sysinfo, re.S)[0]
        _version = androidversion
        log.info('安卓版本androidversion=%s'%_version)
        return _version
    except Exception as e:
        log.exception(e)

def getdevicename():
    """通过正则获取设备名"""
    shell_getdevice_cmd = 'adb devices -l'
    try:
        deviceinfo = subprocess.check_output(shell_getdevice_cmd).decode('utf-8')
        if deviceinfo.find('offline') != -1:
            log.error('设备offline,断开设备重新连接')
            exit()
        else:
            devicename = re.findall(r'device product:(.*)\smodel', deviceinfo, re.S)[0]
            _name = devicename
            log.info('得到设备名称devicename=%s'%_name)
            return _name
    except AttributeError as exc:
        log.exception(exc)

if __name__ == '__main__':
    ip = '192.168.125.136'
    connect.connect(ip)
    getandroidversion()
    getdevicename()
