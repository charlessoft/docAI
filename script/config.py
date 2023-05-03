import os
import logging
import sys
import openai

openai.api_type = "azure"
openai.api_base = "https://adt-openai.openai.azure.com/"
openai.api_version = "2022-12-01"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY", '938ce9d50df942d08399ad736863d063')


# openai.api_type = "azure"
# openai.api_base = "https://south-central-us-openai.openai.azure.com/"
# openai.api_version = "2022-12-01"
# openai.api_key = os.getenv("OPENAI_API_KEY",'b29dfb9a036f46729740d779452bd44d')
# model='code-search-babbage-code-001'


# os.environ["OPENAI_API_KEY"] = 'YOUR_OPENAI_API_KEY'
#
# openai.api_type = "azure"
# openai.api_base = "https://adt-openai.openai.azure.com/"
# openai.api_version = "2022-12-01"
# # openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = os.getenv("OPENAI_API_KEY", '938ce9d50df942d08399ad736863d063')
#
# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_BASE"] = "https://adt-openai.openai.azure.com/"
# os.environ["OPENAI_API_KEY"] = "938ce9d50df942d08399ad736863d063"
#
# OPENAI_API_KEY = "938ce9d50df942d08399ad736863d063"
# PINECONE_API_KEY = "33e67396-4ede-4259-b084-73f5cd10098d"
# PINECONE_API_ENV = "us-east4-gcp"
#
#
# index_name = "langchain-openai"
# namespace = "gsdk"
