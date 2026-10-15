from fastapi import UploadFile

from repositories.file_repository import save_file


async def save_resume(file: UploadFile) -> str:
    return await save_file(file)
