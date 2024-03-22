import requests
from lxml import etree
import re


def get_basic_info(tree):
    # 图片
    image_style_str = tree.xpath('//div[@id="header-img"]/div[@class="alter-text"]/@style')[0]
    image_url = re.search(r'url\((.*)\)', image_style_str).group(1)
    # 拼音
    pinyins = tree.xpath('//div[@id="pinyin"]/span/b/text()')
    # 部首
    radical = tree.xpath('//li[@id="radical"]/span/text()')
    # 笔画
    stroke_count = tree.xpath('//li[@id="stroke_count"]/span/text()')
    # 五行
    wuxing = tree.xpath('//li[@id="wuxing"]/span/text()')
    # 繁体
    traditional = tree.xpath('//li[@id="traditional"]/span/text()')
    # 五笔
    wubi = tree.xpath('//li[@id="wubi"]/span/text()')

    return {
        "image_url": image_url,
        "pinyins": pinyins,
        "radical": radical,
        "stroke_count": stroke_count,
        "wuxing": wuxing,
        "traditional": traditional,
        "wubi": wubi
    }


def get_meaning_info(tree, pinyins):
    pronounces = tree.xpath('./dl')

    # 多音字
    if tree.xpath('./dl/dt'):
        meanings = []
        for pronounce in pronounces:
            pinyin = pronounce.xpath('./dt/span/text()')[0]

            meaning = etree.tounicode(pronounce.xpath('./dd')[0])

            meaning = re.sub(r'</?dd>', '', meaning)
            meaning = re.sub(r'\s', '', meaning)

            meanings.append({'pinyin': pinyin, 'meaning': meaning})

        return meanings

    # 非多音字
    else:
        meaning = etree.tounicode(tree.xpath('./dl/dd')[0])

        meaning = re.sub(r'</?dd>', '', meaning)
        meaning = re.sub(r'\s', '', meaning)

        return [{'pinyin': pinyins[0], 'meaning': meaning}]


def get_cn_char_info(cn_char):
    if cn_char < '\u4e00' or cn_char > '\u9fff':
        raise ValueError(f'{cn_char} is not a valid Chinese character.')

    url_root = r'https://dict.baidu.com/s?ptype=zici&wd='
    response = requests.get(url_root + cn_char)

    text = response.text

    if response.status_code != 200:
        raise RuntimeError(f'Unexpected status code: {response.status_code}.')

    tree = etree.HTML(text)

    char_name = tree.xpath('//body/@data-name')[0]

    basic_info = get_basic_info(tree.xpath('//div[@id="word-header"]')[0])
    meaning_info = get_meaning_info(tree.xpath('//div[@id="basicmean-wrapper"]/div[@class="tab-content"]')[0],
                                    basic_info['pinyins'])

    return {
        'char_name': char_name,
        'basic_info': basic_info,
        'meaning_info': meaning_info
    }
