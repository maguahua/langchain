import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.llms import Tongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = Tongyi(temperature=1)

# 设定系统上下文，构建提示词
template = """假设你是一位像李白一样的浪漫派诗人，会根据物品{obj}写诗。"""

# 创建提示词对象，用于显示给用户的最终提示
prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{obj}")])

# 通过 LCEL 构建调用链并执行得到文本输出
# StrOutputParser() 模型对象的输出转为字符串
chain = prompt | model | StrOutputParser()
for chunk in chain.stream({"obj": "江水"}):
    print(chunk, end="")
