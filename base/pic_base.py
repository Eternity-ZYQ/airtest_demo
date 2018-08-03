
import os

class Pic(object):

    def __init__(self):
        self.base_path = os.path.abspath(os.path.dirname(__file__))

    def pic_path(self):
        "截图路径"
        pic_path = self.base_path.replace("\\","/")+"/pic/"
        return pic_path

