import logging
import os

import logging.config as logging_config

from logging import Formatter

default_logger = 'boilerplate'
backupCount = 10

class PathTruncatingFormatter(Formatter):
    def format(self, record):
        if hasattr(record,'pathname'):
            # truncate the pathname
            # pathname_list = record.pathname.replace('/','.').replace("\\",'.').replace('..','.').split('.')
            pathname_list = record.pathname.split(os.sep)
            new_pathname = ".."+".".join(pathname_list[-4:])
            record.pathname = new_pathname
        # record.pathname = 'test'
        with open('test','w',encoding='utf-8') as f:
            f.write(str(dir(record)))
        return super(PathTruncatingFormatter, self).format(record)

_config = {
    'version': 1,
    'formatters':{
        'simple':{
            'class':'utils.log.PathTruncatingFormatter',
            'format':'%(levelname)s %(asctime)s %(pathname)40s %(lineno)s \t %(message)10s',
        }
    },
    'handlers':{
        'fileHandler':{
            'formatter':'simple',
            'class':'logging.handlers.TimedRotatingFileHandler',
            # 'class':'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename':os.path.join('log','boilerplate.log'),
            'backupCount':backupCount,
            # 'when':'D',
            # 'interval':1,
            'when':'midnight',
            'delay':True,
        },
        'streamHandler':{
            'formatter':'simple',
            'class':'logging.StreamHandler',
        },
    },
    'loggers':{
        default_logger:{
            'level': 'DEBUG',
            'handlers':['fileHandler','streamHandler'],
        }
    }
}


def init_logging(level=logging.DEBUG):

    # FORMAT = '%(asctime)s %(levelname)s | %(message)s | %(filename)s %(lineno)s'
    # logging.basicConfig(format=FORMAT,level=level)

    logging_config.dictConfig(_config)

    pass
