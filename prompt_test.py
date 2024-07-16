import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate

model = Tongyi(temperature=1)
template = '''
        你是一个不耐烦的老奶奶,非常不愿意回答问题,请你不耐烦的回答:{question}
    '''
prompt = PromptTemplate(
    template=template,
    input_variables=["question"]
)
chain = prompt | model
question = '什么是人工智能？'

res = chain.invoke({"question": question})
print("无prompt--->\n", model.invoke(question), "\n")
print("有prompt--->\n", res)
