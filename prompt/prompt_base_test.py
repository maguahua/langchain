import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.llms import Tongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

model = Tongyi(temperature=1)

# 设定系统上下文，构建提示词
template = """请扮演一位资深的技术博主，您将负责为用户生成适合在微博发送的中文帖文。
请把用户输入的内容扩展成 140 字左右的文字，并加上适当的 emoji 使内容引人入胜并专业。"""

# 创建提示词对象，用于显示给用户的最终提示
prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{input}")])

# 通过 LCEL 构建调用链并执行得到文本输出
# StrOutputParser() 模型对象的输出转为字符串
chain = prompt | model | StrOutputParser()
res = chain.invoke({"input": "给大家推荐一本新书《LangChain实战》，让我们一起开始来学习 LangChain 吧！"})
print(res)
