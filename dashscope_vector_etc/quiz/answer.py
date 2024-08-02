from dashscope import Generation


def answer_question(question, context):
    prompt = f'''请基于```内的内容回答问题。"
	```
	{context}
	```
	我的问题是：{question}。
    '''

    rsp = Generation.call(model='qwen-turbo', prompt=prompt)
    return rsp.output.text
