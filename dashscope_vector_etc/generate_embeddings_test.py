import logging
import warnings
import json

from dashscope import TextEmbedding
from dashvector import Client, Doc

# 忽略所有 UserWarning 警告
warnings.filterwarnings("ignore", category=UserWarning)

#
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m%d%Y %H:%M:%S",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("generate_embeddings_test.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
logger.addHandler(file_handler)


# 准备数据
# 输入：path，文件路径，size，每个batch的大小
# 输出：每次迭代返回一个包含指定大小文档的列表
# 调整 prepare_data 函数，确保返回所有文档
def prepare_data(path, size):
    max_docs = 100  # 设定返回数据的最大数量
    count = 0  # 计数器，记录已经读取的文档数量

    with open(path, 'r', encoding='utf-8') as f:
        batch_docs = []
        for line in f:
            if count >= max_docs:
                break

            batch_docs.append(json.loads(line.strip()))
            count += 1

            if len(batch_docs) == size:
                yield batch_docs[:]
                batch_docs = []

        if batch_docs:
            yield batch_docs


# embedding过程
# 输入：文本字符串或字符串列表
# 输出：单个文本或文本列表对应的向量
def generate_embeddings(text):
    rsp = TextEmbedding.call(model=TextEmbedding.Models.text_embedding_v1, input=text)

    embeddings = [record['embedding'] for record in rsp.output['embeddings']]
    return embeddings if isinstance(text, list) else embeddings[0]


# 初始化 DashVector client
# DashVector API KEY和Cluster的endpoint
client = Client(
    api_key='sk-QC92s09WrepVav5GjI20PyeB6vJ2CE44D34634A6211EFA11DB2CF21235769',
    endpoint='vrs-cn-fou3ucvg500011.dashvector.cn-beijing.aliyuncs.com'
)

logger.info(f"client 正在初始化...")

# 指定集合名称和向量维度
logger.info("正在检查collections...")
existing_collections = client.list()

collection_name = "zydCollection_test"

if collection_name not in existing_collections:
    logger.info(f"collection{collection_name} 不存在, 正在创建...")
    rsp = client.create(collection_name, 1536)
    if rsp.code == 0:
        logger.info(f"创建collection成功.")
    else:
        logger.info({f"创建collection失败，返回值：{rsp}."})
        raise Exception(f"创建collection失败，返回值：{rsp}.")

else:
    logger.info(f"collection{collection_name} 已经存在.")

# 获取集合
collection = client.get(collection_name)
if not collection:
    logger.error(f"获取collection失败: {collection_name}.")
    raise Exception(f"获取collection失败: {collection_name}.")

batch_size = 10
for docs in prepare_data('QBQTC-main/dataset/train.json', batch_size):
    embeddings = generate_embeddings([doc["title"] for doc in docs])
    if not embeddings:
        logger.error("生成embeddings失败.")
        continue

    # 插入的数据类型是Doc
    rsp = collection.insert(
        [
            Doc(id=str(doc['id']), vector=embedding, fields={"title": doc['title']})
            for doc, embedding in zip(docs, embeddings)
        ]
    )

    if rsp.code == 0:
        logger.info(f"插入文件成功，返回值：{rsp}")
    else:
        logger.error(f"插入文件失败，返回值：{rsp}.")
        raise Exception(f"插入文件失败，返回值：{rsp}.")
