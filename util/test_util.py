

class Foo(object):
    def get_cls_name( self ):
        return self.__class__.__name__


class Bar(Foo):
    def __init__( self ):
        name = self.get_cls_name()
        print(name)
    pass


b = Bar()