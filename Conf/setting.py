
"""
统一管理公共的库，不要添加相对路径的
"""

import os
class Setting(object):

    path =os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+os.sep