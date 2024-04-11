import os
import base64
import requests

from openai import OpenAI

# 从环境变量中导入API_KEY
# API_KEY = os.getenv("OPENAI_API_KEY")
KEY_PATH = os.path.join(os.path.dirname(__file__), 'gpt.txt')

# 从gpt.key 文件中导入API_KEY
with open(KEY_PATH, 'r') as file:
    API_KEY = file.read().strip()

client = OpenAI(api_key=API_KEY)

# 从system.txt中导入系统内容
with open(os.path.join(os.path.dirname(__file__), 'system.txt'), 'r', encoding='utf-8') as file:
    SYSTEM_CONTENT = file.read()


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

    system_content = SYSTEM_CONTENT

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


if __name__ == '__main__':
    # 使用test.png作为测试图片
    with open('fu.jpg', 'rb') as file:
        img_base64 = base64.b64encode(file.read()).decode()
    result = gpt_comment(img_base64, '夫', 6)
    print(result)
