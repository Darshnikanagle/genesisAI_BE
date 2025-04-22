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
from app.constants import THREAD_DIRECTORY
from app.controllers import llm_controller
from fastapi.encoders import jsonable_encoder
import json
from app.llm import pdf as pdf_vecotr

# session = Session()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

class ThreadCreate(BaseModel):
    type: str
    title: str
    user_id: int

class ThreadUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None

class ListThread(BaseModel):
    type: str
    user_id: int

class ThreadResponse(BaseModel):
    id: int
    type: str
    title: str
    user_id: int

    class Config:
        orm_mode = True

# Create a new thread
@router.post("/")
def create_thread(
    type: str = Form(...),
    title: str = Form(...),
    user_id: int = Form(...),
    content: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    new_thread = Thread(type=type, title=title, user_id=user_id)
    db.add(new_thread)
    db.commit() 
    

    # Create folder path using thread_id
    folder_path = os.path.join(THREAD_DIRECTORY, str(new_thread.id))
    os.makedirs(folder_path, exist_ok=True)

    if type == 'pdf':
        # content_bytes = file.read()
        # # Optionally save or process file content here
        # print(f"Uploaded file name: {file.filename}")
        # print(f"File content size: {len(content_bytes)} bytes")
        file = files[0]
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        print(f"PDF saved at: {file_path}")

        pdf_vecotr.create_embedding(file_path=file_path, user_id=user_id, thread_id=new_thread.id )

        {
            "thread": new_thread,
        }

    elif type == 'summarize':
        # print(f"Received text content: {content[:100]}...")  # Print preview

        if content :
            print("text content found...")
            text_file_path = os.path.join(folder_path, "genesis_data.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Text content saved at: {text_file_path}")

        else:
            print("PDF file present")
            file = files[0]
            file_path = os.path.join(folder_path, file.filename)
            with open(file_path, 'wb') as f:
                f.write(file.file.read())
            print(f"PDF saved at: {file_path}")

        summary = llm_controller.summarize(llm_controller.Chat(thread_id=new_thread.id))

        llm_controller.add_thread_message(thread_id=new_thread.id, user_type="system", message= summary, db=db)

        db.refresh(new_thread)

        return {
            "thread": new_thread,
            "summary": summary,
        }

    elif type == 'resume':

        print("total resumes:", len(files))

        for file in files:
            file_path = os.path.join(folder_path, file.filename)
            with open(file_path, 'wb') as f:
                f.write(file.file.read())
        print(f"{len(files)} file(s) saved to: {folder_path}")

        llm_controller.add_thread_message(thread_id=new_thread.id, user_type="user", message = content, db=db)

        screening_result = llm_controller.screen_resume(llm_controller.Chat(query=content, thread_id=new_thread.id))

        json_data = json.dumps([resume.dict() for resume in screening_result])

        # json_result = json.dumps(screening_result)

        # print("json_result:", json_result)

        llm_controller.add_thread_message(thread_id=new_thread.id, user_type="system", message = json_data, db=db)

        db.refresh(new_thread)

        return {
            "thread": new_thread,
            "screening_result": screening_result
        }

    elif type == 'chat':
        pass

    return {
            "thread": new_thread,
        }

# Get all threads
@router.get("/")
def get_threads(list_thread: ListThread = Depends(),  db: Session = Depends(get_db)):
    return {
        "data": db.query(Thread).filter(Thread.type == list_thread.type, Thread.user_id == list_thread.user_id).all()
        }

# Get thread by ID
@router.get("/{thread_id}")
def get_thread(thread_id: int, db: Session = Depends(get_db)):

    thread = db.query(Thread).filter(Thread.id == thread_id).first()

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    if(thread.type == "summarize" or thread.type == "pdf"):
        # get content
        folder_path = os.path.join(THREAD_DIRECTORY, str(thread_id))

        print("folder_path", folder_path)
        file_paths = llm_controller.get_all_file_path(folder_path=folder_path)

        content = ""
        file_path = ""

        if "genesis_data.txt" in file_paths[0]:
            content = llm_controller.get_file_content(file_paths[0])
        else:
            file_path = file_paths[0]

        return {
            "thread": thread,
            "content": content,
            "file_path": file_path
        }
    elif thread.type == "resume":

        pass


    
    return {
        "data": thread
    }

# Update a thread
@router.put("/{thread_id}", response_model=ThreadResponse)
def update_thread(thread_id: int, thread_data: ThreadUpdate, db: Session = Depends(get_db)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    for key, value in thread_data.dict(exclude_unset=True).items():
        setattr(thread, key, value)

    db.commit()
    db.refresh(thread)
    return {
        "data":thread
        }

# Delete a thread
@router.delete("/{thread_id}")
def delete_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    db.delete(thread)
    db.commit()
    return {"message": "Thread deleted successfully", "thread_id": thread_id}

# ====================================== Thread message =======================

# Get thread messages by ID
@router.get("/{thread_id}/messages")
def get_thread_messages(thread_id: int, db: Session = Depends(get_db)):
    messages = db.query(ThreadMessage).filter(ThreadMessage.thread_id == thread_id).all()
    return {
        "data": messages
    }