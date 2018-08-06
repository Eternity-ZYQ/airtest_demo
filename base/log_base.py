import logging,os,time
from airtest.utils.logger import get_logger

def init_logging():
    logger = logging.getLogger("airTestPro")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
        datefmt='%I:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


init_logging()


def create_logs(path=os.path.abspath(os.path.dirname(__file__)), name='LcmPost', timestamp=True):
        """
        创建日志
        :param path:
        :param name:
        :param timestamp:
        :return:
        """
        if timestamp:
            time_stamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())
            # 返回类似于'lcmTest_20160819073902.log'的文件名称
            name = '%s_%s.log' % (name, time_stamp)
        # 返回路径的格式拼接
        full_path = os.path.join(path + '/../logs/', name)
        if not os.path.exists(full_path):#exists判断full_path是否存在，如果没有就写入
            # 创建一个空的文件
            f = open(full_path, 'w')
            f.close()
        return full_path


def get_logging(name):
    ""
    logger = logging.getLogger(name)
    return logger