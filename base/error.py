class BaseError(Exception):
    """异常的基类"""

    def __init__(self, message=""):
        self.message = message

    def __repr__(self):
        return repr(self.message)


class FileNotExistError(BaseError):
    """图像不存在"""
    pass


class TemplateInputError(BaseError):
    """分辨率输入不正确"""
    pass


class NoSIFTModuleError(BaseError):
    """分辨率输入不正确."""
    pass


class NoSiftMatchPointError(BaseError):
    """错误引发的0个输入图像中的SIFT点"""
    pass


class SiftResultCheckError(BaseError):
    """Exception raised for errors 0 sift points found in the input images."""
    pass


class HomographyError(BaseError):
    """In homography, find no mask, should kill points which is duplicate."""
    pass