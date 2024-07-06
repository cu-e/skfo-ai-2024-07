from fastapi import FastAPI
from backend.app.router import router


app = FastAPI()
app.include_router(router)
