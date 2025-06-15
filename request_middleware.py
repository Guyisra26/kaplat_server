import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from init_services import request_logger, request_counter

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_counter["count"] += 1
        request_id = request_counter["count"]

        method = request.method
        resource = request.url.path

        request_logger.info(
            f"Incoming request | #{request_id} | resource: {resource} | HTTP Verb {method}",
            extra={"request_id": request_id}
        )

        start_time = time.time()
        response: Response = await call_next(request)
        duration_ms = int((time.time() - start_time) * 1000)

        request_logger.debug(
            f"request #{request_id} duration: {duration_ms}ms",
            extra={"request_id": request_id}
        )

        return response