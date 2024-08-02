import os
import dashscope
from dashvector import Client
from dotenv import load_dotenv
from dashscope import TextEmbedding
from search import search_relevant_news
from answer import answer_question

load_dotenv(dotenv_path="D:\zyd\Projects\Python\langchain\.env", verbose=True)

# 从环境变量中加载 Dashscope API 密钥
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
# 必须显式配置，不然后面识别不了
dashscope.api_key = dashscope_api_key

if __name__ == '__main__':
    question = '海南安定追尾事故，发生在哪里？原因是什么？人员伤亡情况如何？'
    context = search_relevant_news(question)
    answer = answer_question(question, context)

    print(f'question: {question}\n' f'answer: {answer}')
