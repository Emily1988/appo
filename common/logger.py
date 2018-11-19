import logging.config
import yaml
import os


# filepath = 'D:/pycode/appo/conf/logging.yml'
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
filepath = rootPath + '\\conf\\logging.yml'

with open(filepath, 'r',encoding='utf-8') as f_conf:
    try:
        dict_conf = yaml.load(f_conf)
    except yaml.YAMLError as exc:
        print(exc)
    finally:
        f_conf.close()

def model_logger(model = None):
    logging.config.dictConfig(dict_conf)
    return logging.getLogger('%s.py'%model)

if __name__ == '__main__':
    logger =  model_logger('logger')
    logger.info('Nihao')