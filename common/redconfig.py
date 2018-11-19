import yaml
import appo.common.logger as log
import os


# config_file_path = 'D:/pycode/appo/conf/config.yml'
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
config_file_path = rootPath + '\\conf\\config.yml'

logger = log.model_logger('redconfig')
with open(config_file_path, mode='r',encoding='UTF-8') as f_conf:
    try:
        dict_conf = yaml.load(f_conf)
    except yaml.YAMLError as exc:
        logger.exception(exc)
    finally:
        f_conf.close()


def configfile():
    return dict_conf

# class Config:
#     """从配置文件得到配置基础数据"""
#     def __init__(self):
#         pass
#
#     def read_config_ip(self,config_file):
#         try:
#             with open(config_file, 'r') as f:
#                 arrayip = demjson.decode(f.read())
#             return arrayip['ip']
#         except Exception as exc:
#             logging
#
#
#     def read_config_package(self, config_file):
#         with open(config_file, 'r') as f:
#             packagedic = demjson.decode(f.read())
#         return packagedic['packages']


if __name__ == '__main__':
    print(configfile())
    print(configfile()['appium']['port1'])
    print(dict_conf['xm']['package']['setting'])
    print(dict_conf['xm']['activity']['common'])
