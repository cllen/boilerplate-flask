import logging


def init_logging(level=logging.DEBUG):

    FORMAT = '%(asctime)s %(levelname)s | %(message)s | %(filename)s %(lineno)s'
    logging.basicConfig(format=FORMAT,level=level)
    
