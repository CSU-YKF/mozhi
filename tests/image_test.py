import requests

# 服务器的URL
url = "http://localhost:8080/upload"

# 要上传的文件路径
file_path = "6.jpeg"

# 打开文件
with open(file_path, "rb") as file:
    # 发送MultiPart请求
    response = requests.post(url, files={"file": file})

# 检查响应状态码
if response.status_code == 200:
    # 解析响应JSON数据
    result = response.json()
    print("文件上传成功!")
    print("文件名:", result["filename"])
    print("内容类型:", result["content_type"])
else:
    print("文件上传失败,状态码:", response.status_code)