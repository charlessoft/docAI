
import os
import openai
# openai.api_type = "azure"
# openai.api_base = "https://adt-openai.openai.azure.com/"
# openai.api_version = "2023-03-15-preview"
# openai.api_key = os.getenv("OPENAI_API_KEY","938ce9d50df942d08399ad736863d063")
# from config import *
#
#
# openai.api_type = "azure"
# openai.api_base = "https://adt-openai.openai.azure.com/"
# # openai.api_version = "2022-12-01"
# # openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = os.getenv("OPENAI_API_KEY", '938ce9d50df942d08399ad736863d063')
import tiktoken

openai.api_type = "azure"
openai.api_base = "https://adt-openai.openai.azure.com/"
# openai.api_version = "2022-12-01"
openai.api_version = "2023-03-15-preview"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY", '938ce9d50df942d08399ad736863d063')


engine = 'ChatGPT-0301'
# sysrole = dic['system']

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

# let's verify the function above matches the OpenAI API response

import openai

example_messages = [
    {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
    },
    {
        "role": "user",
        "content": "你是谁?请给我10个字回复.",
    },
]

for model in ["gpt-3.5-turbo-0301"]:
    print(model)
    # example token count from the function defined above
    print(f"{num_tokens_from_messages(example_messages, model)} prompt tokens counted by num_tokens_from_messages().")
    # example token count from the OpenAI API
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=example_messages,
        temperature=0,
        max_tokens=100  # we're only counting input tokens here, so let's not waste tokens on the output
    )
    print(f'{response["usage"]["prompt_tokens"]} prompt tokens counted by the OpenAI API.')
    print()
    print(response)
    print(num_tokens_from_messages([response['choices'][0]['message']],model))



# response = openai.ChatCompletion.create(
#     engine=engine,
#     # messages=messages,
#     messages=[
#         {
#             "role": "system",
#             "content": "You are an AI assistant that helps people find information."
#         },
#         {
#             "role": "user",
#             "content": "你是谁?只要回复10个字."
#         },
#     ],
#     temperature=0.7,
#     max_tokens=800,
#     top_p=0.95,
#     frequency_penalty=0,
#     presence_penalty=0,
#     stop=None)
# print(response)
