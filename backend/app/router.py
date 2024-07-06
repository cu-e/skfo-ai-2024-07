from fastapi import APIRouter, File
from backend.app.dependencies import LicensePlateRecognitionDep
from typing import Annotated


router = APIRouter()


@router.post('/api/upload-zip-file')
async def upload_zip_file(
    zip_file: Annotated[bytes, File()],
    license_plate_recognition: LicensePlateRecognitionDep
) -> dict:
    """функция-обработчик архива с картинками"""
    recongition_result_bytes = license_plate_recognition.process_zip(zip_file)
    return recongition_result_bytes
