from datetime import datetime
from pathlib import Path
from typing import List, Optional

import aioboto3
import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import app_settings
from db.db import get_session
from schemas.file_schema import FileCreate
from schemas.file_schema import FileResponse as FileResponseEntity
from services.file import file_crud
from services.password_manager import PasswordManager

router = APIRouter()


s3 = aioboto3.Session(aws_access_key_id=app_settings.aws_access_key_id,
                      aws_secret_access_key=app_settings.aws_secret_access_key)


async def upload_file_to_s3(file_path: str, bucket_name: str, object_name: str):
    try:
        async with s3.client('s3', endpoint_url='https://storage.yandexcloud.net') as s3_client:
            await s3_client.upload_file(Filename=file_path, Bucket=bucket_name, Key=object_name)
            return await s3_client.head_object(Bucket=bucket_name, Key=object_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Произошла ошибка при загрузке файла в S3: {e}')


async def download_file_from_s3(bucket_name: str, object_name: str):
    try:
        async with s3.client('s3', endpoint_url='https://storage.yandexcloud.net') as s3_client:
            async with aiofiles.tempfile.NamedTemporaryFile(delete=False) as temp_file:
                await s3_client.download_fileobj(Bucket=bucket_name, Key=object_name, Fileobj=temp_file)
                await temp_file.seek(0)
                return temp_file.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при скачивании файла из S3: {e}")


@router.post("/upload/", response_model=FileResponseEntity)
async def upload_file(
        path: str,
        file: UploadFile = File(...),
        current_user: str = Depends(PasswordManager.get_current_user),
        db: AsyncSession = Depends(get_session)
):
    filepath = Path(path) / file.filename if str(path).endswith('/') else Path(path)
    temp_path = f"/tmp/{file.filename}"
    async with aiofiles.tempfile.NamedTemporaryFile() as buffer:
        await buffer.write(await file.read())
    file_create = FileCreate(size=Path(temp_path).stat().st_size,
                             username=current_user,
                             name=file.filename,
                             created_at=str(datetime.now()),
                             path=str(filepath))
    await upload_file_to_s3(temp_path, app_settings.project_bucket, str(filepath))
    await file_crud.create(db, obj_in=file_create)
    return file_create


@router.get("/", response_model=List[FileResponseEntity])
async def file_info(current_user: str = Depends(PasswordManager.get_current_user),
                      db: AsyncSession = Depends(get_session)):
    return await file_crud.get_multi(db, username=current_user)


@router.get("/download/")
async def download_file(
    path: Optional[str] = None,
    file_id: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user: str = Depends(PasswordManager.get_current_user)
):
    if path:
        file = await download_file_from_s3(app_settings.project_bucket, path)
    elif file_id:
        file_entity = await file_crud.get(db, id=file_id)
        file = await download_file_from_s3(app_settings.project_bucket, file_entity.path)
    else:
        return HTTPException(status_code=400, detail="Не передан путь к файлу")

    return FileResponse(file, media_type='application/octet-stream')
