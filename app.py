import uvicorn
from fastapi import FastAPI, UploadFile, Form, File, Response, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from main import classify_analyse_with_histograms

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def classify_run_controller(config_vars, joints_file):
    if joints_file and config_vars:
        nodes_source = await joints_file.read()
        classify_analyse_with_histograms(config_vars, nodes_source)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error")


@app.post("/classify/run")
async def classify_run(config_vars: str = Form(), joints_file: UploadFile = File()):
    try:
        await classify_run_controller(config_vars, joints_file)
        return {"status": "Running"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
