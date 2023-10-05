# 从anthropic官方库导入必要的包
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
#设置api密钥
anthropic = Anthropic(
    api_key="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",
)
#调用api
def claude(conversation):
 completion = anthropic.completions.create(
    #选择模型
    model="claude-2",
    #设置最大生成长度
    max_tokens_to_sample=1000,
    #设置prompt
    prompt=f"{HUMAN_PROMPT}{conversation}{AI_PROMPT}",
)
 #输出
 answer=completion.completion
 #将claude回话添加到列表，实现上下文解析
 conversation.append({"role":"claude","content":answer})
 #打印输出
 print(answer)
#创建对话空列表
conversation=[]
while True:
 prompt = input("user（输入q退出）:")
 if prompt == "q":
        break
    #将用户输入添加到列表
 conversation.append({"role":"user","content":prompt})
    #调用claude函数
 claude(conversation)
