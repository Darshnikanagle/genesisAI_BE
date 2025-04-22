from langchain.chat_models import init_chat_model
import os
from langchain_community.vectorstores.faiss import FAISS
from app.util import embedding, llm
from app.constants import LOCAL_DB_DIRECTORY, THREAD_DIRECTORY
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



def create_embedding(file_path: str, user_id: int, thread_id: int):

    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(documents)

        print("Chunk prepared")

        index = f"user_id_{user_id}_thread_id_{thread_id}"

        print("initilizing vector db")
        vector_db = FAISS.from_documents(documents=documents, embedding=embedding)
        print("vector db initilized")
        print("Saving vectors into local db")
        # vector_db.save_local(LOCAL_DB_DIRECTORY)
        vector_db.save_local(folder_path=LOCAL_DB_DIRECTORY, index_name=index)
        print("chunk saved succesfully...")

    except Exception as e:
        print(f"An unexpected error occurred while embedding document: {e}")


def find_chunks(query: str, user_id: int, thread_id: int):

    index = f"user_id_{user_id}_thread_id_{thread_id}"

    vector_db = FAISS.load_local(LOCAL_DB_DIRECTORY
        , embeddings=embedding
        , allow_dangerous_deserialization = True
        , index_name=index
    )

    retriever = vector_db.as_retriever()

    # query = "How much IPL contributed to indian GDP in 2015??"
    docs = retriever.invoke(query)

    print("total chunks found:\n", len(docs))

    return docs

def ask_llm(content: str, query: str):

    template = """{user_query}  Provide answer based on the below context only. Do not provide any explaination.
    Context: {context}
    """
    
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", template)]
    )

    result = prompt_template.invoke({"user_query": query, "context": content})

    # print(result.to_messages())
    
    print("submitted question to llm, awaiting response")
    response = llm.invoke(result.to_messages())
    print("Response received:", response)
    # print(response.content)

    return response.content


# try:

    
    

    


  

#     # sentence = "This is a test sentence."
#     # embedding = model.encode(sentence)

#     # print(embedding.shape)  # Output: (384,)


#     # Load the document, split it into chunks, embed each chunk and load it into the vector store.
#     # raw_documents = TextLoader('state_of_the_union.txt').load()
#     # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     # documents = text_splitter.split_documents(raw_documents)

#     # print("Embedding model initialized")

    

    

#     # print("initilizing vector db")
#     # vector_db = FAISS.from_documents(documents=documents, embedding=embedding)
#     # print("vector db initilized")
#     # print("Saving vectors into local db")
#     # vector_db.save_local(LOCAL_DB_DIRECTORY)
#     # print("vectors saved successfully")

#     vector_db = FAISS.load_local(LOCAL_DB_DIRECTORY
#             , embeddings=embedding
#             , allow_dangerous_deserialization = True
#         )
    
#     retriever = vector_db.as_retriever()

#     query = "How much IPL contributed to indian GDP in 2015??"
#     docs = vector_db.similarity_search(query)
   
#     print("similarity_search\n", docs[0].page_content)


#     docs = retriever.invoke(query)
#     print("retriever", docs[0].page_content)

    

    
    
# except Exception as e:
#      print(f"An unexpected error occurred: {e}")
