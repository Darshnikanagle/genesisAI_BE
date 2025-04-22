from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
import os



llm_model_id = "llama-3.1-8b-instant"
llm_proider = "groq"

embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

os.environ["GROQ_API_KEY"] = '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'


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






    



    