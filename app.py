from datetime import datetime
import uvicorn
from waitress import serve
from jose import jwt
from dotenv import dotenv_values
from fastapi import FastAPI, UploadFile, Form, File, BackgroundTasks, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from main import main
import utils.db_manager as db_manager


class SecutityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if ('access_token' in request.cookies):
            access_token = request.cookies['access_token']
            key = env['QDC_2D_ACCESS_TOKEN_SECRET']

            try:
                payload = jwt.decode(access_token, key)
                [user_id, task_id, exp] = [*payload.values()]
                if int(datetime.utcnow().timestamp()) <= exp:
                    request.state.user_id = user_id
                    request.state.task_id = task_id
                    response = await call_next(request)
                    return response

            except Exception as exc:
                return JSONResponse(
                    headers={'Access-Control-Allow-Origin': '*'},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={'message': 'Something went wrong!!!'}
                )

        else:
            return JSONResponse(
                headers={'Access-Control-Allow-Origin': '*'},
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'message': 'Please, authorized first!!!'}
            )


app = FastAPI()
env = dotenv_values(".env")
origins = ["http://localhost:3000", "http://localhost", ]

# db_manager.init(user=env['QDC_2D_DB_USER'],
#                 password=env['QDC_2D_DB_PASSWORD'],
#                 host=env['QDC_2D_DB_HOST'],
#                 port=env['QDC_2D_DB_PORT'],
#                 database=env['QDC_2D_DB_NAME'])


app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.add_middleware(SecutityMiddleware)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        headers={'Access-Control-Allow-Origin': '*'},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'message': 'Something went wrong!!!'}
    )


def classify_run_service(config_vars, joints_source, user_id, task_id):
    main(config_vars, joints_source, user_id, task_id)


async def classify_run_controller(background_tasks: BackgroundTasks, request: Request, config_vars, joints_source):
    joints_source = (await joints_source.read())
    user_id = request.state.user_id
    task_id = request.state.task_id
    background_tasks.add_task(classify_run_service, config_vars, joints_source, user_id, task_id)


@app.post("/classify/run")
async def classify_run(request: Request, background_tasks: BackgroundTasks, config_vars: str = Form(),
                       joints_source: UploadFile = File()):
    await classify_run_controller(background_tasks, request, config_vars, joints_source)
    return {"status": "Running"}


if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=8000)