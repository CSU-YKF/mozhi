from charinfo.cn_char_info import get_cn_char_info
from charinfo.cn_char_recog import recog_cn_char


class CNCharInfoGetter:
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def _to_dom(info):
        basic_dom = ''

        pinyins_plain = info['basic_info']['pinyins'][0]
        if len(info['basic_info']['pinyins']) > 1:
            for i, pinyin in enumerate(info['basic_info']['pinyins']):
                if i == 0:
                    continue
                pinyins_plain += ' ' + pinyin

        radical = info['basic_info']['radical']
        stroke_count = info['basic_info']['stroke_count']
        wuxing = info['basic_info']['wuxing']
        traditional = info['basic_info']['traditional']
        wubi = info['basic_info']['wubi']

        for item in [('拼音', pinyins_plain),
                     ('部首', radical),
                     ('笔画', stroke_count),
                     ('五行', wuxing),
                     ('繁体', traditional),
                     ('五笔', wubi)]:
            basic_dom += f'<span class="char-basic-item"><span style="font-weight: bolder">{item[0]}：</span>{item[1]}</span>'

        basic_dom = '<div id="char-basic">' + basic_dom + '</div>'

        meaning_dom = ''

        if len(info['meaning_info']) == 1:
            meaning_dom = '<div class="char-meaning-item">' + info['meaning_info'][0]['meaning'] + '</div>'
        else:
            for item in info['meaning_info']:
                meaning_dom += '<div class="char-meaning-item"><h4>' + item['pinyin'] + '</h4>'
                meaning_dom += item['meaning'] + '</div>'

        meaning_dom = '<div id="char-meaning">' + meaning_dom + '</div>'

        char_info_dom = '<div id="char_info">' + basic_dom + meaning_dom + '</div>'

        return char_info_dom

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

    '''
    调用此方法直接获取识别到的文字和DOM元素
    '''
    def get_char_and_infodom(self, img_bin):
        info = self.get_info(img_bin)
        char = info['char_name']
        dom = self._to_dom(info)
        return char, dom
