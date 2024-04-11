import os
from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest
from dotenv import load_dotenv
from fastapi import UploadFile

from api.files.files import download_file, file_info, upload_file
from core.config import app_settings


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.mark.asyncio
async def test_upload_file():
    path = "/test/path/"
    file_name = "test_file.txt"
    current_user = "test_user"
    db_session_mock = AsyncMock()
    file_content = b"test file content"

    file = UploadFile(filename=file_name, file=BytesIO(file_content))

    with patch("api.files.files.Path") as pathlib_mock, \
            patch("asyncio.open"), \
            patch("aiofiles.tempfile.NamedTemporaryFile") as tempfile_mock, \
            patch("api.files.files.upload_file_to_s3") as upload_to_s3_mock, \
            patch("services.file.file_crud.create") as file_create_mock:

        temp_file_mock_instance = tempfile_mock.return_value.__aenter__.return_value
        temp_file_mock_instance.name = "/tmp/test_file.txt"

        pathlib_mock.return_value.stat.return_value.st_size = len(file_content)

        await upload_file(
            path=path,
            file=file,
            current_user=current_user,
            db=db_session_mock
        )

        upload_to_s3_mock.assert_called_once_with(
            temp_file_mock_instance.name, os.getenv('PROJECT_BUCKET'), f"{path}/{file_name}"
        )
        db_obj = file_create_mock.mock_calls[0].kwargs['obj_in']
        assert db_obj.name == file_name
        assert db_obj.size == len(file_content)
        assert db_obj.path == f"{path}/{file_name}"
        assert db_obj.username == current_user


@pytest.mark.asyncio
async def test_download_file():
    current_user = "test_user"
    db_session_mock = AsyncMock()
    file_path = "/test/path/test_file.txt"
    downloaded_file_path = '/tmp/file'

    with patch("api.files.files.download_file_from_s3") as download_from_s3_mock, \
            patch("services.file.file_crud.get") as get_file_info_mock:

        download_from_s3_mock.return_value = downloaded_file_path
        get_file_info_mock.return_value = type('test', (object,), {"id": 1, "name": "test_file.txt", "path": file_path})

        response_file = await download_file(
            path=file_path,
            db=db_session_mock,
            current_user=current_user
        )

        download_from_s3_mock.assert_called_once_with(app_settings.project_bucket, file_path)
        assert not get_file_info_mock.called

        assert response_file.path == downloaded_file_path

        await download_file(
            file_id="1",
            db=db_session_mock,
            current_user=current_user
        )

        get_file_info_mock.assert_called_once_with(db_session_mock, id="1")
        download_from_s3_mock.assert_called_with(app_settings.project_bucket, file_path)


@pytest.mark.asyncio
async def test_file_info():
    current_user = "test_user"
    db_session_mock = AsyncMock()
    files_info_mock = [{"id": 1, "name": "test_file1.txt"}, {"id": 2, "name": "test_file2.txt"}]

    with patch("api.files.files.file_crud.get_multi") as get_multi_mock:
        get_multi_mock.return_value = files_info_mock

        response = await file_info(
            current_user=current_user,
            db=db_session_mock
        )

        get_multi_mock.assert_called_once_with(db_session_mock, username=current_user)

        assert response == files_info_mock
