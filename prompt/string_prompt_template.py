import os

from dotenv import find_dotenv, load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.llms import Tongyi

load_dotenv(find_dotenv())

# 需要配置环境变量DASHSCOPE_API_KEY
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

model = Tongyi(temperature=1)

# from_template返回值为PromptValue
prompt = PromptTemplate.from_template("tell me a joke about {topic}")

chain = prompt | model

res = chain.invoke({"topic": "cats"})

print(res)
