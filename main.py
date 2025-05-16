from fastapi import FastAPI
from routes import calculator,stack

app = FastAPI()

app.include_router(calculator.router)
app.include_router(stack.router)