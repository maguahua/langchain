from langchain_core.example_selectors.base import BaseExampleSelector

# examples = [
#     {"input": "hi", "output": "hi is translated into Italian as ciao"},
#     {"input": "bye", "output": "bye is translated into Italian as arrivederci"},
#     {"input": "soccer", "output": "soccer is translated into Italian as calcio"},
# ]

examples = [
    {"input": "hi", "output": "ciao"},
    # {"input": "bye", "output": "arrivederci"},
    {"input": "bye", "output": "bye is translated into Italian as arrivederci"},
    {"input": "soccer", "output": "calcio"},
]


# 选择与输入字符串长度相近的示例
class CustomExampleSelector(BaseExampleSelector):
    def __init__(self, examples):
        self.examples = examples

    def add_example(self, example):
        self.examples.append(example)

    def select_examples(self, input_variables):
        # This assumes knowledge that part of the input will be a 'text' key
        new_word = input_variables["input"]
        new_word_length = len(new_word)

        # Initialize variables to store the best match and its length difference
        best_match = None
        smallest_diff = float("inf")

        # Iterate through each example
        for example in self.examples:
            # Calculate the length difference with the first word of the example
            current_diff = abs(len(example["input"]) - new_word_length)

            # Update the best match if the current one is closer in length
            if current_diff < smallest_diff:
                smallest_diff = current_diff
                best_match = example

        return [best_match]


example_selector: BaseExampleSelector = CustomExampleSelector(examples)
temp1 = example_selector.select_examples({"input": "okay"})
# [{'input': 'bye', 'output': 'arrivederci'}]

example_selector.add_example({"input": "hand", "output": "hand is translated into Italian is mano"})
# example_selector.add_example({"input": "hand", "output": "mano"})
temp2 = example_selector.select_examples({"input": "okay"})
# [{'input': 'hand', 'output': 'mano'}]


# FewShotPromptTemplate：few-shot prompt 少量提示
import os
from langchain_community.llms import Tongyi
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

model = Tongyi(temperature=0)

example_prompt = PromptTemplate.from_template("Input: {input} -> Output: {output}")

# 提示模板
prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    suffix="Input: {input} -> Output: ",
    prefix="Translate the following words from English to Italian:",
    input_variables=["input"],
)

# print(prompt.format(input="word"))

chain = prompt | model
res = chain.invoke({"input": "win"})

print(res)  # parola

