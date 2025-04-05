from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import time
import re

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    start_time = time.time()

    content = await file.read()

    
    try:
        text = content.decode("utf-8")
        encoding_used = "utf-8"
    except UnicodeDecodeError:
        try:
            text = content.decode("latin-1")
            encoding_used = "latin-1"
        except UnicodeDecodeError:
            return {"error": "Unsupported file encoding"}

    
    clean_text = re.sub(r"[^\w\s']", " ", text)  
    clean_text = re.sub(r"\s+", " ", clean_text).strip()  

    words = clean_text.split()
    num_words = len(words)

    unique_words = len(set(word.lower() for word in words))  

    num_chars = len(re.sub(r"\s", "", text)) 

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "filename": file.filename,
        "encoding": encoding_used,
        "num_words": num_words,
        "num_unique_words": unique_words,
        "num_characters": num_chars,
        "execution_time": execution_time
    }
