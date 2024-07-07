from pathlib import Path


ROOT_PATH = Path(__file__).resolve().parent
PATH_TO_ZIP_FILES = ROOT_PATH / 'zip_files'
PATH_TO_RESNET_MODEL = ROOT_PATH / 'models' / 'model_1.tflite'
PATH_TO_NOMER_MODEL = ROOT_PATH / 'models' / 'model_2.tflite'
