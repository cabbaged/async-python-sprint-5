import time
from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session

router = APIRouter()


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(
    *,
    db: AsyncSession = Depends(get_session)
) -> Any:
    """
    Ping services.
    """

    start_time = time.time()
    await db.execute('select 1')
    end_time = time.time()

    return {'db': end_time - start_time}
