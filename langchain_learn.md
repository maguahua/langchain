# LangChain指南

[toc]

## <font color=#ED7D31>LangChain基本概念</font> 

用于开发由LLM驱动的应用程序框架，简化了LLM应用程序生命周期的每个阶段

### <font color=#70AD47>架构（包）</font> 

```markdown
- langchain-core：定义一些核心接口（轻量级）
- langchain-community：第三方集成。一些比较流行的包被提取出来
	- langchain-openai
	- langchain-anthropic
- langgraph：流程/状态控制（可单独工作）
- langserve：实现以REST API形式部署LangChain runnables和链
- langsmith：监控和评估LLM App（可单独工作）
```

### <font color=#70AD47>关于LangChain Expression Language(LCEL)</font> 

声明式的LangChain组件链，为尽可能方便地创建自定义链，运用Runnable标准接口

```markdown
- stream：逐块返回相应内容（响应分段发送）
- invoke：对单个输入调用链并获取结果
- batch：对多个输入调用链并获取结果，一次性处理这些输入
```

上述接口也对应异步方法，应与`asyncio`的`await`语法一起使用实现并发

```markdown
- astream：
- ainvoke：
- abatch：
- astream_log：异步逐块返回中间步骤和最终响应（在处理过程中可实时获取中间步骤结果）
- astream_events：异步逐块返回链中的事件（langchain-core 0.1.14中引入beta版）
```

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

### <font color=#70AD47>Chat models 聊天模型</font> 

**一些标准参数**

```markdown
- model：模型名
- temperature：0-1之间，数字越大，llm的创造力越强（越不精确）
- timeout：请求超时时间
- max_tokens：最大可生成tokens
- stop：默认停止序列
- max_retries：最大重新请求次数
- api_key：模型提供者API密钥（如DASHSCOPE_API_KEY，OPEN_API_KEY）
- base_url：发送请求的端点
```

这些接口标准在`langchain-community`中不强制

> [!NOTE]
>
> - 目前input都用ChatModel，`string`类型作为input比较古早
> - 对于多模态模型，因其不常见，因此还没有标准化定义的API

### <font color=#70AD47>LLMs(Large Language Models)</font> 

LangChain不托管任何LLM，而是依赖第三方集成。

### <font color=#70AD47>Messages</font>

一些LM将消息列表作为输入，并返回一条消息。不同类型的消息都包含

```markdown
- role:谁提交的信息，LangChain针对不同的role有不同的消息类
- content:信息内容，一个字符串（大多数模型处理这种内容）；一个字典列表（用于多模态输入）
```

Message主要分为以下几类（仅包含特殊属性）

> `HumanMessage`：用户输入信息
>
> `AIMessage`：模型信息
>
> - `response_metadata`：包含有关响应的附加元数据，一般都是模型中的专用数据，> 可能会存储日志问题和tokens使用情况等信息
> - ` tool_calls`：AIMessage输出的一部分，可以通过`.tool_calls`来访问
>   - `name`：工具名
>   - `args`：工具args
>   - ` id`： tool call的id
>
> `SystemMessage`：一条系统消息，告诉模型怎么做（不是每个模型都支持）
>
> `ToolMessage`：tool call之后的结果，除了`role`和`content`属性还有
>
> - `tool_call_id`：用于传递产生此结果的tool call的id
> - `artifact`：用于传递工具执行过程中的任意工具（对跟踪有用，不发送到模型中）
>
> `FunctionMessage`(Legacy)：旧版消息类型，适用于OpenAI的旧版函数调用API（新版是`ToolMessage`，适用于更新的工具调用API）

### <font color=#70AD47>Prompt template 提示模板</font> 

通俗说，prompt就是在与ChatGPT聊天时，用户在聊天框输入的文字（**指令**）

- 输入为字典，每个键代表提示模板中要填写的变量
- 输出为**PromptValue**，可以转换为LLM或ChatModel，也可以转换为字符串或消息列表（便于字符串和消息之间的类型转换）

#### String PromptTemplates

用于格式化单个字符串，通常用于比较简单的输入。构造和使用PromptTemplate的常见方法

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

用以格式化信息列表，将一些模板构建成一个整体

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

[How-to guide: Example selectors](https://python.langchain.com/v0.2/docs/how_to/#example-selectors)

Example selectors负责选择正确的few-shot example传递给prompt

### <font color=#70AD47>Output parsers 输出解析器</font>

[How-to guides: Output Paresers](https://python.langchain.com/v0.2/docs/how_to/#output-parsers)



> [!NOTE]
>
> LangChain官方文档推荐使用function/tool的调用而不是output parsing

负责获取模型输出并将其转化为更适合下游任务的格式。LangChain支持的输出解析列表包含（机翻）：

| 名称            | 支持流传输 | 有格式说明 | 调用LLM |         输入类型          |     输出类型      |
| :---------------: | :----------: | :----------: | :-------: |:---------------------:|:-------------:|
| JSON            | ✅          | ✅          |         | str     or    Message | JSON object     |
| XML             | ✅          | ✅          |         |  str or     Message   | dict               |
| CSV             | ✅          | ✅          |         |  str or      Message  | List[str]          |
| OutputFixing    |            |            | ✅       |   str or    Message   |                    |
| RetryWithError  |            |            | ✅       |   str or    Message   |                    |
| Pydantic        |            | ✅          |         |   str or   Message    | pydantic.BaseModel |
| YAML            |            | ✅          |         |   str or   Message    | pydantic.BaseModel |
| PandasDataFrame |            | ✅          |         |   str or    Message   | dict               |
| Enum            |            | ✅          |         |   str or    Message   | Enum               |
| Datetime        |            | ✅          |         |   str or    Message   | datetime.datetime  |
| Structured      |            | ✅          |         |   str or    Message   | Dict[str, str]  |

**标题行定义**

1. **名称**: 解析器名称

2. **支持流式传输**: 解析器是否支持流式传输

3. **格式说明**: 解析器是否有格式说明。通常情况下是有的，除非 ：

   - schema未指明提示，而是在其他参数中指定（如 OpenAI 函数调用）	

   - 输出解析器包装了另一个输出解析器

4. **调用LLM**: 解析器本身是否调用LLM（一般只有那些尝试纠正格式错误输出的输出解析器才会这样做）

5. **输入类型**: 预期的输入类型。大多数为str和Message，但有些（如 OpenAI 函数）需要带有特定 kwargs 的消息

6. **输出类型**: 解析器返回的对象的输出类型

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

从指定源进行加载数据

## <font color=#ED7D31>准备工作</font> 

###  <font color=#70AD47>通义</font> 

```python
pip3 install langchain #安装langchain环境
pip3 install langchain-community #安装第三方集成,就是各种大语言模型
pip3 install python-dotenv #加载工具
pip3 install dashscope #灵积模型服务
```

### <font color=#70AD47>OpenAI</font> 

```python
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

   

   

   

   



