import base64
import numpy as np
from typing import Dict

from src.score import gnn_score
from src.recognize import recog_cn_char, get_cn_char_info
from src.comment import gpt_comment


async def evaluate_image(image_path: str) -> Dict:
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    score = gnn_score(image_path)
    try:
        char_name = recog_cn_char(image_base64)
    except Exception:
        char_name = "未知"
    comment = gpt_comment(image_base64, char_name, score)
    # except Exception:
    #     score = 0
    #     char_name = "未知"
    #     comment = None
    # file_bytes = base64.b64decode(image_base64)
    # file_base64 = base64.b64encode(file_bytes).decode('utf-8')

    # char_name, basic_dom, meaning_dom = get_char_and_infodom(file_base64)

    return {
        "score": score,
        "comment": comment,
        "charName": char_name
    }


if __name__ == '__main__':

    print(evaluate_image("../../tests/ni.png"))
    #     b = f.read()
    #
    #     Image.open(b).show()
    # print(evaluate_image("fu.jpg"))
