from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.management.views.verification import verification_router


app = FastAPI(
    root_path='/api',
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

app.include_router(verification_router)
