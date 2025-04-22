from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.db.models.thread_model import Thread
from app.db.models.thread_message_model import ThreadMessage
from pydantic import BaseModel
from typing import List, Optional

from app.db.db import SessionLocal
import os
from pathlib import Path
from app.llm.chat_model import chat as llm_chat
from app.llm.pdf import find_chunks, ask_llm
# from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from app.constants import THREAD_DIRECTORY
from app.llm.summarize_content import summarize_content
from app.llm.screen_resume import screen_resume as screen_cv
import json

# session = Session()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()

class Chat(BaseModel):
    query: Optional[str] = None
    user_id: Optional[int] = None
    thread_id: int

class ResumeResponse(BaseModel):
    file_name: str
    status: str
    details: dict[str, str]
    summary: str

def get_all_file_path(folder_path: str) -> List[str]:
    # screen resume

    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    return file_paths

def get_file_content(file_path: str) -> str:

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        pages = loader.load()
    elif file_path.endswith(".txt"):
        pages = TextLoader(file_path).load()

    # Combine all text into one document
    combined_text = "\n".join(page.page_content for page in pages)

    return combined_text

def add_thread_message(thread_id: int, user_type: str, message: str, db: Session):
    user_thread_message = ThreadMessage(thread_id = thread_id, user_type = user_type, message = message)
    db.add(user_thread_message)
    db.commit()

# chat with LLM
@router.post("/chat")
def chat(chat: Chat, db: Session = Depends(get_db)):

    add_thread_message(thread_id = chat.thread_id, user_type = "user", message = chat.query, db = db)

    try:
        response = llm_chat(query=chat.query,thread_id=chat.thread_id)

        add_thread_message(thread_id = chat.thread_id, user_type = "system", message = response, db = db)
    except Exception as e:
        pass
    
    return {"data": response}


# ask against pdf
@router.post("/pdf")
def ask_pdf(chat: Chat, db: Session = Depends(get_db)):


    add_thread_message(thread_id = chat.thread_id, user_type = "user", message = chat.query, db = db)

    docs = find_chunks(query=chat.query, user_id=chat.user_id, thread_id=chat.thread_id)

    content = " ".join(obj.page_content for obj in docs)

    response = ask_llm(content=content,query=chat.query)

    add_thread_message(thread_id = chat.thread_id, user_type = "system", message = response, db = db)

    return {"data": response}


# ask against pdf
@router.post("/summarize")
def summarize(chat: Chat) -> str:

    try:
        folder_path = os.path.join(THREAD_DIRECTORY, str(chat.thread_id))

        print("folder_path", folder_path)
        file_paths = get_all_file_path(folder_path=folder_path)

        print("file_paths", file_paths)

        file_content = ""
        for path in file_paths:
            file_content = get_file_content(path)

        if file_content:
            response = summarize_content(content=file_content)
            return response
    
    except Exception as e:
        print(f"An unexpected error occurred while summarizing content: {e}")
    
    raise Exception("No content to summarize")


# ask against pdf
@router.post("/resume")
def screen_resume(chat: Chat):

    try:
        folder_path = os.path.join(THREAD_DIRECTORY, str(chat.thread_id))

        file_paths = get_all_file_path(folder_path=folder_path)

        file_content = ""
        resume_status = []
        for path in file_paths:
            file_content = get_file_content(path)
            response = screen_cv(content=file_content, crieteria=chat.query)
            print("resume result response:", response)
            # json.loads(response)
            r = ResumeResponse(**json.loads(response))
            r.file_name = Path(path).name
            print("resume result:", r)
            resume_status.append(r)

        if resume_status:
            return resume_status
    
    except Exception as e:
        print(f"An unexpected error occurred while resume screening: {e}")