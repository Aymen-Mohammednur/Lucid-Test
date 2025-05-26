from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.db.base import Base
from app.db.session import engine
from app.middleware.size_limit import SizeLimitMiddleware
from app.api.routes import auth as auth_routes
from app.api.routes import posts as posts_routes

app = FastAPI(title="Lucid Test", version="1.0.0")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Lucid Test",
        version="1.0.0",
        description="A simple app for lucid",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 1 MB request-body cap
app.add_middleware(SizeLimitMiddleware, max_bytes=1_048_576)

# Include routers
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(posts_routes.router, tags=["posts"])


## UNCOMMENT TO AUTO CREATE ALL TABLES ON FIRST START
# @app.on_event("startup")
# def create_tables() -> None:
#     """Auto-create DB schema on startup"""
#     Base.metadata.create_all(bind=engine)
