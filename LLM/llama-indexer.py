import os
from llama_index.llms import Replicate
from llama_index import set_global_tokenizer
from transformers import AutoTokenizer
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import ServiceContext
from llama_index import VectorStoreIndex, SimpleDirectoryReader

os.environ["REPLICATE_API_TOKEN"] = "r8_BOalg4ka8u21B7pF6DPcoRlxVfoKAHD3H7a8z"


llama2_7b_chat = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"
llm = Replicate(
    model=llama2_7b_chat,
    temperature=0.75,
    additional_kwargs={"top_p": 0.5,
                       "max_new_tokens": 10000000, 
                       "system_prompt": "You are a reporter that provides crisp summaries of the last day's events in 2500 to 2700 words."},
)

print("set tokenizer to match LLM...")


set_global_tokenizer(
    AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode
)

print("global tokenizer set!!!")


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
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

print("asking query...")

query_engine = index.as_query_engine(similarity_top_k=5, streaming=True)
# response1 = query_engine.query("Who is the greatest footballer ever?")
# response2 = query_engine.query("How many Ballon d'Ors does Messi have?")
# response3 = query_engine.query("What did Ron de Santis do?")
# response4 = query_engine.query("Was there any sports news?")
# response5 = query_engine.query("How's the weather in Kansas City?")
# response6 = query_engine.query("Tell me about the Ram Temple in Ayodhya")

summary = query_engine.query("Based on the provided data, write a 2500-2700 word long article of all the major news events of the past day. \
    You can omit less relevant news and add some creativity in your presentation, but make sure that you keep the important details\
        (like names, dates, and other information)in your write up. \. Make sure that you write this summary as if you are a reporter narrating the news.")

stocks = query_engine.query("Tell me about the stock market. Is it a good time to invest?")

# print("Document : \n\n\n", documents)
# print("The Greatest Footballer Ever - \n\n", response1)
# print("Messi's achievements - \n\n", response2)
# print("Ron de Santis question ::: ", response3)
# print("Sports news ::: ", response4)
# print("Kansas City Weather ::: ", response5)
# print("Ram Mandir info ::: ", response6)


print("\n\n\nSUMMARY OF THE DAY\n\n\n")
summary.print_response_stream()

print("\n\nSTOCKS\n\n", stocks)

stanford = query_engine.query("Was there any news about Stanford?")
print("\n\nSTANFORD\n\n", stanford)
