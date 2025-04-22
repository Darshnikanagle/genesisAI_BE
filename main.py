from app.db.db import Base, engine
# from app.db. import Base, engine

# db = SessionLocal()
# user = get_user_by_id(db, 1)
# print(user)


from fastapi import FastAPI, Request
from app.controllers import user_controller
from app.controllers import thread_controller
from app.controllers import llm_controller
import os
from app.llm.pdf import create_embedding, ask_llm, find_chunks
from app.llm.summarize_content import summarize_content
from app.llm.screen_resume import screen_resume
from app.constants import THREAD_DIRECTORY
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import pdfplumber

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["null"] but "*" is easier for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user_controller.router, prefix="/api/users")
app.include_router(thread_controller.router, prefix="/api/thread")
app.include_router(llm_controller.router, prefix="/api/llm")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve the HTML file at root
@app.get("/", response_class=FileResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# file_path = os.path.join(THREAD_DIRECTORY, "2", "IPL.pdf")
# create_embedding(file_path=file_path, user_id=1, thread_id=2)

# query = "who owner IPL in 2017?"
# docs = find_chunks(query=query, user_id=1, thread_id=2)

# combined_text = " ".join(obj.page_content for obj in docs)

# print(ask_llm(content=combined_text, query=query))


# summarize content
# from pathlib import Path

# file_path = os.path.join(THREAD_DIRECTORY, "3")

# folder_path = Path(file_path)

# # List all files
# content = ""
# for file in folder_path.iterdir():
#     if file.is_file():
#         print(f"Reading file: {file}")
#         with open(file, 'r', encoding='utf-8') as f:
#             content = f.read()
#             print(content)

# response = summarize_content(content=content)
# print("summarized conent:\n", response)



# def read_pdf(file_path):
#     text = ""
#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text
#     return text


# # screen resume
# file_path = os.path.join(THREAD_DIRECTORY, "5")

# folder_path = Path(file_path)

# from langchain.document_loaders import PyPDFLoader
# from langchain.schema import Document

# folder_path = file_path
# file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]


# for path in file_paths:

#     loader = PyPDFLoader(path)
#     pages = loader.load()

#     # Combine all text into one document
#     combined_text = "\n".join(page.page_content for page in pages)


#     crieteria = """2 Years of experience, Angular developer 
#     """
#     response = screen_resume(content=combined_text, crieteria=crieteria)
#     print("summarized conent:\n", response)