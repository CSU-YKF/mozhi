from charinfo.cn_char_info import get_cn_char_info
from charinfo.cn_char_recog import recog_cn_char
import time


class CNCharInfoGetter:
    def __init__(self, access_token, retries=5, sleep_time=0.1):
        self.access_token = access_token
        self.retries = retries
        self.sleep_time = sleep_time

    def get_info(self, img_bin):
        char = None
        info = None

        for i in range(self.retries):
            try:
                char = recog_cn_char(img_bin, self.access_token)
            except RuntimeError:
                print('Getting output failed. Retrying...')
                time.sleep(self.sleep_time)
                continue
            except ValueError:
                return None

            break

        for i in range(self.retries):
            try:
                info = get_cn_char_info(char)
            except RuntimeError:
                print('Getting output failed. Retrying...')
                time.sleep(self.sleep_time)
                continue
            except ValueError:
                return None

            break

        return info
