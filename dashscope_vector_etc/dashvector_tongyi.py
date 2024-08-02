import os
import dashscope
from dashscope import TextEmbedding
from dashvector import Client, Doc
from dotenv import load_dotenv
from logger import Logger

# 初始化 Logger 实例
log = Logger(__file__)
load_dotenv(dotenv_path="../.env", verbose=True)

# 从环境变量中加载 Dashscope API 密钥
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
# 必须显式配置，不然后面识别不了
dashscope.api_key = dashscope_api_key


# 处理CEC-Corpus-master中所有数据
def prepare_data(path, batch_size=25):
    batch_docs = []
    for file in os.listdir(path):
        with open(path + '/' + file, 'r', encoding='utf-8') as f:
            batch_docs.append(f.read())
            if len(batch_docs) == batch_size:
                yield batch_docs
                batch_docs = []

    if batch_docs:
        yield batch_docs


def generate_embeddings(news):
    response = TextEmbedding.call(
        model=TextEmbedding.Models.text_embedding_v1,
        input=news
    )

    embeddings = [record['embedding'] for record in response.output['embeddings']]
    result = embeddings if isinstance(news, list) else embeddings[0]
    return result


if __name__ == '__main__':

    # 初始化 dashvector 客户端
    client = Client(
        api_key=os.getenv("DASHVECTOR_API_KEY"),
        endpoint=os.getenv("ENDPOINT")
    )

    # 列出现有集合
    existing_collections = client.list()

    # 指定集合名称和向量维度
    collection_name = "CEC-Corpus-TextEmbedding"

    if collection_name not in existing_collections:
        rsp = client.create(collection_name, 1536)

    # 加载数据
    id = 0
    # 获取集合
    collection = client.get(collection_name)
    if not collection:
        log.error(f"获取集合失败: {collection_name}.")
        raise Exception(f"获取集合失败: {collection_name}.")

    for news_batch in prepare_data('CEC-Corpus-master/raw corpus/allSourceText'):
        ids = [id + i for i, _ in enumerate(news_batch)]
        id += len(news_batch)
        vectors = generate_embeddings(news_batch)

        # 将文档插入集合
        rsp = collection.upsert(
            [
                Doc(id=str(doc_id), vector=vector, fields={"raw": doc})
                for doc_id, vector, doc in zip(ids, vectors, news_batch)
            ]
        )
