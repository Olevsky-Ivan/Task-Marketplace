from fastapi import FastAPI, Depends

from app.database.base import Base
from app.database.session import engine

from app.auth.router import router as auth_router
from app.core.deps import get_current_user
from app.models.user import User

app = FastAPI(
    title="Task Wallet System",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "API works"}


@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
    }