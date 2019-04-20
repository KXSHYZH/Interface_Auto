import os
import datetime
import logging.handlers
from functools import wraps

path = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = os.path.join(path + r'\..\\', 'Log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

time_str = datetime.datetime.now().strftime('%Y-%m-%d')

LOG = logging.getLogger('mylogger')
LOG.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR + r'\..\Log\\' + time_str + '.log', when='midnight', interval=1,
                                                       backupCount=7, atTime=datetime.time(0, 0, 0, 0),
                                                       encoding='utf-8')
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler(LOG_DIR + r'\..\Log\error\\' + time_str + '.log', encoding='utf-8')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

LOG.addHandler(rf_handler)
LOG.addHandler(f_handler)


def logger(param, *args_l):
    """ function from logger meta """

    def wrap(function):
        """ logger wrapper """

        @wraps(function)
        def _wrap(*args, **kwargs):
            """ wrap tool """
            LOG.info("当前调用方法 {}".format(param))
            if args:
                num = 0
                for arg in args[1:]:
                    try:
                        LOG.info("'%s'参数信息：%s" % (str(args_l[num]), str(arg)))
                    except Exception as e:
                        LOG.info("参数信息：%s" % str(arg))
                    num += 1
            if kwargs:
                for key, value in kwargs.items():
                    LOG.info("'%s'参数信息：%s" % (str(key), str(value)))
            return function(*args, **kwargs)

        return _wrap

    return wrap
