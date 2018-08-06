#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
计算图形识别的函数
NumPy+PIL
OpenCV 提供的算法 进行改造

"""

try:
    import cv2
    import numpy as np
    from base.error import TemplateInputError,FileNotExistError
    from PIL import Image
except Exception as error:
    print(format(error))

def diff_img(src_img,find_img):
    """
    找出相似度高于0.8的图片
    :param src_img:目标截图
    :param find_img:要匹配的截图
    :return:
    """
    img_x =cv2.imread(src_img)
    img_y =cv2.imread(find_img)
    res = cv2.matchTemplate(img_x, img_y, cv2.TM_CCOEFF_NORMED)
    diff =np.where(res >=0.8)
    for point in zip(*diff[::-1]):
        return point


def _img_read_firsthand(img_path,method=0):
    "读取图片 0是彩色图像去掉法线通道"
    if img_path is not None:
        img =cv2.imread(img_path,method)
    else:
        raise FileNotExistError("error:找不到图片")
    return img

def img_show_waitKey(img_path):
    """
    展示图片，点击enter结束展示
    :param img_path:
    :return:
    """
    img =cv2.imread(img_path)
    while 1:
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('enter'):#64位系统
            print("img_show_waitKey is pass")
            break

def generate_result(middle_point, pypts, confi):
    """Format the result: 定义图像识别结果格式."""
    ret = dict(result=middle_point,
               rectangle=pypts,
               confidence=confi)
    return ret

def _image_encode(img_path,img_format):
    """
    (暂时不直接使用)对图片进行格式解码，解码methods根据图片格式来
    :param img_path: 图片的格式
    :param img_format:str 决定图片解码格式
    :return:
    """
    img =cv2.imread(img_path)
    img_encode =cv2.imencode(str(img_format),img)[1] #按img_format格式进行解码
    data_encode = np.array(img_encode).tostring()
    return data_encode

def image_encode_flush(txt_path,img_path,img_format):
    """
    把图片编码缓存保存到本地pic_diff/dir
    文件如果比较大，考虑按buffer然后做判断
    :param txt_path:pic_diff/dir写入的路径
    :param img_path:图片的格式
    :param img_format:决定图片解码格式
    :return:None
    """
    with open(str(txt_path),"w+")as fp:
        fp.write(_image_encode(img_path,img_format))
        fp.flush()



# def check_read_image_pass(img_path):
#     for i in range(0,3):
#         image = cv2.imdecode(np.fromfile(img_path),dtype=np.uint8)
#         try:
#             image.shape
#         except:
#             print('fail to read xxx.jpg')


def check_image_valid(im_source, im_search):
    """检查输入图像是否有效 any()所有元素都在则为真"""
    if im_source is not None and im_source.any() and im_search is not None and im_search.any():
        return True
    else:
        return False


def check_source_larger_than_search(im_source, im_search):
    """检查图像识别的输入."""
    # 图像格式, 确保输入图像为指定的矩阵格式:
    # 图像大小, 检查截图宽、高是否大于了截屏的宽、高:
    h_search, w_search = im_search.shape[:2]
    h_source, w_source = im_source.shape[:2]
    if h_search > h_source or w_search > w_source:
        raise TemplateInputError("error: in template match, found im_search bigger than im_source.")


def img_mat_rgb_2_gray(img_mat):
    """
    Turn img_mat into gray_scale, so that template match can figure the img data.
    "print(type(im_search[0][0])")  can check the pixel type.
    """
    assert isinstance(img_mat[0][0], np.ndarray), "input must be instance of np.ndarray"
    return cv2.cvtColor(img_mat, cv2.COLOR_BGR2GRAY)


def img_2_string(img):
    _, png = cv2.imencode('.png', img)
    return png.tostring()


def string_2_img(pngstr):
    nparr = np.fromstring(pngstr, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def pil_2_cv2(pil_image):
    open_cv_image = np.array(pil_image)
    # Convert RGB to BGR (method-1):
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    # Convert RGB to BGR (method-2):
    # b, g, r = cv2.split(open_cv_image)
    # open_cv_image = cv2.merge([r, g, b])
    return open_cv_image


def cv2_2_pil(cv2_image):
    cv2_im = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    return pil_im