import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate

model = Tongyi(temperature=0)
template = """
不要给出过程
输入一句话
{question}
以“The answer is”格式回答，is后面写的是上面输入的那句话的正确性，正确写right，错误写wrong

"""
prompt = PromptTemplate(
    template=template,
    input_variables=["question"]
)

# Create the chain with the model
chain = prompt | model

# Define the question
question = "The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1."

# Invoke the chain with the question
res = chain.invoke({"question": question})

print("无prompt--->\n", model.invoke(question), "\n")
print("有prompt--->\n", res)
