# LangChainָ��

- [LangChainָ��](#langchainָ��)
  - [LangChain��������](#langchain��������)
    - [�ܹ�������](#�ܹ���)
    - [����LangChain Expression Language(LCEL)](#����langchain-expression-languagelcel)
  - [LangChain���](#langchain���)
    - [LLMs ������ģ��](#llms-������ģ��)
    - [Chat models ����ģ��](#chat-models-����ģ��)
    - [Messages ��Ϣ](#messages-��Ϣ)
    - [Prompt templates ��ʾģ��](#prompt-templates-��ʾģ��)
      - [PromptTemplates](#prompttemplates)
      - [ChatPromptTemplates](#chatprompttemplates)
      - [MessagesPlaceholder](#messagesplaceholder)
    - [Example selectors ģ��ѡ����](#example-selectors-ģ��ѡ����)
    - [Output parsers ���������](#output-parsers-���������)
    - [Chat history ������ʷ](#chat-history-������ʷ)
    - [Document �ļ�](#document-�ļ�)
    - [Document loaders �ļ�������](#document-loaders-�ļ�������)
    - [Text splitters �ı������](#text-splitters-�ı������)
    - [Embedding models Ƕ��ģ�ͣ��������ĵ���](#embedding-models-Ƕ��ģ�Ͱ������ĵ�)
    - [ͨ��DashVector�����������������](#ͨ��dashvector���������������)
    - [Vector stores �����洢](#vector-stores-�����洢)
    - [Retrievers ������](#retrievers-������)
  - [׼������](#׼������)
    - [ͨ��](#ͨ��)
    - [OpenAI](#openai)
    - [�������ģ��](#�������ģ��)



## LangChain��������

���ڿ�����LLM������Ӧ�ó����ܣ�����LLMӦ�ó����������ڵ�ÿ���׶�

### �ܹ�������

> - `langchain-core`������һЩ���Ľӿڣ���������
> - `langchain-community`�����������ɡ�һЩ�Ƚ����еİ�����ȡ����
> 	- `langchain-openai`
>   - `langchain-anthropic`
> - `langgraph`������/״̬���ƣ��ɵ���������
> - `langserve`��ʵ����REST API��ʽ����LangChain runnables����
> - `langsmith`����غ�����LLM App���ɵ���������

### ����LangChain Expression Language(LCEL)

����ʽ��LangChain�������Ϊ�����ܷ���ش����Զ�����������Runnable��׼�ӿ�

> - `stream`����鷵����Ӧ���ݣ���Ӧ�ֶη��ͣ�
> - `invoke`���Ե����������������ȡ���
> - `batch`���Զ���������������ȡ�����һ���Դ�����Щ����

�����ӿ�Ҳ��Ӧ�첽������Ӧ��`asyncio`��`await`�﷨һ��ʹ��ʵ�ֲ���

> - `astream`��
> - `ainvoke`��
> - `abatch`��
> - `astream_log`���첽��鷵���м䲽���������Ӧ���ڴ�������п�ʵʱ��ȡ�м䲽������
> - `astream_events`���첽��鷵�����е��¼���langchain-core 0.1.14������beta�棩

input type��output type��Ϊ�����ͬ����ͬ

|     ���     |                      ��������                       |       �������        |
| :----------: | :-------------------------------------------------: | :-------------------: |
|    Prompt    |                     Dictionary                      |      PromptValue      |
|  ChatModel   | Single string,list ofchat messages or a PromptValue |      ChatMessage      |
|     LLM      | Single string,list ofchat messages or a PromptValue |        String         |
| OutputParser |          The output of an LLM or ChatModel          | Depends on the parser |
|  Retriever   |                    Single string                    |   List of Documents   |
|     Tool     | Single string or dictionary, depending on the tool  |  Depends on the tool  |

���е�runnable���ᱩ¶`input`��`output`�����Ա���

- `input_schema`������Runnable�ṹ�Զ����ɵ�`input`Pydanticģ��
- `output_schema`������Runnable�ṹ�Զ����ɵ�`output`Pydanticģ��

## LangChain���

> [!IMPORTANT]
>
> ������Ϊ�����Ը���ָ�ϣ����������ͻ������룬�г��˹ٷ��ĵ������ʹ�÷����������в���

### LLMs ������ģ��

[How-to guides: LLMs](https://python.langchain.com/v0.2/docs/how_to/#llms)

LLMs�Ǵ�ͳ�ϱȽϾɵ�ģ�ͣ�����ͨ����Chat models�������ַ�����Ϊ���벢�����ַ���

LangChain������Щģ�ͽ�Messages��Ϊ���룬��Щ���뽫��LangChain wrappers��ʽ��Ϊһ���ַ�����Ȼ���ٱ������ײ�ģ��

### Chat models ����ģ��

[How-to guides: Chat models](https://python.langchain.com/v0.2/docs/how_to/#chat-models)

��Ϣ��Ϊ�������������Ǵ��ı���������ģ�ͣ��������ַ�����Ϊ������Ϊ`HumanMessage`���ݸ��ײ�ģ��

**һЩ��׼����**

> - `model`��ģ����
> - `temperature`��0-1֮�䣬����Խ��llm�Ĵ�����Խǿ��Խ����ȷ��
> - `timeout`������ʱʱ��
> - `max_tokens`����������tokens
> - `stop`��Ĭ��ֹͣ����
> - `max_retries`����������������
> - `api_key`��ģ���ṩ��API��Կ����DASHSCOPE_API_KEY��OPEN_API_KEY��
> - `base_url`����������Ķ˵�

> [!NOTE]
>
> - �������е�ģ���ж�����ȫ����׼������û�б������ı�׼�������ܱ�ʹ��
> - ��׼����ֻ����Щ���Լ����ɰ��ļ�����ǿ��ִ�У�langchain-openai�ȣ�����langchain-community�б�׼��������ǿ��ִ��
> - ���ڶ�ģ̬ģ�ͣ����䲻��������˻�û�б�׼�������API

LangChain���й��κ�Chat models��LLMs��������������������

### Messages ��Ϣ

һЩģ�ͽ���Ϣ�б���Ϊ���룬������һ����Ϣ����ͬ���͵���Ϣ������

> - `role`:˭�ύ����Ϣ��LangChain��Բ�ͬ��role�в�ͬ����Ϣ��
> - `content`:��Ϣ���ݣ�һ���ַ����������ģ�ʹ����������ݣ���һ���ֵ��б����ڶ�ģ̬���룩
> - `response_metadata`:�����й���Ӧ�ĸ���Ԫ���ݣ�һ�㶼��ģ���е�ר�����ݣ����ܻ�洢��־�����tokensʹ���������Ϣ

Message��Ҫ��Ϊ���¼��ࣨ�������������ԣ�

> - `HumanMessage`���û�������Ϣ
>- `AIMessage`��ģ����Ϣ
>   - ` tool_calls`��AIMessage�����һ���֣�����ͨ��`.tool_calls`������
>    - `name`��������
>     - `args`������args
>     - ` id`�� tool call��id
> - `SystemMessage`��һ��ϵͳ��Ϣ������ģ����ô��������ÿ��ģ�Ͷ�֧�֣�
> - `ToolMessage`��tool call֮��Ľ��
>   - `tool_call_id`�����ڴ��ݲ����˽����tool call��id
>  - `artifact`�����ڴ��ݹ���ִ�й����е����⹤�ߣ��Ը������ã������͵�ģ���У�
> - `FunctionMessage`��ToolMesage�ĵľɰ棬������OpenAI�ľɰ溯������API

### Prompt templates ��ʾģ�� 

[How-to guides: Prompt templates](https://python.langchain.com/v0.2/docs/how_to/#prompt-templates)

ͨ��˵��prompt��������ChatGPT����ʱ���û����������������֣�**������ָ��**��

- ����Ϊ�ֵ䣬ÿ����������ʾģ����Ҫ��д�ı���
- ���Ϊ`PromptValue`������ת��ΪLLM��ChatModel��Ҳ����ת��Ϊ�ַ�������Ϣ�б������ַ�������Ϣ֮�������ת����

#### PromptTemplates

���ڸ�ʽ������**�ַ���**��ͨ�����ڱȽϼ򵥵����롣�����ʹ��PromptTemplate�ĳ�������

```python
from langchain.prompts import PromptTemplate

# from_template����ֵΪPromptValue
prompt = PromptTemplate.from_template("tell me a joke about {topic}")

# chain������ΪRunnableSerializable
chain = prompt | model
res = chain.invoke({"topic": "cats"})
print(res)
```

> [!NOTE]
>
> 1. DASHSCOPE_API_KEY�Ĵ�����ʹ����[׼������](#׼������)�����������´��뽫ʡ�Ի�ȡAPI key���ִ���
> 2. ģ�͵ĵ��÷���Ĭ��Ϊ���Ϸ���

#### ChatPromptTemplates

Ϊ**Chat models**������ʾģ�塪��һ��������Ϣ�б��б��е�ÿһ����Ϣ����һ����ݣ�����ϵͳ���û���AI

```python
from langchain.prompts import ChatPromptTemplate

# ChatPromptTemplate����ʱ�ṹ��������Ϣ��SystemMessage��HumanMessage
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant"),
        ("user", "tell me a joke about {topic}")
    ]
)
```

#### MessagesPlaceholder

����봫��һ��message�б�����������ض�λ�ã�����ʹ��MessagesPlaceholder

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

res = chain.invoke({"msgs": [HumanMessage(content="hi!")]})
```

### Example selectors ģ��ѡ����

[How-to guides: Example selectors](https://python.langchain.com/v0.2/docs/how_to/#example-selectors)

Ϊ�������ģ�͵����ܣ������ķ����ǽ�ʾ����������ʾ�С�Example selectors���Ǹ���ѡ����Щʾ���������Ǹ�ʽ������ʾ�еĹ����࣬һ�������·���

> 1. Ӳ���룺ֱ������ʾ��д��̶���ʾ��
> 2. ��̬ѡ��ʾ�������ݾ��������̬ѡ����ʵ�ʾ��

������δ����У� �����䷭��һ������Ϊ3�ĵ��ʣ�output����"xxx is translated into Italian as xxx."������䷭��һ������Ϊ4�Ĵ��룬outputֻ�з���������Ϊexamples���г��˳��Ȳ�ͬӦ��λظ���ʾ��

```python
from langchain_core.example_selectors.base import BaseExampleSelector

examples = [
    {"input": "hi", "output": "ciao"},
    {"input": "bye", "output": "bye is translated into Italian as arrivederci"},
    {"input": "soccer", "output": "calcio"},
]

# �Զ���ģ��ѡ������ѡ���������ַ������������ʾ��
class CustomExampleSelector(BaseExampleSelector):
    def __init__(self, examples):
        self.examples = examples

    def add_example(self, example):
        self.examples.append(example)

    def select_examples(self, input_variables):
        # �����Ԫ����һ���ֵ䣬��Ϊinput��value����new_word��
        new_word = input_variables["input"]
        new_word_length = len(new_word)

        # ��ʼ��һ�������洢���ƥ�������ͳ��Ȳ�ֵ
        best_match = None
        smallest_diff = float("inf")

        # ����ÿһ��ʾ��
        for example in self.examples:
            # �����µ��ʵĳ�����ʾ���б�����ʳ��Ȳ�
            current_diff = abs(len(example["input"]) - new_word_length)

            # ѡ�񳤶Ȳ���С����һ��
            if current_diff < smallest_diff:
                smallest_diff = current_diff
                best_match = example

        # list[dict]
        return [best_match]


example_selector: BaseExampleSelector = CustomExampleSelector(examples)
temp1 = example_selector.select_examples({"input": "okay"})
# temp1Ϊ[{'input': 'bye', 'output': 'arrivederci'}]

example_selector.add_example({"input": "hand", "output": "hand is translated into Italian mano"})
temp2 = example_selector.select_examples({"input": "okay"})
# temp2Ϊ[{'input': 'hand', 'output': 'mano'}]

from langchain_core.prompts.few_shot import FewShotPromptTemplate

example_prompt = PromptTemplate.from_template("Input: {input} -> Output: {output}")

# few-shot��ʾģ��Ŀ�꣺�������붯̬ѡ��ʾ����Ȼ��ʾ����ʽ��Ϊ������ʾ���ṩ��ģ��
# ���·�FewShotPromptTemplate������FewShotChatMessagePromptTemplates
prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    suffix="Input: {input} -> Output: ",
    prefix="Translate the following words from English to Italian:",
    input_variables=["input"],
)
```

### Output parsers ���������

[How-to guides: Output Paresers](https://python.langchain.com/v0.2/docs/how_to/#output-parsers)

> [!NOTE]
>
> LangChain�ٷ��ĵ��Ƽ�ʹ��function/tool�ĵ��ö�����output parsing

�����ȡģ�����������ת��Ϊ���ʺ���������ĸ�ʽ��LangChain֧�ֵ���������б��������������

| ����            | ֧�������� | �и�ʽ˵�� | ����LLM | ��������       | �������           |
| :---------------: | :----------: | :----------: | :-------: | :--------------: | :------------------: |
| JSON            | ��          | ��         |         | `str`\|` Message` | JSON object     |
| XML             | ��         | ��         |         | `str`\|`Message` | `dict`             |
| CSV             | ��         | ��         |         | `str`\|`Message` | `list[str]`        |
| OutputFixing    |            |            | ��      | `str`\|`Message` |                    |
| RetryWithError  |            |            | ��      | `str`\|`Message` |                    |
| Pydantic        |            | ��         |         | `str`\|`Message` | `pydantic.BaseModel` |
| YAML            |            | ��         |         | `str`\|`Message` | `pydantic.BaseModel` |
| PandasDataFrame |            | ��         |         | `str`\|`Message` | `dict`             |
| Enum            |            | ��         |         | `str`\|`Message` | `enum`             |
| Datetime        |            | ��         |         | `str`\|`Message` | `datetime.datetime` |
| Structured      |            | ��         |         | `str`\|`Message` | `dict[str, str]` |

**�����ж���**

> **����**: ����������
>
> **֧����ʽ����**: �������Ƿ�֧����ʽ����
>
> **��ʽ˵��**: �������Ƿ��и�ʽ˵����ͨ����������еģ����� ��
>
>    - schemaδָ����ʾ������������������ָ������ OpenAI �������ã�	
>
>    - �����������װ����һ�����������
>
> **����LLM**: �����������Ƿ����LLM��һ��ֻ����Щ���Ծ�����ʽ�������������������Ż���������
>
> **��������**: Ԥ�ڵ��������͡������Ϊstr��Message������Щ���� OpenAI ��������Ҫ�����ض� kwargs ����Ϣ
>
> **�������**: ���������صĶ�����������

�����������ۼ����ó�����û�г������þ��ǹٷ��ĵ���δ�����

|      ����       | ����                                                         |
| :-------------: | ------------------------------------------------------------ |
|      JSON       | ����ָ����JSON���󡣿�ָ��һ��Pydanticģ�ͣ��������ظ�ģ�͵�JSON<br />�����ǻ�ȡ�ṹ��������ɿ����������������ʹ�ú������� |
|       XML       | ���ر�ǩ�ֵ䣬����ҪXML���ʱʹ��<br />�������ó���дXML��ģ�� |
|       CSV       | ����һ�����ŷָ�ֵ���б�                                     |
|  OutputFixing   | ��װ��һ���������������������������������Ὣ������Ϣ�ʹ���������ݸ�LLM����Ҫ�����޸������ |
| RetryWithError  | ��װ��һ���������������������������������Ὣԭʼ���롢��������ʹ�����Ϣ���ݸ�LLM����Ҫ�����޸�����OutputFixingParser��ȣ��ý��������ᷢ��ԭʼָ�� |
|    Pydantic     | �����û������Pydanticģ�ͣ����Ըø�ʽ��������               |
|      YAML       | �����û������Pydanticģ�ͣ����Ըø�ʽ�������ݡ�ʹ��YAML���б��� |
| PandasDataFrame | ������ʹ��pandas DataFrame���в���                           |
|      Enum       | ����Ӧ����Ϊ�ṩ��ö��ֵ֮һ                                 |
|    Datetime     | ����Ӧ����Ϊdatetime�ַ���                                   |
|   Structured    | ���ؽṹ����Ϣ�������������������ֻ�����ֶ�Ϊ�ַ���������������������������ǿ��<br />������ʹ�ý�СLLM�ĳ���ʹ�� |

### Chat history ������ʷ

LangChain�е�һ���࣬��������װ��������ChatHistory�����ٵײ�������������������������Ϊ��Ϣ���ӵ���Ϣ���ݿ��С�
### Document �ļ�

ʹ��DocumentLoader��ȡ������Դ����Ҫת��ΪDocument����֮�����ʹ��

Document������������

- `page_content: str`���ļ����ݣ�ͨ��ֻ��һ���ַ���
- `matadata: dict`�����ļ���ص�����Ԫ���ݣ���׷�ٵ��ļ�id���ļ����ݵ�

### Document loaders �ļ�������

[How-to guides: Document loaders](https://python.langchain.com/v0.2/docs/how_to/#document-loaders)

��ָ��Դ���м�������

```python
from langchain_community.document_loaders.csv_loader import CSVLoader

file_path = ("test.csv")

loader = CSVLoader(file_path=file_path)
# data���ͣ�list[Document]
data = loader.load()
```

### Text splitters �ı������

[How-to guides: Text splitters](https://python.langchain.com/v0.2/docs/how_to/#text-splitters)

ԭ�򣺷��͸�ģ�͵��ı����ַ����ƣ��������token��

������**�������**�ı�Ƭ�η���һ��

Text splitters������ʽ��

> 1. �ı����Ϊ�������������С�飨ͨ��Ϊ���ӣ�
> 2. С����ɴ�飬ֱ���ﵽһ���Ĵ�С����ĳЩ����������
> 3. �ﵽ�ô�Сʱ�����ÿ���Ϊ�Լ����ı��Σ��ڴ���һ������һЩ�ص������ı��飨���ֿ�֮��������ģ�

Text splitter������ʽ˵����ֹ���������ά��

> 1. �ı���ηָ�
> 2. ��β������С

���Ը���������ά���Զ���Text splitters

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ���ز����ļ�
with open("test.txt", 'r', encoding='utf-8') as f:
    state_of_the_union = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # �ֿ����ߴ磬��length_function����
    chunk_overlap=20,  # ����ص����ص��ֿ������ڼ�����Ϣ��ʧ
    length_function=len,  # �����ֿ��С�ĺ���
    is_separator_regex=False,  # �ָ����б�Ĭ��Ϊ["\n\n","\n"," ",""]���Ƿ�Ӧ�ý���Ϊregex
)
texts = text_splitter.create_documents([state_of_the_union])
print(texts[0])
print(texts[1])
```

> `page_content`='�ֲ�ʽ���ϵͳ��ͬ�ڲ���ȥ���Ļ����ֻ���ϵͳ���ڷֲ�ʽ���ϵͳ�в�����Ҫ���������Ϣ����˽�Ի���Ҫ�����û���Ȩ����Դ��ơ����ڷֲ�ʽ�������������������ص㣬û�е����������ܹ�ֱ�������û������������'
>
> 
>
> `page_content`='�е����������ܹ�ֱ�������û������������Ȩ��¼���Ᵽ�����û��������˽������Ҳ��������Դ���û�е������������飬�����Ҫ�µļ�����������֤��Դ��������ҽ����Ա������ض�Ȩ�޵�ʵ����ʡ����⣬���ڷֲ�ʽ'

---

### Embedding models Ƕ��ģ�ͣ��������ĵ���

[������������������TextEmbeddingʵ����������](https://help.aliyun.com/zh/dashscope/implementation-of-semantic-search-based-on-vector-retrieval-service-and-textembedding?spm=a2c4g.11186623.0.0.50101d61gyL4ye)

��DashScope��[ͨ���ı�����](https://help.aliyun.com/zh/dashscope/developer-reference/text-embedding-quick-start)ģ��Ϊ����ͨ������һ���ı���[ͨ���ı�����](https://help.aliyun.com/zh/dashscope/developer-reference/text-embedding-quick-start)ģ�ͻὫ����ı����һ����������**�ı��������**�Ĺ��̽� `Embedding`

<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="img/embedding����.png">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">embedding����</div>
</center>



- **Embedding**��ͨ��DashScope�ṩ��ͨ���ı�����ģ�ͣ������Ͽ������б������ɵĶ�Ӧ��embedding����
- **������������Ͳ�ѯ**
  - ͨ��DashVector����������������ɵ�embedding������������
  - ����ѯ�ı�embedding������Ϊ���룬ͨ��DashVector�������Ƶı���

```python
from dashscope import TextEmbedding

# ��Ҫ��ȡ��ȡDASHSCOPE_API_KEY
def generate_embeddings(text):
    rsp = TextEmbedding.call(model=TextEmbedding.Models.text_embedding_v1, input=text)

    embeddings = [record['embedding'] for record in rsp.output['embeddings']]
    return embeddings if isinstance(text, list) else embeddings[0]

# ��hello�ַ�����Ϊά��Ϊ1536��������embedding����ά��Ϊ1536��
print(len(generate_embeddings('hello')))
```

### ͨ��DashVector�����������������

DashVector�������������ϵ������Լ��ϣ�Collection��Ϊ��λ�洢��д������ǰӦ�ȴ���һ���������������ݼ����������ݼ���ʱ����Ҫָ������Ϊ�ȣ���Ϊembeddings�Ĳ����õ�ģ����`model=TextEmbedding.Models.text_embedding_v1`������ά��Ϊͳһ��Ϊ1536



### Vector stores �����洢

[DashVector x ͨ��ǧ�ʴ�ģ�ͣ��������ר��֪ʶ���ʴ����](img)

��ͼ�ǻ�������ͻ���¼����Ͽ⣨CEC Corpus����ʾ����ͻ��ʱ�����ű�����֪ʶ�ʴ�

<center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="img/ר��֪ʶ���ʴ����.png">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">ר��֪ʶ���ʴ����</div>
</center>

��Ҫ��Ϊ�����׶�

1. **����֪ʶ�����������**ͨ���ı�����ģ�ͽ���ת��Ϊ��������γ�ȵ��������ݣ���д��DashVector�����������񡣣�����������ʹ��DashScope�ϵ�EmbeddingAPIʵ�֣�
2. **���֪ʶ�����ȡ��**�������ı���������ͨ��DashVector��ȡ���֪ʶ���ԭ��
3. **����Prompt�������ʡ�**�����֪ʶ����Ϊ���޶�������+���ʡ�һ����Ϊpromptѯ��ͨ��ǧ��

### Retrievers ������



## ׼������

###  ͨ��

```bash
pip3 install langchain #��װlangchain����
pip3 install langchain-community #��װ����������,���Ǹ��ִ�����ģ��
pip3 install python-dotenv #���ع���
pip3?install?dashscope #���ģ�ͷ���
pip3 install dashvector #���������������
```

### OpenAI

```bash
pip3 install langchain #��װlangchain����
pip3 install langchain-community #��װ����������,���Ǹ��ִ�����ģ��
pip3 install langchain-openai
```

> [!TIP]
>
> ʹ��OpenAI��APIkey��Ҫ��ֵ�����Գ���ʹ�����˺ţ�����Ҫ��֤������ֻ��ţ��Ƚ��鷳����ָ�ϲ�ʹ��OpenAI API key

### �������ģ��

1. �����˺Ų�����dashscope api key

   [DashScope ģ�ͷ������/API-KEY����](https://dashscope.console.aliyun.com/apiKey)

2. ���û�������

   ����Ŀ��Ŀ¼����.env�ļ���������дAPI Key����ʽΪ

   ```html
   <XXX_API_KEY>=<sk-xxxxxxxxx>
   �磺
   DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxx
   ```

3. ʹ����Կ

   ```python
   import os
   from dotenv import load_dotenv
   # ֻҪ��.env�����ù���ֻ��ģ�鼶����� load_dotenv()������ڴ�����ģ�Ͷ���ʱ�Զ�ʶ��
   load_dotenv()
   # ��ʱ��ʶ��DASHSCOPE_API_KEY
   model = Tongyi(temperature=1)
   ```

4. ������������

   [������������DashVector (aliyun.com)](https://dashvector.console.aliyun.com/overview)

   1. ����API-KEY

      [DashVector-API-KEY����](https://dashvector.console.aliyun.com/api-key)

      <center>
          <img style="border-radius: 0.3125em;
          box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
          src="img\DashVector_API_KEY.png">
          <br>
          <div style="color:orange; border-bottom: 1px solid #d9d9d9;
          display: inline-block;
          color: #999;
          padding: 2px;">����DASHSCOPE_API_KEY</div>
      </center>
   
      > [!NOTE]
      >
      > DashVector-API-KEY��DASHSCOPE_API_KEY��ͬ
   
   2. ����Cluster������Ѱ棩
   
      [Cluster����](https://common-buy.aliyun.com/?commodityCode=dashvector_vector_public_cn&regionId=cn-beijing&request={"cluster_type":"storage_type","replica":"1"})
   
      <center>
          <img style="border-radius: 0.3125em;
          box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
          src="img\����Cluster.png">
          <br>
          <div style="color:orange; border-bottom: 1px solid #d9d9d9;
          display: inline-block;
          color: #999;
          padding: 2px;">����cluster</div>
      </center>
   
   3. ����Collection
   
      <center>
          <img style="border-radius: 0.3125em;
          box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
          src="img\����Collection.png">
          <br>
          <div style="color:orange; border-bottom: 1px solid #d9d9d9;
          display: inline-block;
          color: #999;
          padding: 2px;">����collection</div>
      </center>
      
   4. ������������
   
      ```python
      import json
      
      # ׼������
      # ���룺path���ļ�·����size��ÿ��batch�Ĵ�С
      # �����ÿ�ε�������һ������ָ����С�ĵ����б�
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
      
      # embedding����
      # ���룺�ı��ַ������ַ����б�
      # ����������ı����ı��б��Ӧ������
      def generate_embeddings(text):
          rsp = TextEmbedding.call(model=TextEmbedding.Models.text_embedding_v1, input=text)
      
          embeddings = [record['embedding'] for record in rsp.output['embeddings']]
          return embeddings if isinstance(text, list) else embeddings[0]
      
      from dashvector import Client, Doc
      
      # ��ʼ�� DashVector client
      # DashVector API KEY��Cluster��endpoint
      client = Client(
          api_key='sk-QC9.....',
          endpoint='vrs-cn-fou.....'
      )
      
      # ָ���������ƺ�����ά��
      existing_collections = client.list()
      
      # �ж���������Ƿ��Ѿ�������Collection
      if 'your_collection' not in existing_collections:
          print("your_collection does not exist, creating it...")
          rsp = client.create('your_collection', 1536)
          assert rsp
      else:
          print("your_collection already exists.")
      
      # ��ȡ����
      collection = client.get('your_collection')
      assert collection
      
      batch_size = 10
      for docs in list(prepare_data('your_data', batch_size)):
          # ���� embedding
          embeddings = generate_embeddings([doc['title'] for doc in docs])
      
          # ����д������
          rsp = collection.insert(
              [
                  Doc(id=str(doc['id']), vector=embedding, fields={"title": doc['title']})
                  for doc, embedding in zip(docs, embeddings)
              ]
          )
          print("Response from insert:", rsp)
          assert rsp
      
      # ����������������������
      rsp = collection.query(generate_embeddings('Ӧ���� ��Ƹ'), output_fields=['title'])
      print("Response from query:", rsp)
      
      for doc in rsp.output:
          print(f"id: {doc.id}, title: {doc.fields['title']}, score: {doc.score}")
      ```
   
   5. ����������ѯ
   
      ```python
      import os
      
      import dashscope
      from dashscope import TextEmbedding
      
      from dashvector import Client, Doc
      
      # ������������һ��
      def prepare_data(path, batch_size=25)
      def generate_embeddings(news)
      
      
      if __name__ == '__main__':
          dashscope.api_key = '{sk-95exxx}'
      
          # ��ʼ�� dashvector client
          client = Client(
              api_key='sk-QC9.....',
          	endpoint='vrs-cn-fou.....'
          )
      
          # �������ϣ�ָ���������ƺ�����ά��, text_embedding_v1 ģ�Ͳ���������ͳһΪ 1536 ά
          rsp = client.create('your_collection', 1536)
          assert rsp
      
          # ��������
          id = 0
          collection = client.get('your_collection')
          for news in list(prepare_data('your_data')):
              ids = [id + i for i, _ in enumerate(news)]
              id += len(news)
      
              vectors = generate_embeddings(news)
              # д�� dashvector ��������
              rsp = collection.upsert(
                  [
                      Doc(id=str(id), vector=vector, fields={"raw": doc})
                      for id, vector, doc in zip(ids, vectors, news)
                  ]
              )
              assert rsp
      ```
   
      > [!NOTE]
      >
      > ��ѵ�Cluster�����洢������10w������������ִ洢ʱ�ᱨ�����������ʹ��train.json��һ������������뷶�������׼ȷ�����������͡�
      >
      > [����״̬��˵��](https://help.aliyun.com/document_detail/2510266.html?spm=5176.28371440.help.dexternal.682666d7FmUoHB)
      
      <center>
          <img style="border-radius: 0.3125em;
          box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
          src="img\��collection�в��������ķ���ֵ.png">
          <br>
          <div style="color:orange; border-bottom: 1px solid #d9d9d9;
          display: inline-block;
          color: #999;
          padding: 2px;">��collection�в��������ķ���ֵ</div>
      </center>



