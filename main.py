from contextlib import asynccontextmanager

from config.database import create_tables, drop_tables
from fastapi import FastAPI
from routers.department_router import router as department_api
from routers.employee_router import router as employee_api
from termcolor import colored
from uvicorn import run


@asynccontextmanager
async def lifespan(app: FastAPI):
    INFO = colored('INFO', 'green')

    # await drop_tables()
    # print(f"{INFO}:\t  База очищена")
    # await create_tables()
    # print(f"{INFO}:\t  База готова к работе")
    yield
    print(f"{INFO}:\t  Выключение")


app = FastAPI(title="Restful API", description="FastAPI restful api for department organization", lifespan=lifespan)


@app.get("/")
def hello_world():
    return {"message": "Hello world!"}


app.include_router(department_api)
app.include_router(employee_api)

if __name__ == "__main__":
    run("main:app", host="localhost", port=228, reload=True)
