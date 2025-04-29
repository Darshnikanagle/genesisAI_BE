from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
import os

from langchain_tavily import TavilySearch



llm_model_id = "llama-3.1-8b-instant"
llm_proider = "groq"

embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

os.environ["GROQ_API_KEY"] = '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'
os.environ["TAVILY_API_KEY"] = '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'


load_dotenv()

print("initiating model")
# llm = ChatGroq(model="llama3-8b-8192")
llm = init_chat_model(llm_model_id, model_provider = llm_proider)
print("model initiated")


print("initializing embedding model")
embedding = HuggingFaceEmbeddings(
    model_name = embedding_model_name,
    model_kwargs = model_kwargs,
    encode_kwargs = encode_kwargs,
    show_progress = True,
)
print("embedding model initialized")

print("initializing TavilySearch tool")
from langchain_tavily import TavilySearch

search_tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)








    



    