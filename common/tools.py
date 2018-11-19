import subprocess
import psutil
import os
from appo.common import global_var as gl
from appo.common import logger
import time

log = logger.model_logger('tools')

'''
    获取进程、线程id类
'''
class MyPsutil:

    def processinfo(self,processName):
        pids = psutil.pids()
        for pid in pids:
            # print(pid)
            p = psutil.Process(pid)
            print(p.name)
            if p.name() == processName:
                print(pid)
                return True  # 如果找到该进程则打印它的PID，返回true
        return False  # 没有找到该进程，返回false

    def getpid(self,port):
        cmd = 'netstat -ano |findstr "{}"'.format(port)
        print(cmd)
        try:
            sysinfo = subprocess.check_output(cmd, stderr=subprocess.PIPE,
                                              cwd=os.getcwd(),
                                              shell=True,
                                              startupinfo=gl.globalStartupInfo)
            index = sysinfo.decode('utf-8').find('LISTENING')
            if index != -1:
                begin = index + len('LISTENING') + 7
                end = begin + 5
                info = sysinfo[begin:end]
                if info.isdigit():
                    return info.strip().decode('utf-8')
                else:
                    log.error('【包含非数字字符】%s,转化之后为%s'%(info,int(info)))
                    return int(info)
            else:
                log.error('没有找到【LISTENING】字符串')
        except Exception as e: #port没有查到PID，才会到异常这里
            gl.appium_server_pid = False
            log.exception(e)
            log.info('没有找到%s对应的PID' % port)
            return None

    def check_exist_pid(self,port):
        cmd = 'netstat -ano |findstr "{}"'.format(port)
        print(cmd)
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, cwd=None,
                                 env=None,
                                 shell=True,
                                 startupinfo=gl.globalStartupInfo)
            p.communicate()
            log.info('p.communicate 执行状态码：%s' % p.returncode)
            # 存在PID p.returncode=0，不存在PID, p.returncode=1
            if p.returncode == 0:
                sysinfo = p._stdout_buff[0]
                index = sysinfo.decode('utf-8').find('LISTENING')
                if index != -1:
                    begin = index + len('LISTENING') + 7
                    end = begin + 5
                    info = sysinfo[begin:end]
                    if info.isdigit():
                        log.info('获取到appiun server port=%s的PID=%s'
                                 %(port,info.strip().decode('utf-8')))
                        gl.appium_server_pid = True
                        return info.strip().decode('utf-8')
                    else:
                        log.error('【包含非数字字符】%s,转化之后为%s' % (info, int(info)))
                        return int(info)
            else:
                log.info('没有找到%s端口的的PID ，执行状态码是%s,' %(port,p.returncode))
                gl.appium_server_pid = False
                return None
        except subprocess.CalledProcessError as e:
            log.exception(e)
            gl.appium_server_pid = False
            return None

'''
Appium Server类
'''
class AppiumServer:

    def __init__(self):
        self.port = gl.configFile['appium']['port1']
        psutil = MyPsutil()
        self.pid = psutil.check_exist_pid(self.port)
        if self.pid != None:
            gl.appium_server_pid = True
        else:
            gl.appium_server_pid = False

    def check_appium_state(self):
        return gl.appium_start_state

    def startAppium(self):
        if gl.appium_server_pid == False:
            cmd = 'start appium -a 127.0.0.1 -p {}'.format(self.port)
            try:
                o = os.system(cmd)
                if o == 0:
                    gl.appium_start_state = True
                    log.info('appium port=%s启动成功,启动状态is:%s' %(self.port,gl.appium_start_state ))
                else:
                    gl.appium_server_pid = False
            except Exception as exc:
                gl.appium_server_pid = False
                print(exc)
        else:
            log.info('appium已经启动了，PID = %s' % self.pid)

    def stopAppium(self):
        psutil = MyPsutil()
        pid = psutil.check_exist_pid(self.port)
        if pid != None:
            cmd = 'taskkill -f -pid {}'.format(pid)
            try:
                o = os.system(cmd)
                if o == 0:
                    return True
                else:
                    return False
            except Exception as exc:
                log.exception(exc)
        else:
            log.info('appium启动状态 is %s：'%gl.appium_start_state)

'''
adb连接设备后，执行shell命令
'''
class ShellCmd:
    def runcmd(self,cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=os.getcwd(),
                             shell=True,
                             startupinfo=gl.globalStartupInfo)
        p.communicate()
        return p

if __name__ == '__main__':
    appium = AppiumServer()
    appium.startAppium()
    print('**************************************************8')
    time.sleep(5)
    appium.stopAppium()


