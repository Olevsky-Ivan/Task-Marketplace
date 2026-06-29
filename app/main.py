from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router
from app.wallet.router import router as wallet_router
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Task Wallet System", version="1.0.0")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])

Path("/uploads").mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="/uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "API works"}
