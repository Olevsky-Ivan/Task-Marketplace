from fastapi import FastAPI, Depends

from app.database.session import Base, engine
from app.api import auth
from app.core.deps import get_current_user
from app.models import user  # IMPORTANT: import models

app = FastAPI(title="Task Wallet System")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "API works"}


@app.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }