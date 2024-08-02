import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.llms import Tongyi
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]
prompt = ChatPromptTemplate.from_template("请编写一篇关于{topic}的中文小故事，不超过100字")
print(prompt.messages[0])
model = Tongyi(temperature=1)
chain = prompt | model
res = chain.invoke({"topic": "小白兔"})
print(res)
