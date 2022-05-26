import uvicorn
from fastapi import FastAPI, UploadFile

import utils.template

app = FastAPI()


@app.post("/upload-file/")
async def create_upload_file(file: UploadFile):
    content = await file.read()

    return {"filename": file.filename, "contentType": file.content_type}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
