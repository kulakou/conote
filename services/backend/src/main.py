from fastapi import FastAPI

app = FastAPI(
    title="CoNote Backend",
    description="Backend service for CoNote application",
    version="0.0.1",
)


@app.get("/ping", tags=["Testing"])
async def ping():
    return {"message": "pong"}
