import requests
import os

api_key = os.getenv("DASHSCOPE_API_KEY")
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
headers = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {api_key}'}

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]

# 封装模型的响应函数
def get_response(last_messages):
    body = {
        'model': 'qwen-turbo',
        "input": {
            "messages": last_messages
        },
        "parameters": {
            "result_format": "message"
        }
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

# 您可以在此修改对话轮数，当前为3轮对话
for i in range(3):
    UserInput = input('请输入：')
    messages.append({
        "role": "user",
        "content": UserInput
    })
    response = get_response(messages)
    assistant_output = response['output']['choices'][0]['message']
    print("用户输入：", UserInput)
    print(f"模型输出：{assistant_output['content']}\n")
    messages.append(assistant_output)