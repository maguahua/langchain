import logging
import warnings
import json


# 忽略所有 UserWarning 警告
warnings.filterwarnings("ignore", category=UserWarning)

#
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m%d%Y %H:%M:%S",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("generate_embeddings.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
logger.addHandler(file_handler)


# 准备数据
# 输入：path，文件路径，size，每个batch的大小
# 输出：每次迭代返回一个包含指定大小文档的列表，最终输出文档列表的列表
def prepare_data(path, size):
    with open(path, 'r', encoding='utf-8') as f:
        batch_docs = []
        for line in f:
            batch_docs.append(json.loads(line.strip()))
            if len(batch_docs) == size:
                yield batch_docs[:]
                batch_docs.clear()

        if batch_docs:
            yield batch_docs


from dashscope import TextEmbedding


# embedding过程
# 输入：文本字符串或字符串列表
# 输出：单个文本或文本列表对应的向量
def generate_embeddings(text):
    rsp = TextEmbedding.call(model=TextEmbedding.Models.text_embedding_v1, input=text)

    embeddings = [record['embedding'] for record in rsp.output['embeddings']]
    return embeddings if isinstance(text, list) else embeddings[0]


from dashvector import Client, Doc

# 初始化 DashVector client
# DashVector API KEY和Cluster的endpoint
client = Client(
    api_key='sk-QC92s09WrepVav5GjI20PyeB6vJ2CE44D34634A6211EFA11DB2CF21235769',
    endpoint='vrs-cn-fou3ucvg500011.dashvector.cn-beijing.aliyuncs.com'
)

logger.info("Client initialized: %s", client)

# 指定集合名称和向量维度
logger.info("Checking collections...")
existing_collections = client.list()

if 'zydCollection' not in existing_collections:
    logger.info("zydCollection does not exist, creating it...")
    rsp = client.create('zydCollection', 1536)
    logger.info("Response from create: %s", rsp)
    if rsp.code != 0:
        logger.error("Error creating collection: %s", rsp)
        raise Exception(f"Error creating collection: {rsp}")
else:
    logger.info("zydCollection already exists.")

# 获取集合
collection = client.get('zydCollection')
if not collection:
    logger.error("Failed to get collection: zydCollection")
    raise Exception("Failed to get collection: zydCollection")

batch_size = 10
for docs in list(prepare_data('QBQTC-main/dataset/new_train.json', batch_size)):
    # 批量 embedding
    embeddings = generate_embeddings([doc['title'] for doc in docs])

    # 批量写入数据
    rsp = collection.insert(
        [
            Doc(id=str(doc['id']), vector=embedding, fields={"title": doc['title']})
            for doc, embedding in zip(docs, embeddings)
        ]
    )
    print("Response from insert: %s", rsp)
    if rsp.code != 0:
        logger.error("Error inserting documents: %s", rsp)
        raise Exception(f"Error inserting documents: {rsp}")

# 基于向量检索的语义搜索
rsp = collection.query(generate_embeddings('应届生 招聘'), output_fields=['title'])
print("Response from query: %s", rsp)

for doc in rsp.output:
    print(f"id: {doc.id}, title: {doc.fields['title']}, score: {doc.score}")
