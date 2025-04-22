from pathlib import Path
import os


DIR_PATH: Path = Path(__file__).parent

LOCAL_FILE_DIRECTORY = os.path.join(DIR_PATH, "data")
LOCAL_PDF_DIRECTORY = os.path.join(LOCAL_FILE_DIRECTORY, "PDF")
LOCAL_DB_DIRECTORY = os.path.join(LOCAL_FILE_DIRECTORY, "vector_db")    
GENESIS_DATABASE_DIRECTORY = os.path.join(LOCAL_FILE_DIRECTORY, "genesis_db", "genesis.db")   
THREAD_DIRECTORY = os.path.join(LOCAL_FILE_DIRECTORY, "thread")