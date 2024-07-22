import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.llms import Tongyi
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

model = Tongyi(temperature=1, api_key=DASHSCOPE_API_KEY)

examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]

example_prompt = ChatPromptTemplate.from_messages(
    messages=examples,
    template_format="'input': {input}\n'output':{output}"

)

example_selector = LengthBasedExampleSelector(
    # 提示模板期望使用的示例列表
    examples=examples,
    # 用于格式化示例的提示模板
    example_prompt=example_prompt,
    # 设定期望的示例文本长度
    max_length=25
)
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    # 设置示例以外部分的前置文本
    prefix="Give the antonym of every input",
    # 设置示例以外部分的后置文本
    suffix="Input: {adjective}\nOutput:\n\n",
    input_variables=["adjective"],
)

# 当用户输入的内容比较少时，所有示例都足够被使用
print(dynamic_prompt.format(adjective="big"))

# 当用户输入的内容足够长时，只有少量示例会被引用
long_string = "big and huge and massive and large and gigantic and tall and much much much much much bigger than " \
              "everything else "
print(dynamic_prompt.format(adjective=long_string))
