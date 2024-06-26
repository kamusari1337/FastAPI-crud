from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers.employee_router import router as employee_router
from routers.department_router import router as department_router
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


app = FastAPI(title="Restful API",
              description="FastAPI restful api for department organization",
              lifespan=lifespan)


@app.get("/")
def hello_world():
    return {"message": "Hello world!"}


app.include_router(employee_router)
app.include_router(department_router)

if __name__ == "__main__":
    run("main:app", host="localhost", reload=True)
