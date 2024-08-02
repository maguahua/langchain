from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载测试文件
with open("test.txt", 'r', encoding='utf-8') as f:
    state_of_the_union = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # 块大小
    chunk_overlap=20,  # 覆盖大小
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.create_documents([state_of_the_union])
print(texts[0])
print(texts[1])

print(text_splitter.split_text(state_of_the_union)[:2])
