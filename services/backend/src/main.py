from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.management.views.verification import verification_router
from src.management.views.users import telegram_users_router
from src.notetaking.views.rooms import rooms_router
from src.notetaking.views.notes import notes_router


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
app.include_router(telegram_users_router)
app.include_router(rooms_router)
app.include_router(notes_router)
