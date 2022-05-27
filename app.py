import uvicorn
from fastapi import FastAPI, UploadFile, Form, File, Response, Request, HTTPException, status

from main import classify_analyse_with_histograms

app = FastAPI()


async def classify_run_controller(config_vars=Form(), joints_file: UploadFile = File()):

    if joints_file and config_vars:
        nodes_source = (await joints_file.read()).decode()
        classify_analyse_with_histograms(config_vars, nodes_source)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error")


@app.post("/classify/run")
async def classify_run(config_vars: str = Form(), joints_file: UploadFile = File()):
    await classify_run_controller(config_vars, joints_file)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
