

import os
from time import sleep
import re

command0 ='adb shell ime list -s'
command1 ='adb shell settings get secure default_input_method'
command2 ='adb shell ime set com.android.inputmethod.latin/.LatinIME'
command3 ='adb shell ime set io.appium.android.ime/.UnicodeIME'


def list_IME():
    "列出系统现在所安装的所有输入法"
    os.system(command0)

def enable_LatinIME():
    "切换latin输入法为当前输入法"
    os.system(command2)

def enable_UnicodeIME():
    "#切换appium输入法为当前输入法"
    os.system(command3)



"adb封装的公共方法，原生的用法"


class AndroidDebugBridge(object): #缩短可以用as
    def calladb(self, command):
        "实现adb命令发射器,下面可以省略了adb和methods"
        cmd_res = " "
        cmd_text = "adb %s" % command
        res = os.popen(cmd_text, "r")
        while 1:
            line = res.readline()
            if not line: break
            cmd_res += line
            res.close()
        return cmd_res

    def get_PhoneMsg(self, cmdlog, deviceName):
        "获取手机信息 做报告使用"
        path = os.path.abspath(os.path.dirname(__file__))
        cmdlog = path + '\\' + cmdlog
        os.system('adb -s %s shell cat /system/build.prop > %s' % (deviceName, cmdlog))
        PhoneMsg = {}
        with open(cmdlog, "r") as fobj:
            lines = fobj.readlines()  # 一次性读多行
            for line in lines:
                line = line.split('=')  # 切割读出来的数据
                # print(line)
                if (line[0] == 'ro.build.version.release'):  # 得到系统
                    s = line[1]
                    s = s.strip('\n')
                    PhoneMsg["系统"] = s
                if (line[0] == 'ro.product.model'):  # 得到手机名字
                    s = line[1]
                    s = s.strip('\n')
                    PhoneMsg["名称"] = s
                if (line[0] == 'ro.product.brand'):  # 得到手机品牌
                    s = line[1]
                    s = s.strip('\n')
                    PhoneMsg["品牌"] = s

        if os.path.exists(cmdlog):  # 最后移除文件
            os.remove(cmdlog)
        return PhoneMsg

    def get_men_total(seld, cmdlog):
        """
        获取当前手机内存,不是应用的
        :param cmdlog:
        :return:
        """
        os.system("adb shell cat /proc/meminfo >" + cmdlog)
        men_total = ""
        with open(cmdlog, "r") as fobj:
            lines = fobj.readlines()
            for line in lines:
                line = line.split('=')
                if line[0]:
                    men_total = re.findall(r"\d+", line[0])[0]
                    break
        if os.path.exists(cmdlog):
            os.remove(cmdlog)
        return str(cmdlog(int(men_total) / 1000)) + "M"


    def attached_devices(self):
        """
        检查设备是否存在
        :return:
        """
        res = self.calladb("devices") #adb封装的
        devices = res.partition('\n')[2].replace('\n', '').split('\tdevice')
        flag = [device for device in devices if len(device) > 2]  # 大于3行代表通过
        if flag:
            print("devices exists")
            return True
        else:
            self.calladb("kill-server")
            sleep(3)
            res = self.calladb("start-server")  # 二个一起用的
            return res or False

    def get_apppix(self):
        "手机分辨率"
        res = self.calladb("shell wm size")
        return res.readline().split("Physical size:")[1]

    def get_state(self):
        """
        设备的状态有 3 钟，device , offline , unknown
        device：设备正常连接
        offline：连接出现异常，设备无响应
        unknown：没有连接设备
        :return: None
        """
        res = self.calladb("get-state")
        res = res.strip(' \t\n\r')  # 去除空格
        return res or None  # 返回结果或者无

    def _push(self, local, remote):
        """
        电脑文件推到手机里面 local代表本地 remote手机
        :param local:
        :param remote:
        :return:
        """
        res = self.calladb("push {0} {1}".format(local, remote))
        return res

    def _pull(self, remote, local):
        """
        手机啦数据到电脑里面  local代表本地 remote手机
        :param remote:
        :param local:
        :return:
        """
        res = self.calladb("pull {0} {1}".format(remote, local))
        return res

    def _open_apk(self, package, Activity):
        """
        (原生)打开指定app am start -n ｛包(package)名｝/｛包名｝.{活动(activity)名称}
        :param package:包名
        :param Activity: Activity
        :return:
        """
        res = self.calladb("shell am start -n {0}/{1}".format(package, Activity))
        check = res.partition('\n')[2].replace('\n', '').split('\t ')
        if check[0].find("Error") >= 1:
            return False
        else:
            return True

    def get_app_pid(self, package):
        """
        根据package得到进程名"
        :param package:
        :return:
        """
        string = self.calladb("shell ps | grep " + package)
        if string == '':
            return "the process doesn't exist."
        res = string.split(" ")
        return res[4]

    def get_cpu(self,devices,package):
        """
        根据手机id+包名拿到cpu
        :param devices:devicesid
        :param package:包名
        :return:
        """
        res ="adb -s"+devices+" shell dumpsys cpuinfo|grep -w"+package+":"
        get_res =os.popen(res).readlines()
        for i in get_res:
            return float(i.split()[2].split("%")[0])

    def get_mem(self,devices,package):
        """
        根据手机id+包名拿到内存
        :param devices:
        :param package:
        :return:
        """
        res = "adb -s"+devices+" shell dumpsys meminfo {0}".format(package)
        total ="TOTAL"
        get_res =os.popen(res).readlines()
        for info in get_res:
            info_sp = info.strip().split()
            for i in range(len(info_sp)):
                if info_sp[i]==total:
                    return int(info_sp[i+1])

    def get_devices(self):
        '''
        获得所有的设备名称
        :return: list
        '''
        devices = []
        import subprocess
        bstr = subprocess.check_output('adb devices', shell=True)
        # 将二进制转换为字符串
        str = bstr.decode('ascii')
        str = str.strip()
        lst = str.splitlines()
        for s in lst:
            if '\tdevice' in s:
                i = s.find('device')
                name = s[:i]
                devices.append(name.strip())
        return devices

