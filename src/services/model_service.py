import base64
from typing import Dict
try:
    from ..score import gnn_score
    from ..recognize import recog_cn_char, get_cn_char_info
    from ..comment import gpt_comment
except ModuleNotFoundError:
    pass


def evaluate_image(image_base64: str) -> Dict:
    try:
        score = gnn_score(image_base64)
        char_name = recog_cn_char(image_base64)
        comment = gpt_comment(image_base64, char_name, score)
    except Exception as e:
        score = 0
        char_name = "未知"
        comment = None
    # file_bytes = base64.b64decode(image_base64)
    # file_base64 = base64.b64encode(file_bytes).decode('utf-8')

    # char_name, basic_dom, meaning_dom = get_char_and_infodom(file_base64)


    return {
        "score": score,
        "comment": comment,
        "charName": char_name
    }
