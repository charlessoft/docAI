import os
import logging
import sys
from config import *
from llama_index import GPTSimpleVectorIndex

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# 加载索引
new_index = GPTSimpleVectorIndex.load_from_disk('index.json')
# 查询索引
response = new_index.query("What did the author do in 9th grade?")
# 打印答案
print(response)
