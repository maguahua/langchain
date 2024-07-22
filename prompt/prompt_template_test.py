"""
模板中有多个参数如何写代码
"""

import os
from langchain_community.llms import Tongyi
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

# 初始化 Tongyi 模型
model = Tongyi(temperature=1, api_key=DASHSCOPE_API_KEY)

# 创建聊天模板
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

chain = template | model

res = chain.invoke(
    {
        "name": "Bob",
        "user_input": "What is your name?"
    }
)

print(res)
