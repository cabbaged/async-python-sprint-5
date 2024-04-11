from fastapi import FastAPI

middlewares = []


def apply_middlewares(app: FastAPI):
    for middleware in middlewares:
        app.add_middleware(middleware)
