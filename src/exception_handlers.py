import logging
from urllib.request import Request

import fastapi
import sqlalchemy
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


class RequestValidationError:
    pass


async def handle_db_integrity_error(request: Request, exc: RequestValidationError) -> PlainTextResponse:
    logging.getLogger('').error(exc)
    return PlainTextResponse(str(fastapi.status.HTTP_409_CONFLICT), status_code=fastapi.status.HTTP_409_CONFLICT)


handlers = {
    sqlalchemy.exc.IntegrityError: handle_db_integrity_error
}


def apply_exception_handlers(app: FastAPI):
    for exc, handler in handlers.items():
        app.add_exception_handler(exc, handler)
