import os
import base64
import requests

from openai import OpenAI

# 从环境变量中导入API_KEY
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def gpt_comment(image_src, image_type: str, image_score: float) -> str:
    base64_image = encode_image(image_src)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    with open("prompt.txt", "r") as f:
        system_content = f.read()

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
