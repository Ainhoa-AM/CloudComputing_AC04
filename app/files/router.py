import os
from fastapi import APIRouter, UploadFile, File, Header, HTTPException
from fastapi.responses import FileResponse
from pypdf import PdfMerger
from pydantic import BaseModel
from app.files.models import FileDB
import uuid
import aiohttp

from app.authentication.api.router import IntrospectOutput

router = APIRouter()

BASE_PATH = "storage"

class BaseFile(BaseModel):
    id: str
    filename: str
    user: str


auth_url = "http://carlemany-backend:80/auth/introspect"
async def introspect(auth: str):
    headers = {
        "accept": "application/json",
        "auth": auth
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(auth_url, headers=headers, ssl=False) as response:
            if response.status != 200:
                return None
            data = await response.json()
            return IntrospectOutput(**data)


@router.get("/")
async def list_files(auth: str = Header()) -> dict[str, list[dict]]:
    user_info = await introspect(auth=auth)
    if user_info is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    db_files = await FileDB.filter(user=user_info.username)
    result = [{"id": str(f.id), "filename": f.filename, "user": f.user} for f in db_files]
    return {"files": result}


@router.post("/")
async def create_file(auth: str = Header()) -> dict[str, str]:
    user_info = await introspect(auth=auth)
    if user_info is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    new_id = uuid.uuid4()
    await FileDB.create(id=new_id, filename="", user=user_info.username)
    return {"status": f"File created, id: {new_id}"}


@router.post("/files/{id}")
async def upload_file(id: str, auth: str = Header(), input_file: UploadFile = File()) -> dict[str, str]:
    user_info = await introspect(auth=auth)
    if user_info is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    file = await FileDB.get_or_none(id=id, user=user_info.username)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    username = user_info.username
    path = os.path.join(BASE_PATH, username)
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(BASE_PATH, username, id)
    with open(file_path, "wb") as buffer:
        while chunk := await input_file.read(8192):
            buffer.write(chunk)

    file.filename = input_file.filename
    await file.save()

    return {"status": "File uploaded"}


@router.get("/files/{id}")
async def get_file(id: str, auth: str = Header()):
    user_info = await introspect(auth=auth)
    if user_info is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    file = await FileDB.get_or_none(id=id, user=user_info.username)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    username = user_info.username
    file_path = os.path.join(BASE_PATH, username, id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=file.filename, media_type="application/pdf")


@router.delete("/files/{id}")
async def delete_file(id: str, auth: str = Header()) -> dict[str, str]:
    user_info = await introspect(auth=auth)
    if user_info is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    file = await FileDB.get_or_none(id=id, user=user_info.username)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    username = user_info.username
    file_path = os.path.join(BASE_PATH, username, id)
    if os.path.exists(file_path):
        os.remove(file_path)

    await file.delete()
    return {"status": "File deleted"}


@router.post("/merge")
async def merge_files(auth: str = Header()) -> dict[str, str]:
    user_info = await introspect(auth=auth)
    if user_info is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    username = user_info.username
    user_files = await FileDB.filter(user=username)
    user_files = [f for f in user_files if f.filename.endswith(".pdf") and "merged" not in f.filename.lower()]

    merged_count = await FileDB.filter(user=username, filename__icontains="merged").count()
    merger = PdfMerger()

    for f in user_files:
        pdf_file_path = os.path.join(BASE_PATH, username, str(f.id))
        if os.path.exists(pdf_file_path):
            merger.append(pdf_file_path)

    merged_filename = f"Merged PDFs{'' if merged_count == 0 else f' {merged_count + 1}'}.pdf"
    new_id = uuid.uuid4()
    file_path = os.path.join(BASE_PATH, username, str(new_id))

    os.makedirs(os.path.join(BASE_PATH, username), exist_ok=True)
    merger.write(file_path)
    merger.close()

    await FileDB.create(id=new_id, filename=merged_filename, user=username)
    return {"status": f"PDF files merged, id: {new_id}"}
