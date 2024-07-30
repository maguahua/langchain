import os

import dashscope
from dashscope import TextEmbedding

from dashvector import Client, Doc


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
    rsp = TextEmbedding.call(
        model=TextEmbedding.Models.text_embedding_v1,
        input=news
    )
    embeddings = [record['embedding'] for record in rsp.output['embeddings']]
    return embeddings if isinstance(news, list) else embeddings[0]


if __name__ == '__main__':
    dashscope.api_key = '{sk-95ec6c38888044ce8a5addd4224edc83}'

    # 初始化 dashvector client
    client = Client(
        api_key='sk-QC92s09WrepVav5GjI20PyeB6vJ2CE44D34634A6211EFA11DB2CF21235769',
        endpoint='vrs-cn-fou3ucvg500011.dashvector.cn-beijing.aliyuncs.com'
    )

    # 创建集合：指定集合名称和向量维度, text_embedding_v1 模型产生的向量统一为 1536 维
    rsp = client.create('zydCollection_2', 1536)
    assert rsp

    # 加载语料
    id = 0
    collection = client.get('zydCollection_2')
    for news in list(prepare_data('dashscope_vector_etc/CEC-Corpus-master/raw corpus/allSourceText')):
        ids = [id + i for i, _ in enumerate(news)]
        id += len(news)

        vectors = generate_embeddings(news)
        # 写入 dashvector 构建索引
        rsp = collection.upsert(
            [
                Doc(id=str(id), vector=vector, fields={"raw": doc})
                for id, vector, doc in zip(ids, vectors, news)
            ]
        )
        assert rsp
