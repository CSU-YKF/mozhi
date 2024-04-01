import os
import requests
import json

API_KEY = os.getenv('ERNIE_API_KEY')
SECRET_KEY = os.getenv('ERNIE_SECRET_KEY')


def main(f1=1, f2=4, f3=4):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"""Based on the analysis of the calligraphic copy, the following aesthetic features have been extracted:

1. Intersection over Union (IoU): {f1}
   - IoU measures the fullness of the characters and the fidelity of the copy to the template. 

2. Image Similarity: {f2}
   - This metric evaluates the visual similarity between the copy and the template, indicating how well the copy captures the essence of the template.

3. Keypoint Matching: {f3}
   - This assesses the precision of the brushstrokes, providing insight into the skill level and attention to detail of the artist.

Could you please generate a comprehensive review and guidance based on these features by Chinese? 
The review should include specific comments on each feature and overall advice on how to improve the aesthetic quality of the calligraphy.
The above three indicators range from 1 to 10. If 0 appears, the indicator is ignored.
But please do not generate any sentences that are not related to the comments, and there is no need for reasoning.
You should give the comments directly in one or two sentences like a teacher.

Your answer should look like the following example:
"字体笔画过于单薄,应当注重运笔的力度,整体布局和结构基本遵循范本,但还需提高对细节的把握,笔画结束处缺乏收.请加油!"
Please give your comments directly and do not include the following content in your answer
" 您好,根据您提供的特征分析,我给出以下评价和建议:"""
            }
        ]
    })
    headers = {
        'Content-Type': 'application'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    text = json.loads(response.text)

    return text['result']


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()
