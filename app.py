import uvicorn
from fastapi import FastAPI, UploadFile, Form, File, BackgroundTasks, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from main import main

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

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        headers={'Access-Control-Allow-Origin': '*'},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'Something went wrong!!!'}
    )

def classify_run_service(config_vars, joints_source):
    main(config_vars, joints_source)


async def classify_run_controller(background_tasks: BackgroundTasks, config_vars, joints_source):
    joints_source = (await joints_source.read())
    background_tasks.add_task(classify_run_service, config_vars, joints_source)


@app.post("/classify/run")
async def classify_run(background_tasks: BackgroundTasks, config_vars: str = Form(),
                       joints_source: UploadFile = File()):
    await classify_run_controller(background_tasks, config_vars, joints_source)
    return {"status": "Running"}


if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=8000)
