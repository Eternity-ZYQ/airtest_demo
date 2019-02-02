import sys,os,re,json,time
import subprocess
import threading
import psutil
from Conf.setting import Setting
from airtest.utils.logger import get_logger

class Base(object):

    _json_file =Setting.path+"test_files"+os.sep+"scene.json" #获取Json数据位置

    def __read_data(self,path=_json_file):
        """
        读取json数据
        :return:
        """
        with open(path,"r") as fp:
            data = json.load(fp)
            return data

    def get_data(self,key):
        """
        读取json数据后对应value数据
        :param key:
        :return:
        """
        if self.__read_data().__contains__(key):
            value = self.__read_data().get(key)
            return value
        else:
            print("检查字典里的key")

    def jude_platform(self):
        "判断平台的处理"
        return sys.platform

    def check_task(self,propname):
        """
        搜索任务列表
        :param propname: 需要搜索的进程名称
        :return:
        """
        if self.jude_platform() =="win32":
            return subprocess.check_output('tasklist | findstr %s'%propname, shell=True)
        elif self.jude_platform() =="linux":
            command = 'ps aux |grep %s' % propname
            return subprocess.check_output(command, shell=True)
        else:
            command = 'ps aux |grep %s' % propname
            return subprocess.check_output(command, shell=True)


    def color_print(self,content, color='green'):
        """
        把文字输出到cls上
        user:color_print("text")
        :param content:
        :param color:
        :return:
        """
        ct = {
            'green': '\033[92m',
            'red': '\033[91m',
            'none': '\033[0m'
        }
        return ''.join([ct[color], content, ct['none']])

    def get_pic_path(self):
        """
        获取截图路径
        :return:
        """
        pic_path = Setting.path+"pic"
        return pic_path

    def show_packages(self,path):
        """
        移除path目录下所有包含__init__.py的文件夹
        use:path = r'E:\sendHttp_client\thirdp'
        :return:
        """
        packages = []
        for root, _, files in os.walk(path):
            if '__init__.py' in files:
                if self.jude_platform() =="Linux":
                    packages.append(
                        re.sub('^[^A-z0-9_]', '', root.replace('/', '\\'))
                    )
                elif self.jude_platform() =="win32":
                    packages.append(
                        re.sub('^[^A-z0-9_]', '', root.replace('\\', '\\'))
                    )
                else:
                    packages.append(
                        re.sub('^[^A-z0-9_]', '', root.replace('\\', '\\'))
                    )
        return packages

    def find_process_pass(self,propname):
        """
        判断进程是否存在，如果存在返回pid  不存在就返回None =False
        user:
        obj =find_process_pass('notepad++.exe')
        if obj and instance(obj,int):
            ...
        :param propname:
        :return:
        """
        pid_list = psutil.pids()
        for pid in pid_list:
            if psutil.Process(pid).name() == propname:
                return pid

    def create_logs(self,name='LcmPost', timestamp=True):
        """
        创建log，返回日志的位置
        :param path:
        :param name:
        :param timestamp:
        :return:
        """
        path=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        log_dir =path +os.sep+"logs"+os.sep
        if timestamp:
            time_stamp = time.strftime("%Y-%m-%d-%H%M%S",time.gmtime())
            time_stamp =time_stamp.replace("-0","-") #去掉前面的0
            name = '%s-%s.log' % (name, time_stamp)# 返回类似于'lcmTest_20160819073902.log'的文件名称
        # 返回路径的格式拼接
        full_path = os.path.join(log_dir+os.sep, name)
        if not os.path.exists(log_dir):#exists判断full_path是否存在，如果没有就写入
            os.makedirs(log_dir)# 创建一个空文件夹
            f = open(full_path, 'w')
            f.close()
        return full_path

# base =Base()
# print(base.show_packages(r"E:\ste_test\airtest_project"))
# print(base.jude_platform())

class ApkBase(object):

    def apk_path(self,apkname):
        """
        读取单个apk路径
        user:apk_path("game_01")
        :return: str apk路径
        """
        apkpath =Setting.path+"test_tools"+os.sep+str(apkname)+".apk"
        return apkpath

    def excute(self,commond):
        """
        excute command数据
        :param command:
        :return:
        """
        subprocess.Popen(commond,stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,shell=True)

    def get_apk_name(self,apk_path):
        """
        apk_path的绝对路径
        :param apk_path:
        :return:
        """
        commond ="/root/android/android-sdk-linux/build-tools/20.0.0/aapt dump badging "\
        +apk_path +" | grep application-label:"
        (output,err)=self.excute(commond).communicate()
        if isinstance(output,str) and output !="":
            try:
                result =output[19:-2]
            except Exception as err:
                print(format(err))
            else:
                return result

    def __connect_dev(self):
        """
        拿到包体的
        :return:
        """
        p =os.popen('adb devices')
        outstr =p.read()
        connectdeviceid =re.findall(r'(\w+)\s+device\s',outstr) #这里代码需要试试
        return connectdeviceid

    def batch_install_apk(self):
        """
        批量安装
        :return:
        """
        connectdevice =self.__connect_dev()
        commands =[]
        for device in connectdevice:
            # cmd ="for %i in (*.apk) do adb install %i"  #adb可以这样执行
            # os.system(cmd)
            cmd = "adb -s %s install -r %s" % (device,self.apk_path(apkname=""))
            commands.append(cmd)
        return commands

    def threads_action(self):
        """
        多线程执行
        :return:
        """
        threads =[]
        threads_count =len(self.batch_install_apk())

        for i in range(threads_count):
            t =threading.Thread(target=self.excute, args=(self.batch_install_apk()[i],))
            threads.append(t)

        for i in range(threads_count):
            time.sleep(1)
            threads[i].start()

        for i in range(threads_count):
            threads[i].join()

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