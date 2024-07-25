# LangChain指南

- [LangChain基本概念](#LangChain基本概念)
  - [架构（包）](#架构（包）)
  - [关于LangChain Expression Language(LCEL)](#关于LangChain Expression Language(LCEL))
- [LangChain组件](#LangChain组件)
  - [LLMs大语言模型](#LLMs 大语言模型)
  - [Chat models 聊天模型](#Chat models 聊天模型)
  - [Messages 消息](#Messages 消息)
  - [Prompt templates 提示模板](#Prompt templates 提示模板)
    - [PromptTemplates](#PromptTemplates)
    - [ChatPromptTemplates](#ChatPromptTemplates)
    - [MessagesPlaceholder](#MessagesPlaceholder)
  - [Example selectors 模板选择器](#Example selectors 模板选择器)
  - [Output parsers 输出解析器](#Output parsers 输出解析器)
  - [Chat history 聊天历史](#Chat history 聊天历史)
  - [Document 文件](#Document 文件)
  - [Document loaders 文件加载器](#Document loaders 文件加载器)
  - [Text splitters 文本拆分器](#Text splitters 文本拆分器)
  - [Embedding models 嵌入模型（阿里云文档）](#Embedding models 嵌入模型（阿里云文档）)
  - [Vector stores 向量存储](#Vector stores 向量存储)
- [准备工作](#准备工作)
  - [通义](#通义)
  - [OpenAI](#OpenAI)
  - [灵积服务模型](#灵积服务模型)

## <font color=#ED7D31>LangChain基本概念</font> 

用于开发由LLM驱动的应用程序框架，简化了LLM应用程序生命周期的每个阶段

### <font color=#70AD47>架构（包）</font> 

> - `langchain-core`：定义一些核心接口（轻量级）
> - `langchain-community`：第三方集成。一些比较流行的包被提取出来
>   - `langchain-openai`
>   - `langchain-anthropic`
> - `langgraph`：流程/状态控制（可单独工作）
> - `langserve`：实现以REST API形式部署LangChain runnables和链
> - `langsmith`：监控和评估LLM App（可单独工作）

### <font color=#70AD47>关于LangChain Expression Language(LCEL)</font> 

声明式的LangChain组件链，为尽可能方便地创建自定义链，运用Runnable标准接口

> - `stream`：逐块返回相应内容（响应分段发送）
> - `invoke`：对单个输入调用链并获取结果
> - `batch`：对多个输入调用链并获取结果，一次性处理这些输入

上述接口也对应异步方法，应与`asyncio`的`await`语法一起使用实现并发

> - `astream`：
> - `ainvoke`：
> - `abatch`：
> - `astream_log`：异步逐块返回中间步骤和最终响应（在处理过程中可实时获取中间步骤结果）
> - `astream_events`：异步逐块返回链中的事件（langchain-core 0.1.14中引入beta版）

input type和output type因为组件不同而不同

|     组件     |                      输入类型                       |       输出类型        |
| :----------: | :-------------------------------------------------: | :-------------------: |
|    Prompt    |                     Dictionary                      |      PromptValue      |
|  ChatModel   | Single string,list ofchat messages or a PromptValue |      ChatMessage      |
|     LLM      | Single string,list ofchat messages or a PromptValue |        String         |
| OutputParser |          The output of an LLM or ChatModel          | Depends on the parser |
|  Retriever   |                    Single string                    |   List of Documents   |
|     Tool     | Single string or dictionary, depending on the tool  |  Depends on the tool  |

所有的runnable都会暴露`input`和`output`方案以便检查

- `input_schema`：根据Runnable结构自动生成的`input`Pydantic模型
- `output_schema`：根据Runnable结构自动生成的`output`Pydantic模型

## <font color=#ED7D31>LangChain组件</font> 

> [!IMPORTANT]
>
> 本部分为概述性概念指南，仅描述典型基础代码，列出了官方文档中相关使用方法，请自行查阅

### <font color=#70AD47>LLMs 大语言模型</font> 

[How-to guides: LLMs](https://python.langchain.com/v0.2/docs/how_to/#llms)

LLMs是传统上比较旧的模型（较新通常是Chat models），将字符串作为输入并返回字符串

LangChain允许将这些模型将Messages作为输入，这些输入将被LangChain wrappers格式化为一个字符串，然后再被传到底层模型

### <font color=#70AD47>Chat models 聊天模型</font> 

[How-to guides: Chat models](https://python.langchain.com/v0.2/docs/how_to/#chat-models)

消息作为输入和输出（不是纯文本）的语言模型，但允许将字符串作为输入作为`HumanMessage`传递给底层模型

**一些标准参数**

> - `model`：模型名
> - `temperature`：0-1之间，数字越大，llm的创造力越强（越不精确）
> - `timeout`：请求超时时间
> - `max_tokens`：最大可生成tokens
> - `stop`：默认停止序列
> - `max_retries`：最大重新请求次数
> - `api_key`：模型提供者API密钥（如DASHSCOPE_API_KEY，OPEN_API_KEY）
> - `base_url`：发送请求的端点

> [!NOTE]
>
> - 不是所有的模型中都包含全部标准参数，没有被公开的标准参数不能被使用
> - 标准参数只在那些有自己集成包的集成中强制执行（langchain-openai等），在langchain-community中标准参数不被强制执行
> - 对于多模态模型，因其不常见，因此还没有标准化定义的API

LangChain不托管任何Chat models和LLMs，而是依赖第三方集成

### <font color=#70AD47>Messages 消息</font>

一些模型将消息列表作为输入，并返回一条消息。不同类型的消息都包含

> - `role`:谁提交的信息，LangChain针对不同的role有不同的消息类
> - `content`:信息内容，一个字符串（大多数模型处理这种内容）；一个字典列表（用于多模态输入）
> - `response_metadata`:包含有关响应的附加元数据，一般都是模型中的专用数据，可能会存储日志问题和tokens使用情况等信息

Message主要分为以下几类（仅包含特殊属性）

> - `HumanMessage`：用户输入信息
> - `AIMessage`：模型信息
>   - ` tool_calls`：AIMessage输出的一部分，可以通过`.tool_calls`来访问
>    - `name`：工具名
>     - `args`：工具args
>     - ` id`： tool call的id
> - `SystemMessage`：一条系统消息，告诉模型怎么做（不是每个模型都支持）
> - `ToolMessage`：tool call之后的结果
>   - `tool_call_id`：用于传递产生此结果的tool call的id
>  - `artifact`：用于传递工具执行过程中的任意工具（对跟踪有用，不发送到模型中）
> - `FunctionMessage`：ToolMesage的的旧版，适用于OpenAI的旧版函数调用API

### <font color=#70AD47>Prompt templates 提示模板</font> 

[How-to guides: Prompt templates](https://python.langchain.com/v0.2/docs/how_to/#prompt-templates)

通俗说，prompt就是在与ChatGPT聊天时，用户在聊天框输入的文字（**发出的指令**）

- 输入为字典，每个键代表提示模板中要填写的变量
- 输出为`PromptValue`，可以转换为LLM或ChatModel，也可以转换为字符串或消息列表（便于字符串和消息之间的类型转换）

#### PromptTemplates

用于格式化单个**字符串**，通常用于比较简单的输入。构造和使用PromptTemplate的常见方法

```python
import os

from dotenv import find_dotenv, load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.llms import Tongyi

load_dotenv(find_dotenv())
# 需要配置环境变量DASHSCOPE_API_KEY
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]

model = Tongyi(temperature=1)

# from_template返回值为PromptValue
prompt = PromptTemplate.from_template("tell me a joke about {topic}")

# chain的类型为RunnableSerializable
chain = prompt | model

res = chain.invoke({"topic": "cats"})

print(res)
```

> [!NOTE]
>
> 1. DASHSCOPE_API_KEY的创建和使用在[准备工作](#准备工作)中描述，以下代码将省略获取API key部分代码
> 2. 模型的调用方法默认为以上方法

#### ChatPromptTemplates

为**Chat models**生成提示模板——一个聊天信息列表，列表中的每一条信息都有一个身份，比如系统、用户或AI

```python
from langchain.prompts import ChatPromptTemplate

# ChatPromptTemplate调用时会构造两个消息，SystemMessage和HumanMessage
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant"),
        ("user", "tell me a joke about {topic}")
    ]
)
```

#### MessagesPlaceholder

如果想传进一个message列表，并将其插入特定位置，可以使用MessagesPlaceholder

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

res = chain.invoke({"msgs": [HumanMessage(content="hi!")]})
```

### <font color=#70AD47>Example selectors 模板选择器</font>

[How-to guides: Example selectors](https://python.langchain.com/v0.2/docs/how_to/#example-selectors)

为提高语言模型的性能，常见的方法是将示例包含在提示中。Example selectors就是负责选择这些示例并将它们格式化到提示中的工具类，一般有以下方法

> 1. 硬编码：直接在提示中写入固定的示例
> 2. 动态选择示例：根据具体情况动态选择合适的示例

下面这段代码中， 若让其翻译一个长度为3的单词，output就是"xxx is translated into Italian as xxx."如果让其翻译一个长度为4的代码，output只有翻译结果，因为examples中列出了长度不同应如何回复的示例

```python
from langchain_core.example_selectors.base import BaseExampleSelector

examples = [
    {"input": "hi", "output": "ciao"},
    {"input": "bye", "output": "bye is translated into Italian as arrivederci"},
    {"input": "soccer", "output": "calcio"},
]

# 自定义模板选择器：选择与输入字符串长度相近的示例
class CustomExampleSelector(BaseExampleSelector):
    def __init__(self, examples):
        self.examples = examples

    def add_example(self, example):
        self.examples.append(example)

    def select_examples(self, input_variables):
        # 输入的元素是一个字典，键为input，value存在new_word里
        new_word = input_variables["input"]
        new_word_length = len(new_word)

        # 初始化一个变量存储最佳匹配结果，和长度差值
        best_match = None
        smallest_diff = float("inf")

        # 遍历每一个示例
        for example in self.examples:
            # 计算新单词的长度与示例列表各单词长度差
            current_diff = abs(len(example["input"]) - new_word_length)

            # 选择长度差最小的那一个
            if current_diff < smallest_diff:
                smallest_diff = current_diff
                best_match = example

        # list[dict]
        return [best_match]


example_selector: BaseExampleSelector = CustomExampleSelector(examples)
temp1 = example_selector.select_examples({"input": "okay"})
# temp1为[{'input': 'bye', 'output': 'arrivederci'}]

example_selector.add_example({"input": "hand", "output": "hand is translated into Italian mano"})
temp2 = example_selector.select_examples({"input": "okay"})
# temp2为[{'input': 'hand', 'output': 'mano'}]

from langchain_core.prompts.few_shot import FewShotPromptTemplate

example_prompt = PromptTemplate.from_template("Input: {input} -> Output: {output}")

# few-shot提示模板目标：根据输入动态选择示例，然后将示例格式化为最终提示以提供给模型
# 除下方FewShotPromptTemplate，还有FewShotChatMessagePromptTemplates
prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    suffix="Input: {input} -> Output: ",
    prefix="Translate the following words from English to Italian:",
    input_variables=["input"],
)
```

### <font color=#70AD47>Output parsers 输出解析器</font>

[How-to guides: Output Paresers](https://python.langchain.com/v0.2/docs/how_to/#output-parsers)

> [!NOTE]
>
> LangChain官方文档推荐使用function/tool的调用而不是output parsing

负责获取模型输出并将其转化为更适合下游任务的格式。LangChain支持的输出解析列表包含（机翻）：

|      名称       | 支持流传输 | 有格式说明 | 调用LLM |     输入类型      |       输出类型       |
| :-------------: | :--------: | :--------: | :-----: | :---------------: | :------------------: |
|      JSON       |     ✅      |     ✅      |         | `str`\|` Message` |     JSON object      |
|       XML       |     ✅      |     ✅      |         | `str`\|`Message`  |        `dict`        |
|       CSV       |     ✅      |     ✅      |         | `str`\|`Message`  |     `list[str]`      |
|  OutputFixing   |            |            |    ✅    | `str`\|`Message`  |                      |
| RetryWithError  |            |            |    ✅    | `str`\|`Message`  |                      |
|    Pydantic     |            |     ✅      |         | `str`\|`Message`  | `pydantic.BaseModel` |
|      YAML       |            |     ✅      |         | `str`\|`Message`  | `pydantic.BaseModel` |
| PandasDataFrame |            |     ✅      |         | `str`\|`Message`  |        `dict`        |
|      Enum       |            |     ✅      |         | `str`\|`Message`  |        `enum`        |
|    Datetime     |            |     ✅      |         | `str`\|`Message`  | `datetime.datetime`  |
|   Structured    |            |     ✅      |         | `str`\|`Message`  |   `dict[str, str]`   |

**标题行定义**

> **名称**: 解析器名称
>
> **支持流式传输**: 解析器是否支持流式传输
>
> **格式说明**: 解析器是否有格式说明。通常情况下是有的，除非 ：
>
>    - schema未指明提示，而是在其他参数中指定（如 OpenAI 函数调用）	
>
>    - 输出解析器包装了另一个输出解析器
>
> **调用LLM**: 解析器本身是否调用LLM（一般只有那些尝试纠正格式错误输出的输出解析器才会这样做）
>
> **输入类型**: 预期的输入类型。大多数为str和Message，但有些（如 OpenAI 函数）需要带有特定 kwargs 的消息
>
> **输出类型**: 解析器返回的对象的输出类型

各解析器评价及适用场景（没有场景适用就是官方文档上未标出）

|      名称       | 描述                                                         |
| :-------------: | ------------------------------------------------------------ |
|      JSON       | 返回指定的JSON对象。可指定一个Pydantic模型，它将返回该模型的JSON<br />可能是获取结构化数据最可靠的输出解析器，不使用函数调用 |
|       XML       | 返回标签字典，当需要XML输出时使用<br />适用于擅长编写XML的模型 |
|       CSV       | 返回一个逗号分隔值的列表                                     |
|  OutputFixing   | 包装另一个输出解析器。如果该输出解析器出错，则会将错误消息和错误输出传递给LLM，并要求其修复输出。 |
| RetryWithError  | 包装另一个输出解析器。如果该输出解析器出错，则会将原始输入、错误输出和错误消息传递给LLM，并要求其修复。与OutputFixingParser相比，该解析器还会发送原始指令 |
|    Pydantic     | 接受用户定义的Pydantic模型，并以该格式返回数据               |
|      YAML       | 接受用户定义的Pydantic模型，并以该格式返回数据。使用YAML进行编码 |
| PandasDataFrame | 适用于使用pandas DataFrame进行操作                           |
|      Enum       | 将响应解析为提供的枚举值之一                                 |
|    Datetime     | 将响应解析为datetime字符串                                   |
|   Structured    | 返回结构化信息的输出解析器。由于它只允许字段为字符串，因此它不如其他输出解析器强大。<br />可以在使用较小LLM的场景使用 |

### <font color=#70AD47>Chat history 聊天历史</font>

LangChain中的一个类，可以来包装任意链。ChatHistory将跟踪底层链的输入和输出，并将它们作为消息附加到消息数据库中。

### <font color=#70AD47>Document 文件</font>

使用DocumentLoader读取到数据源后，需要转换为Document对象之后才能使用

Document类有两个属性

- `page_content: str`：文件内容，通常只是一个字符串
- `matadata: dict`：与文件相关的任意元数据，能追踪到文件id，文件内容等

### <font color=#70AD47>Document loaders 文件加载器</font>

[How-to guides: Document loaders](https://python.langchain.com/v0.2/docs/how_to/#document-loaders)

从指定源进行加载数据

```python
from langchain_community.document_loaders.csv_loader import CSVLoader

file_path = ("test.csv")

loader = CSVLoader(file_path=file_path)
# data类型：list[Document]
data = loader.load()
```

### <font color=#70AD47>Text splitters 文本拆分器</font>

[How-to guides: Text splitters]([How-to guides | 🦜️🔗 LangChain](https://python.langchain.com/v0.2/docs/how_to/#text-splitters))

原因：发送给模型的文本有字符限制（超过最大token）

期望：**语义相关**文本片段放在一起

Text splitters工作方式：

> 1. 文本拆分为语义上有意义的小块（通常为句子）
> 2. 小块组成大块，直到达到一定的大小（由某些函数测量）
> 3. 达到该大小时，将该块设为自己的文本段，在创建一个具有一些重叠的新文本块（保持块之间的上下文）

Text splitter工作方式说明拆分过程有两个维度

> 1. 文本如何分割
> 2. 如何测量块大小

可以根据这两个维度自定义Text splitters

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载测试文件
with open("test.txt", 'r', encoding='utf-8') as f:
    state_of_the_union = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # 分块最大尺寸，由length_function决定
    chunk_overlap=20,  # 块间重叠。重叠分块有助于减少信息丢失
    length_function=len,  # 决定分块大小的函数
    is_separator_regex=False,  # 分隔符列表（默认为["\n\n","\n"," ",""]）是否应该解释为regex
)
texts = text_splitter.create_documents([state_of_the_union])
print(texts[0])
print(texts[1])
```

> `page_content`='分布式身份系统不同于部分去中心化数字货币系统，在分布式身份系统中不仅需要考虑身份信息的隐私性还需要考虑用户授权可溯源审计。由于分布式身份弱化第三方参与的特点，没有第三方机构能够直接掌握用户完整的身份授'
>
> 
>
> `page_content`='有第三方机构能够直接掌握用户完整的身份授权记录，这保护了用户的身份隐私，但是也导致了溯源结果没有第三方机构背书，因此需要新的技术方法来保证溯源结果可信且仅可以被具有特定权限的实体访问。此外，由于分布式'

---

### <font color=#70AD47>Embedding models 嵌入模型（阿里云文档）</font>

[基于向量检索服务与TextEmbedding实现语义搜索](https://help.aliyun.com/zh/dashscope/implementation-of-semantic-search-based-on-vector-retrieval-service-and-textembedding?spm=a2c4g.11186623.0.0.50101d61gyL4ye)

以DashScope上[通用文本向量](https://help.aliyun.com/zh/dashscope/developer-reference/text-embedding-quick-start)模型为例，通过输入一段文本，[通用文本向量](https://help.aliyun.com/zh/dashscope/developer-reference/text-embedding-quick-start)模型会将这段文本变成一个向量，将**文本变成向量**的过程叫 `Embedding`

![embedding流程](img/embedding流程.png)

- **Embedding**：通过DashScope提供的通用文本向量模型，对语料库中所有标题生成的对应的embedding向量
- **构建索引服务和查询**
  - 通过DashVector向量检索服务对生成的embedding向量构建索引
  - 将查询文本embedding向量作为输入，通过DashVector搜索相似的标题

```python
from dashscope import TextEmbedding

# 需要获取获取DASHSCOPE_API_KEY
def generate_embeddings(text):
    rsp = TextEmbedding.call(model=TextEmbedding.Models.text_embedding_v1, input=text)

    embeddings = [record['embedding'] for record in rsp.output['embeddings']]
    return embeddings if isinstance(text, list) else embeddings[0]

# 把hello字符串换为维度为1536的向量（embedding向量维数为1536）
print(len(generate_embeddings('hello')))
```

### <font color=#70AD47>通过DashVector构建检索：向量入库</font>

DashVector向量检索服务上的数据以集合（Collection）为单位存储，写入向量前应先创建一个集合来管理数据集，创建数据集的时候需要指定向量为度，因为embeddings的产生用的模型是`model=TextEmbedding.Models.text_embedding_v1`，所以维度为统一均为1536



### <font color=#70AD47>Vector stores 向量存储</font>

[DashVector x 通义千问大模型：打造基于专属知识的问答服务](img)

下图是基于中文突发事件语料库（CEC Corpus）演示关于突发时间新闻报道的知识问答

![embedding流程](img/专属知识等问答服务.png)

主要分为三个阶段

1. **本地知识库的向量化。**通过文本向量模型将其转化为高质量低纬度的向量数据，再写入DashVector向量检索服务。（数据向量化使用DashScope上的EmbeddingAPI实现）
2. **相关知识点的提取。**将提问文本向量化后，通过DashVector提取相关知识点的原文
3. **构造Prompt进行提问。**将相关知识点作为”限定上下文+提问“一起作为prompt询问通义千问

### <font color=#70AD47>Retrievers 检索器</font>



## <font color=#ED7D31>准备工作</font> 

###  <font color=#70AD47>通义</font> 

```bash
pip3 install langchain #安装langchain环境
pip3 install langchain-community #安装第三方集成,就是各种大语言模型
pip3 install python-dotenv #加载工具
pip3 install dashscope #灵积模型服务
pip3 install dashvector #灵积向量检索服务
```

### <font color=#70AD47>OpenAI</font> 

```bash
pip3 install langchain #安装langchain环境
pip3 install langchain-community #安装第三方集成,就是各种大语言模型
pip3 install langchain-openai
```

> [!TIP]
>
> 使用OpenAI的APIkey需要充值，可以尝试使用新账号，但是要验证国外的手机号，比较麻烦，本指南不使用OpenAI API key

### <font color=#70AD47>灵积服务模型</font> 

1. 创建账号并申请dashscope api key

   [DashScope 模型服务灵积/API-KEY管理](https://dashscope.console.aliyun.com/apiKey)

2. 配置环境变量

   "DASHSCOPE_API_KEY" = "sk-95exxxx"

3. 使用密钥

   ```python
   import os
   
   from dotenv import find_dotenv, load_dotenv
   
   load_dotenv(find_dotenv())
   DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]
   ```

4. 向量检索服务

   [向量检索服务DashVector (aliyun.com)](https://dashvector.console.aliyun.com/overview)

   1. 创建API-KEY

      [DashVector-API-KEY创建](https://dashvector.console.aliyun.com/api-key)

      ![DashVector_API_KEY](img\DashVector_API_KEY.PNG)

      > [!NOTE]
      >
      > DashVector-API-KEY和DASHSCOPE_API_KEY不同

   2. 创建Cluster（有免费版）

      [Cluster创建](https://common-buy.aliyun.com/?commodityCode=dashvector_vector_public_cn&regionId=cn-beijing&request={"cluster_type":"storage_type","replica":"1"})

      ![创建Cluster](img\创建Cluster.PNG)

   3. 创建Collection

      [CollectionList](https://dashvector.console.aliyun.com/cn-beijing/cluster/zydCluster/collectionList)

      ![创建Collection](img\创建Collection.PNG)

   4. 新增向量数据

   5. 进行向量查询









