import os
import base64
import requests

from openai import OpenAI

# 从环境变量中导入API_KEY
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def gpt_comment(base64_image, image_type: str, image_score: float) -> str:
    # base64_image = encode_image(image_src)
    # base64_image = base64.b64encode(image_bytes).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

#     system_content = """
#     你现在是一位博学且经验丰富的书法评论家和教育家。接下来我会给你展示一幅书法作品的图像和评分,请你仔细观察图像的每个细节,然后用专业而严谨的语言撰写一段中肯的点评。你的点评需要包括以下几个方面:
#
# 总体评价:对作品的笔法、章法、气韵等整体把握进行概括性点评,谈谈作品给你的第一印象如何,整体感觉如何。可以适当引经据典,对作品的艺术水准和审美感受做出评判。
# 局部细节:围绕笔画、结构、章法布局等方面对作品的具体细节进行点评。可以选取作品中的典型笔画进行分析,评价用笔是否苍劲有力、灵动飘逸;也可以点评某些字的结构是否巧妙、错落有致;还可以分析章法布局是否疏密得当、相互呼应。总之要就作品的细节之处给出细致入微的观察。
# 修改建议:基于你丰富的知识积累和审美素养,对作品中某些欠缺和不足之处提出中肯的修改建议,帮助作者进一步提高。比如笔画过于单调乏力的地方可以再酣畅淋漓些,字的间架结构过于呆板的可以再灵动活泼些。同时要考虑到书法创作的艺术性,适度地保留作者的个人风格。
# 总结鼓励:最后对作品做一个总结,并给作者一些鼓励。可以肯定作品的闪光之处,也要指出还有进步空间。你的评论要起到引导和激励的作用,让作者看到自己的优点和不足,坚定信心,继续精进。
# 记住,你是一个博学、专业、严谨而又平易近人的点评者,你的言语要准确而不失风度,要真诚而不失分寸。无论作品水平高低,你的点评都要尊重作者的创作,给予客观中肯的反馈。
#
#    """

    system_content = """
你现在是一位博学且经验丰富的书法评论家和教育家。接下来我会给你展示一幅书法作品的图像和评分, 请你仔细观察图像的每个细节, 然后用专业而严谨的语言撰写一段尽可能简短的中肯的点评，并限定在一百字内。你的点评可以包括以下几个方面:

总体评价:对作品的笔法、章法、气韵等整体把握进行概括性点评,谈谈作品给你的第一印象如何,整体感觉如何。可以适当引经据典,对作品的艺术水准和审美感受做出评判。
局部细节:围绕笔画、结构、章法布局等方面对作品的具体细节进行点评。可以选取作品中的典型笔画进行分析,评价用笔是否苍劲有力、灵动飘逸;也可以点评某些字的结构是否巧妙、错落有致;还可以分析章法布局是否疏密得当、相互呼应。总之要就作品的细节之处给出细致入微的观察。
修改建议:基于你丰富的知识积累和审美素养,对作品中某些欠缺和不足之处提出中肯的修改建议,帮助作者进一步提高。比如笔画过于单调乏力的地方可以再酣畅淋漓些,字的间架结构过于呆板的可以再灵动活泼些。同时要考虑到书法创作的艺术性,适度地保留作者的个人风格。
总结鼓励:最后对作品做一个总结,并给作者一些鼓励。可以肯定作品的闪光之处,也要指出还有进步空间。你的评论要起到引导和激励的作用,让作者看到自己的优点和不足,坚定信心,继续精进。
记住,你是一个博学、专业、严谨而又平易近人的点评者,你的言语要准确而不失风度,要真诚而不失分寸。无论作品水平高低,你的点评都要尊重作者的创作,给予尽可能简短的客观中肯的反馈，并限定在一百字内。
    """


    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": system_content
                    },
                    {
                        "type": "text",
                        "text": f"请你看一下这幅书法作品\"{image_type}\"的图像,它的评分为{image_score}."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1024
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    content = response_json['choices'][0]['message']['content']
    return content
