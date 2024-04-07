import logging

from fastapi import Request, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from services.blacklist_manager import BlacklistManager


class BlacklistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.blacklist_manager = BlacklistManager.from_file()
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        logging.getLogger('').info(f'Checking the client with ip {request.client.host}')
        if self.blacklist_manager.ip_is_blacklisted(request.client.host):
            logging.getLogger('').info(f'Ip {request.client.host} is blocked')
            return Response(status_code=status.HTTP_403_FORBIDDEN)
        response = await call_next(request)
        return response
