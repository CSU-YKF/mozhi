import os
import base64
import requests

KEY_PATH = os.path.join(os.path.dirname(__file__), 'baidu.txt')


def get_baidu_access_token():
    with open(KEY_PATH, 'r') as file:
        access_token = file.read().strip()
    return access_token


BAIDU_ACCESS_TOKEN = get_baidu_access_token()


# 百度云 API
def recog_cn_char(img_base64):
    url_root = 'https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting'

    url = f'{url_root}?access_token={BAIDU_ACCESS_TOKEN}'

    response = requests.post(url, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }, data={
        'image': img_base64
    })

    if response.status_code != 200:
        raise RuntimeError(f'Unexpected status code: {response.status_code}.')

    response_data = response.json()

    try:
        pred_char = response_data['words_result'][0]['words']
    except KeyError:
        raise RuntimeError('Got error response.')
    except IndexError:
        raise ValueError('Did\'t detected any characters.')

    return pred_char


if __name__ == '__main__':
    # 使用test.png作为测试图片

    with open('../../../tests/ni.png', 'rb') as file:
        img_base64 = base64.b64encode(file.read()).decode()
        print(img_base64)
    # result = recog_cn_char(img_base64)
    #     result = recog_cn_char(file.read())
    # print(result)
