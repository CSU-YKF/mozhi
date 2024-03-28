import os

from charinfo.cn_char_info import get_cn_char_info
from charinfo.cn_char_recog import recog_cn_char


'''
获取信息失败时抛出 RuntimeError，需要异常处理
当输入图像未检测出有效汉字输出 None
'''
def get_info(img_base64):
    try:
        char = recog_cn_char(img_base64)
    except ValueError:
        return None

    try:
        info = get_cn_char_info(char)
    except ValueError:
        return None

    return info


'''
调用此方法直接获取识别到的文字和DOM元素
'''
def get_char_and_infodom(img_base64):
    info = get_info(img_base64)
    char = info['char_name']
    basic_dom, meaning_dom = to_dom(info)
    return char, basic_dom, meaning_dom
