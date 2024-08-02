import os
import dashscope
from dashvector import Client
from dotenv import load_dotenv
from dashscope import TextEmbedding

load_dotenv(dotenv_path="D:\zyd\Projects\Python\langchain\.env", verbose=True)

# 从环境变量中加载 Dashscope API 密钥
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
# 必须显式配置，不然后面识别不了
dashscope.api_key = dashscope_api_key


def generate_embeddings(news):
    response = TextEmbedding.call(
        model=TextEmbedding.Models.text_embedding_v1,
        input=news
    )

    embeddings = [record['embedding'] for record in response.output['embeddings']]
    result = embeddings if isinstance(news, list) else embeddings[0]
    return result


def search_relevant_news(question):
    # 初始化 dashvector client
    client = Client(
        api_key=os.getenv("DASHVECTOR_API_KEY"),
        endpoint=os.getenv("ENDPOINT")
    )

    # 获取刚刚存入的集合
    collection = client.get('CEC-Corpus-TextEmbedding')
    assert collection

    # 向量检索：指定 topk = 1
    rsp = collection.query(generate_embeddings(question), output_fields=['raw'],
                           topk=1)
    assert rsp
    return rsp.output[0].fields['raw']
