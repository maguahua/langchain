import logging
from langchain_community.llms import Tongyi

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Tongyi class
tongyi_instance = Tongyi(
    api_key='your_api_key',
    model_name='model_name',
    max_retries=5,
    verbose=True
)

# Synchronous text generation
try:
    result = tongyi_instance.generate(prompt="Hello, world!")
    print("Generated text:", result)
except Exception as e:
    print("Error:", e)

# Asynchronous text generation
import asyncio


async def async_generate():
    try:
        result = await tongyi_instance.agenerate(prompt="Hello, async world!")
        print("Generated text:", result)
    except Exception as e:
        print("Error:", e)


asyncio.run(async_generate())
