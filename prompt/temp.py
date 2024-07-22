from langchain_core.prompts import PromptTemplate

# 返回的是PromptValue类型的值
prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

# 返回的是Prompt的output，res类型为langchain_core.prompt_values.StringPromptValue
res = prompt_template.invoke({"topic": "cats"})

print(res.to_string())


# import os
# from dotenv import load_dotenv, find_dotenv
# from langchain_community.llms import Tongyi
# from langchain_core.prompts import PromptTemplate
#
# load_dotenv(find_dotenv())
# DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]
# prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
# model = Tongyi(temprature=1)
# chain = prompt | model
# res = chain.invoke({"topic": "cats"})
#
# print(res)
