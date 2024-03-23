from charinfo.cn_char_info import get_cn_char_info
from charinfo.cn_char_recog import recog_cn_char


class CNCharInfoGetter:
    def __init__(self, access_token):
        self.access_token = access_token

    '''
    获取信息失败时抛出 RuntimeError，需要异常处理
    当输入图像未检测出有效汉字输出 None
    '''
    def get_info(self, img_bin):
        try:
            char = recog_cn_char(img_bin, self.access_token)
        except ValueError:
            return None

        try:
            info = get_cn_char_info(char)
        except ValueError:
            return None

        return info
