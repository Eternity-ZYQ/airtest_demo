
import json
_json_file ="../test_data/data.json"


class Read_Json(object):

    def __init__(self):
        self.data = self.read_data() #通过函数self.read_data()去绑定1个成员方法

    def read_data(self):

        with open(_json_file,"r") as fp:
            data = json.load(fp)
            return data

    def get_data(self,key):
        value = self.data.get(key)
        return value

    