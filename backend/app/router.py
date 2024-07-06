from fastapi import APIRouter, UploadFile
from backend.config import PATH_TO_ZIP_FILES
import aiofiles


router = APIRouter()

@router.post('/upload-zip-file')
async def upload_zip_file(zip_file: UploadFile):
    out_path = PATH_TO_ZIP_FILES / zip_file.filename
    async with aiofiles.open(out_path, 'wb') as out_file:
        while content := await zip_file.read(1024):
            await out_file.write(content)
    return {'message': 'ok'}
