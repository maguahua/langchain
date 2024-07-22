import os

from langchain_community.llms import Tongyi
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

model = Tongyi(temperature=1)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

chain = prompt | model

res = chain.invoke({"msgs": [HumanMessage(content="hi!")]})

print(res)
