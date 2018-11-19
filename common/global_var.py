import subprocess
from appo.common import redconfig

android_home = False   #android环境变量
connect_state = False  #设备连接状态
appium_start_state = False  #Appium启动状态
appium_server_pid = False  #appium进程pid是否存在


globalStartupInfo = subprocess.STARTUPINFO()
globalStartupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# read File
configFile = redconfig.configfile()
# Path
