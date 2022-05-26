import uvicorn
from fastapi import FastAPI, UploadFile

from main import classify_analyse_with_histograms

app = FastAPI()


@app.post("/upload-file/")
async def create_upload_file(file: UploadFile):
    content = await file.read()
    classify_analyse_with_histograms(var_config_json: str = None, nodes_source: str = None)

    return {"filename": file.filename, "contentType": file.content_type}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
