from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

UPLOADS = Path("uploads")
CHUNK_SIZE = 1024 * 1024  # 1 MB


async def save_file(file: UploadFile) -> str:
    UPLOADS.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "").suffix.lower()
    filename = f"{uuid4().hex}{extension}"
    file_path = UPLOADS / filename

    try:
        async with aiofiles.open(file_path, "wb") as output:
            while chunk := await file.read(CHUNK_SIZE):
                await output.write(chunk)

        return str(file_path)

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    finally:
        await file.close()
