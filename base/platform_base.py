import platform,sys,os,re
import subprocess

def system_plat():
    "判断是wins还是ios,用于命令行差异"
    plat =platform.system()
    if plat == "Windows":
        pass
    elif plat == 'Linux':
        pass
    else:
        pass
    return plat

def win_linux_platform():
    "判断平台的处理"
    if sys.platform.startswith('linux'):
        pass
    elif sys.platform.startswith('win'):
        pass
    else:#sys.platform.startswith('mac')
        pass
    return sys.platform

def check_task(name):
    """
    搜索任务列表
    :param name: 需要搜索的进程名称
    :return:
    """
    if win_linux_platform() =="Windows":
        return subprocess.check_output('tasklist | findstr %s'%name, shell=True)
    elif win_linux_platform() =="linux":
        command = 'ps aux |grep %s' % name
        return subprocess.check_output(command, shell=True)
    else:
        command = 'ps aux |grep %s' % name
        return subprocess.check_output(command, shell=True)


def color_print(s, color='green'):
    """
    颜色输入
    :param s:
    :param color:
    :return:
    """
    ct = {
        'green': '\033[92m',
        'red': '\033[91m',
        'none': '\033[0m'
    }
    return ''.join([ct[color], s, ct['none']])


def show_packages(path):
    """
    拿到path目录下所有包含__init__.py的文件夹
    use:path = r'E:\sendHttp_client\thirdp'
    :return:
    """
    packages = []

    for root, _, files in os.walk(path):
        if '__init__.py' in files:
            if win_linux_platform() =="Linux":
                packages.append(
                    re.sub('^[^A-z0-9_]', '', root.replace('/', '\\'))
                )
            if win_linux_platform() =="Windows":
                packages.append(
                    re.sub('^[^A-z0-9_]', '', root.replace('\\', '\\'))
                )
            else:
                packages.append(
                    re.sub('^[^A-z0-9_]', '', root.replace('\\', '\\'))
                )
    return packages


import psutil

def find_process_pass(proname):
    """
    判断进程是否存在，如果存在则维持，如果不存在重新启动
    :param proname:
    :return:
    """
    pid_list = psutil.pids()
    for pid in pid_list:
        if psutil.Process(pid).name() == proname:
            return pid
    else:
        pass

print(find_process_pass('notepad++.exe'))




import threading
class _Singleton(object):
    """
    （多线程）单例类的 装饰器
    """
    _LOCK = threading.Lock()

    def __init__(self, cls):
        self.__instance = None
        self.__cls = cls

    def __call__(self, *args, **kwargs): #让实例化的对象直接返回结果
        self._LOCK.acquire()
        if self.__instance is None:
            self.__instance = self.__cls(*args, **kwargs)
        self._LOCK.release()
        return self.__instance