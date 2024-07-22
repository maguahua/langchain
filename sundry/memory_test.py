import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]


from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import Runnable, RunnableLambda, RunnableSequence

# 初始化LLM
llm = Tongyi(api_key=DASHSCOPE_API_KEY)

# 定义提示模板，必须用chat_memory来命名之后要插入的字符串
template = '''你是一个美少女，你的名字是燕砸，你的任务是用温柔的语气回答人类的问题。
{chat_memory}
human: {question}
'''

prompt = PromptTemplate(
    template=template,
    # input_variables 是一个列表，指定了模板中需要替换的变量名称。这个列表中的变量名应该与模板中的占位符一致
    input_variables=["question", "chat_memory"]
)

# 初始化记忆
memory = ConversationBufferMemory(memory_key="chat_memory", return_messages=False, input_key="human", output_key="ai")


# 自定义Runnable以处理对话
class ConversationRunnable(Runnable):
    def __init__(self, llm, prompt, memory):
        self.llm = llm
        self.prompt = prompt
        self.memory = memory

    def invoke(self, inputs, config=None):
        # 构建提示
        prompt_text = self.prompt.format(
            question=inputs,
            # 必须和input_variables中的字符串列表各字符串是一样的
            chat_memory=self.memory.chat_memory
        )

        # 调用LLM
        response = self.llm.generate([prompt_text])  # 传递一个列表
        response_text = response.generations[0][0].text  # 获取响应文本

        # 更新记忆
        self.memory.save_context({"human": inputs}, {"ai": response_text})

        return response_text


# 初始化ConversationRunnable
conversation_runnable = ConversationRunnable(llm, prompt, memory)


# 创建一个处理输入的 Runnable
def wrap_inputs(inputs):
    return inputs


# 使用RunnableSequence组合组件:首先执行 wrap_inputs，然后将其输出作为输入传递给 conversation_runnable。
sequence = (
    RunnableLambda(wrap_inputs) |
    conversation_runnable
)

# 模拟对话
sequence.invoke("我喜欢美食,我最喜欢的美食是清蒸鲈鱼")
sequence.invoke("你是谁?")
sequence.invoke("今天的天气真好啊")
res = sequence.invoke("我最开始跟你聊的什么呢？")

print(res)
