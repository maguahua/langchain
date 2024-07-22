import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

prompt.invoke({"topic": "cats"})
