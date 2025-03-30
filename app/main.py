from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.authentication.api.router import router as authentication_router
from app.files.router import router as files_router
from app.database import DATABASE_URL

app = FastAPI()
app.include_router(authentication_router, prefix="/auth", tags=["Authentication"])
app.include_router(files_router, prefix="/files", tags=["Files"])

@app.get("/")
def home():
    return {"status": "FastAPI working"}

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["app.authentication.models", "app.files.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
