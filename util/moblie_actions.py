import time
from poco.utils.track import MotionTrack as Track
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class MoblieActions(object):

    def two_finger_action(self,hold_time):
        """
        2根手指操作 warning:该函数需要在游戏内实验
        :return:
        """
        mt_a = Track(speed=0.3)
        mt_b = Track(speed=0.4)
        mt_a.start([0.5, 0.5]).move([0.2, 0.5]).hold(hold_time).move([0.5, 0.5])
        mt_b.start([0.5, 0.6]).move([0.2, 0.6]).move([0.5, 0.6]).hold(hold_time)
        poco = AndroidUiautomationPoco() #目前用原生api
        poco.apply_motion_tracks([mt_a, mt_b],accuracy=0.004)
        time.sleep(2)

    def three_finger_action(self,hold_time):
        """
        3根手指操作 warning:该函数需要在游戏内实验
        :return:
        """
        mt_a = Track(speed=0.3)
        mt_b = Track(speed=0.4)
        mt_c = Track(speed=0.35)
        mt_a.start([0.5, 0.5]).move([0.2, 0.5]).hold(hold_time).move([0.5, 0.5])
        mt_b.start([0.5, 0.6]).move([0.2, 0.6]).move([0.5, 0.6]).hold(hold_time)
        mt_c.start([0.5, 0.6]).move([0.2, 0.6]).move([0.5, 0.6]).hold(hold_time)
        poco = AndroidUiautomationPoco() #目前用原生api
        poco.apply_motion_tracks([mt_a, mt_b,mt_c],accuracy=0.006) #
        time.sleep(2)
