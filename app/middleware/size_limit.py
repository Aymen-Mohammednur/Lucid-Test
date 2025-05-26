from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse 

class SizeLimitMiddleware(BaseHTTPMiddleware):
    """Reject any request whose body exceeds max_bytes (default 1 MB)."""

    def __init__(self, app, max_bytes: int = 1_048_576):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        if len(body) > self.max_bytes:
            return JSONResponse(     
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={
                    "error": "payload_too_large",
                    "max_bytes": self.max_bytes,
                    "detail": f"Payload exceeds {self.max_bytes} bytes limit",
                },
            )
        
        request._receive = lambda: {"type": "http.request", "body": body}
        return await call_next(request)
