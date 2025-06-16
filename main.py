from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import applicant, event ,creator

app = FastAPI()

# 設定允許的來源
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://14bd-202-208-112-184.ngrok-free.app", 
    "https://*.ngrok.io", 
    "https://*.ngrok-free.app" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # 預檢請求的快取時間（秒）
)

models.Base.metadata.create_all(bind=engine)

app.include_router(event.router)
app.include_router(applicant.router)
app.include_router(creator.router)