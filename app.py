from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import time
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint with a welcome message and link to upload page
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
      <head>
        <title>Welcome to the File Upload API</title>
      </head>
      <body>
        <h1>Welcome to the File Upload API</h1>
        <p>To upload a file, go to <a href="/upload-page">Upload Page</a></p>
      </body>
    </html>
    """

# Upload page with a file upload form
@app.get("/upload-page", response_class=HTMLResponse)
def upload_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload File to FastAPI</title>
    </head>
    <body>
        <h1>Upload a Text File</h1>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".txt" required>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """

# Optional GET handler for /upload/ to provide guidance if someone sends a GET request
@app.get("/upload/")
def upload_info():
    return {"info": "This endpoint accepts POST requests only for file uploads."}

# POST endpoint to handle file uploads
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
    execution_time = time.time() - start_time

    return {
        "filename": file.filename,
        "encoding": encoding_used,
        "num_words": num_words,
        "num_unique_words": unique_words,
        "num_characters": num_chars,
        "execution_time": execution_time
    }
