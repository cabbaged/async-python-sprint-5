from fastapi import FastAPI

from .middleware import BlacklistMiddleware

middlewares = [BlacklistMiddleware]


def apply_middlewares(app: FastAPI):
    for middleware in middlewares:
        app.add_middleware(middleware)
