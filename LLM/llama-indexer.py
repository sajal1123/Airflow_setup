import os
from llama_index.llms import Replicate
from llama_index import set_global_tokenizer
from transformers import AutoTokenizer
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import ServiceContext
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import json

# Read the constants from the JSON file
with open('../config.json') as f:
    constants = json.load(f)

os.environ["REPLICATE_API_TOKEN"] = constants["REPLICATE_API_TOKEN"]


llama2_7b_chat = constants["llama_chat_model"]
llm = Replicate(
    model=llama2_7b_chat,
    temperature=0.75,
    additional_kwargs={"top_p": 0.5,
                       "max_new_tokens": 10000000, 
                       "system_prompt": "You are a reporter that provides summaries of the last day's events."},
)

print("set tokenizer to match LLM...")


set_global_tokenizer(
    AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode
)

print("global tokenizer set!!!")

hf_model_name = constants["hf_embedding_model"]
embed_model = HuggingFaceEmbedding(model_name=hf_model_name)
service_context = ServiceContext.from_defaults(
    llm=llm, embed_model=embed_model
)
# print("service context created\n\n", service_context)


print('creating index...')

documents = SimpleDirectoryReader("data").load_data()

index = VectorStoreIndex.from_documents(
    documents,
    service_context=service_context
)
print("start of index : ", index[:100])
print("asking query...")

query_engine = index.as_query_engine(similarity_top_k=5, streaming=True)

summary = query_engine.query("Based on the provided data, write a 2500-2700 word long article of all the major news events of the past day. \
    Break your report down in the following sections: Technology, Politics, International news, Sports, and the Stock Market.\
    Mention relevant information (like names, dates, and other information)in your write up.\
    Do not say phrases like 'Based on the given data', 'According to the given information', etc. to start.\
    Talk about the topic directly.")

stocks = query_engine.query("Tell me about the stock market. Is it a good time to invest?")

print("\n\n\nSUMMARY OF THE DAY\n\n\n")
summary.print_response_stream()

print("\n\nSTOCKS\n\n", stocks)

stanford = query_engine.query("Was there any news about India?")
print("\n\India\n\n", stanford)
