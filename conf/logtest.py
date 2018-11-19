import logging
import logging.config
import yaml


with open('logging.yml','r') as f_conf:
    try:
        dict_conf = yaml.load(f_conf)
    except yaml.YAMLError as exc:
        print(exc)
    finally:
        f_conf.close()
logging.config.dictConfig(dict_conf)

# time = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
# print(time)
# # 修改log文件名，以时间定义文件名字
# dict_conf['handlers']['file']['filename']='%s.txt'%(time)
# print(dict_conf)
# logging.config.dictConfig(dict_conf)

# logging.FileHandler()
# log输出到控制台
consolelogger = logging.getLogger('infoLog')
consolelogger.debug('debug message')
consolelogger.info('info message')
consolelogger.warning('warn message')
consolelogger.error('error message')
consolelogger.critical('critical message')
consolelogger.exception('这是一个异常log')

# log输出到文件
filelogger = logging.getLogger('logtest.py')
filelogger.debug('debug message')
filelogger.info('info message')
filelogger.warning('warn message')
filelogger.error('error message')
filelogger.critical('critical message')


