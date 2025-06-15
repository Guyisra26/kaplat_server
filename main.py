from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from request_middleware import RequestLoggingMiddleware
from handlers.exception_handlers import http_exception_handler
from routes import calculator,stack
from routes.logs import router as logs_router
from routes.stack import router as stack_router
from routes.calculator import router as calculator_router


app = FastAPI()
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(calculator_router)
app.include_router(stack_router)
app.include_router(logs_router)