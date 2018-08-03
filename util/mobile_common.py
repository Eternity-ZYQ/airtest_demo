
from airtest.core.api import *  #支持基于图像识别的Airtest框架，适用于所有Android和Windows游戏
from airtest.core.android.adb import ADB
from base.read_files import * #读取各种文件的处理
from airtest.core.helper import *

auto_setup(__file__)
_adb =ADB()
Guide=True

class MobileCommon(object):

    def __init__(self,device_num=1):
        self.device_num =device_num

    def init_server(self):
        "初始化服务，在connect_device()拿不到dev时使用"
        return init_device(platform="Android")

    def if_platform(self):#需要测试
        """
        返回device的平台信息
        :return: 平台信息
        """
        plat =device_platform()
        return plat

    def install_app(self):
        "install_app的封装"
        if install(apk_path()): #安装base/read_files目录下
            return True
        else:
            self.uninstall_app()
            self.install_app()
        #删除apk然后在安装1次

    def uninstall_app(self):
        uninstall()

    def get_index_page(self):
        """
        home的封装
        :return: None
        """
        home()


    def open_app(self,packagename):
        """
        开始执行
        :param packagename:用adb方式拿到当前运行的包名
        :return:
        """
        start_app(packagename)

    def get_touch(self):
        """
        默认是0.05秒检查一次
        :return:
        """
        touch()


    def connect_adb_multit(self,phone_id):  #phone_id要写成自然拿
        """
        (多手机)adb请求链接
        :param phone_id: str
        :return:
        """
        self.init_server()
        phone = '127.0.0.1:5037/{}'.format(str(phone_id))
        #_adb.devices()是返回当前设备
        if list(_adb.devices())>1: #判断机器数量 这里需要调下。  #后续打算改成if self.device_num >1:
            _adb.cmd("connect {}".format(phone), device=False)
            dev =connect_device("Android://127.0.0.1:5037/{}?cap_method=javacap&touch_method=adb".format(phone))
            return dev
        else:
            self.init_server() #初始化
            self.connect_adb_multit(phone_id) #重来一次


    def connect_adb_once(self):
        """
        (单个手机)adb
        :return:
        """
        self.init_server()
        if self.device_num ==1:
            dev = connect_device("Android:///")
            return dev
        else:
            self.init_server() #初始化
            self.connect_adb_once()

    def game_Poco_once(self,platform ="Unity"):
        """
        (单个手机)Poco的初始化
        :param platform:对应平台
        :return:
        """
        addr = ('', 5001)
        if platform =="Unity":
            from poco.drivers.unity3d import UnityPoco
            poco = UnityPoco(addr, device=self.connect_adb_once())
        elif platform =="UnityWins":
            from poco.drivers.unity3d.device import UnityEditorWindow as UnityWindow  #<----不知道是否还有效
            poco = UnityWindow()
            return -1 #暂时屏蔽
        elif platform =="Cocos":
            from poco.drivers.cocosjs import CocosJsPoco
            poco = CocosJsPoco(addr, device=self.connect_adb_once())
        else:
            from poco.drivers.android.uiautomation import AndroidUiautomationPoco as AndroidPoco  #游戏sdk
            poco = AndroidPoco(addr, device=self.connect_adb_once())
        return poco


    def game_Poco_multit(self,phone_id,platform ="Unity"):
        """
        (多个手机)不同版本Poco的初始化 poco是要接入sdk的，可以展开UImap
        :param phone_id:devices_list
        :param platform:对应平台
        :return:
        """
        addr = ('', 5001)
        if platform =="Unity":
            from poco.drivers.unity3d import UnityPoco
            poco = UnityPoco(addr, device=self.connect_adb_multit(phone_id))
        elif platform =="UnityWins":
            from poco.drivers.unity3d.device import UnityEditorWindow as UnityWindow  #<----不知道是否还有效
            poco = UnityWindow()
            return -1
        elif platform =="Cocos":
            from poco.drivers.cocosjs import CocosJsPoco
            poco = CocosJsPoco(addr, device=self.connect_adb_multit(phone_id))
        else:
            from poco.drivers.android.uiautomation import AndroidUiautomationPoco as AndroidPoco   #游戏sdk
            poco = AndroidPoco(addr, device=self.connect_adb_multit(phone_id))
        return poco



    def Android_Poco(self,msg):
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco as AndroidPoco
        poco =AndroidPoco()
        try:
            dr =poco().child()
            dr.click()
            snapshot(msg)
        except:
            snapshot(msg)


    def _read_Pcoo_sence(self):
        "读取配置txt文件的场景step"
        global Guide
        if self.device_num ==1:
            poco =self.game_Poco_once()
            while(Guide): #ps:后面在给poco()封装1个msg=None的注释
                data =open_with_txt() #调用base/read_files 读取text的
                if not data:
                    Guide =False #修改条件
                    break
                elif data:#read over is false
                    obj =poco(data)
                    return obj


    def if_Guide(self): #加入多线程手机和单个手机区分
        """

        :param file:
        :param phone_id:
        :return:
        """
        import time
        if self.device_num ==1: #1台手机
            poco =self.game_Poco_once()
        else:
            poco =self.game_Poco_multit(phone_id="",platform ="Unity")
        scr_main =True
        while(scr_main):
            try:
                #按顺序往下走
                gamemain =poco.wait_for_any([open_json(0),open_json(1),open_json(2)], timeout=120) #这里没有抽象，用了数据驱动
                #这里默认是gamemain找到的。如果找不到需要在啦一次uimap 这里预留函数1个
                #try_poco()
            except Exception as error:
                global scr_main
                scr_main =False
                break
            if gamemain is open_json(0):  #一层一层判断
                time.sleep(1.5) #还要封装1个wait()
                #这里加1个logger
            elif gamemain is open_json(1):
                time.sleep(1.5)
            elif gamemain is open_json(2):
                time.sleep(1.5)
            else:
                raise gamemain




