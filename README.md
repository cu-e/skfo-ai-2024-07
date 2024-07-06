## Установка и запуск
### В корне проекта:
#### Создать виртуальное окружение и установить зависимости
```
python -m venv venv
source venv/bin/activate (Linux/MacOS)
venv\Scripts\activate (Windows)
pip install -r requirements.txt
```
#### В папке backend создать папку models и закинуть туда файлы model_resnet.tflite и model1_nomer.tflite
#### Запустить бекенд из корневой папки
```
uvicorn backend.app.main:app
```