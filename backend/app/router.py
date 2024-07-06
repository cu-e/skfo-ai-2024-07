from fastapi import APIRouter, UploadFile
from backend.app.dependencies import LicensePlateRecognitionDep


router = APIRouter()


@router.post('/upload-zip-file')
async def upload_zip_file(
    zip_file: UploadFile,
    license_plate_recognition: LicensePlateRecognitionDep
) -> dict:
    """функция-обработчик архива с картинками"""
    content = await zip_file.read()
    recongition_result_bytes = license_plate_recognition.process_zip(content)
    return recongition_result_bytes
