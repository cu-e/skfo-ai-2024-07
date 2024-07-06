from backend.utils.network import LicensePlateRecognition
from backend.config import PATH_TO_NOMER_MODEL, PATH_TO_RESNET_MODEL
from fastapi import Depends
from typing import Annotated


def get_licence_plate_recognition() -> LicensePlateRecognition:
    """зависимость для получения класса обработчика картинок"""
    return LicensePlateRecognition(
        str(PATH_TO_RESNET_MODEL),
        str(PATH_TO_NOMER_MODEL),
        [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', 'A', 'B', 'C', 'E', 'H', 'K', 'M', 'O', 'P', 'T', 'X', 'Y'
        ]
    )


LicensePlateRecognitionDep = Annotated[
    LicensePlateRecognition, Depends(get_licence_plate_recognition)
]
