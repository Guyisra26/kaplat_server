from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_409_CONFLICT

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=HTTP_409_CONFLICT,
        content={"errorMessage": str(exc.detail)}  # ✅ this replaces "detail"
    )
