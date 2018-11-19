import os
import subprocess
import appo.common.global_var as gl
import appo.common.logger as log

logger = log.model_logger('connect')

def checkandroidevn(self = None):
    """检查Android adb环境"""
    if 'ANDROID_HOME' in os.environ:
        command = os.path.join(
            os.environ['ANDROID_HOME'],
            'platform-tools',
            'adb')
        gl.android_home = True
        logger.info('android adb 环境存在')
    else:
        logger.error('Adb not found in $ANDROID_HOME path: %s.' % os.environ['ANDROID_HOME'])
        gl.android_home = False
        raise EnvironmentError(
            'Adb not found in $ANDROID_HOME path: %s.' %
            os.environ['ANDROID_HOME'])


def checkdevcieconnect():
    """检查设备是否连接"""

    cmd = 'adb devices'
    try:
        """获取设备列表信息，并用"\r\n"拆分"""
        deviceinfo = subprocess.check_output(cmd, stderr=subprocess.PIPE, cwd=os.getcwd(),
                                             shell=True,
                                             startupinfo=gl.globalStartupInfo)
        devicename = deviceinfo.decode('utf-8').split('\r\n')
        """如果没有链接设备或者设备读取失败，第二个元素为空"""
        if devicename[1] == '':
            gl.connect_state = False
        else:
            gl.connect_state = True
        # logger.info('设备连接状态 is: %s' % gl.connect_state)
    except Exception as exc:
        logger.exception(exc)
        gl.connect_state = False
    logger.info('设备连接状态 is: %s' % gl.connect_state)

def check_devices_connect_state():
    cmd = 'adb get-state'
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=os.getcwd(),
                             shell=True,
                             startupinfo=gl.globalStartupInfo)
        p.communicate()
        info = p._stderr_buff[0].decode('utf-8')
        index = info.find('error: no devices/emulators found')
        if index is not -1:
            logger.info('%s',info)
        else:
            logger.info('检测到已有设备连接')
    except Exception as exc:
        logger.exception(exc)

def runcmd(cmd, msg):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=os.getcwd(),
                             shell=True,
                             startupinfo=gl.globalStartupInfo)
        p.communicate()
        logger .info('p.communicate 执行状态码：%s' %p.returncode)
        if msg == '断开设备':
            if p.returncode == 0 :
                logger.info('adb connect命令执行成功,设备已经断开连接')
            else:
                logger.info('设备已经是断开的啦~,连接状态 is %s,'%gl.connect_state)
        else:
            # 确保连接成功，再次检查连接状态
            checkdevcieconnect()
            if p.returncode == 0 and gl.connect_state:
                logger.info('adb connect命令执行成功,设备成功连接')
            else:
                logger.error('adb connect命令执行失败,设备连接失败,请检查网络频段')
    except subprocess.CalledProcessError as e:
        logger.exception(e)

def connect(ip):
    """连接设备"""
    cmd = 'adb connect {}'.format(ip)
    checkandroidevn()
    if gl.android_home:
        logger.info('android adb 环境准备 is: %s' % gl.android_home)
        try:
            checkdevcieconnect()
            if gl.connect_state == False:
                try:
                     runcmd(cmd, '连接设备')
                     # os.system(r"d: & cd d:\adbkit & adb connect 192.168.0.112") #连接不成功的，
                except Exception as e:
                     logger.exception(e.args[0])
                     print('设备连接过程中遇到异常:')
        except Exception as exc:
            print(exc)

def disconnect(ip):
    """断开设备"""
    cmd = 'adb disconnect {}'.format(ip)
    try:
        runcmd(cmd, '断开设备')
    except Exception as e:
        logger.exception(e)
        print('设备断开时遇到异常')

if __name__ == '__main__':
    ip = '192.168.125.136'
    connect(ip)
    # disconnect(ip)
    # cmd =  cmd = 'netstat -ano |findstr "4723"'
    # msg = '断开设备'
    # runcmd(cmd,msg)
    check_devices_connect_state()