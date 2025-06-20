from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.management.views.users import telegram_users_router

app = FastAPI(
    openapi_prefix='/api',
    title="CoNote Backend",
    description="Backend service for CoNote application",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(telegram_users_router)
