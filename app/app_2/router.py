from fastapi import APIRouter, Header, UploadFile, HTTPException
import uuid
from app_2.persistences.minio_file_storage_service import MinioFileStorageService
import aiohttp

router = APIRouter()

object_storage_service = MinioFileStorageService()

authentication_url = "http://carlemany-backend:80/auth/introspect"

async def introspect(auth: str):
    headers = {
        "accept": "application/json",
        "auth": auth
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(authentication_url, headers=headers) as response:
            if response.status != 200:
                return None
            body = await response.json()
            return body

@router.post("/file/")
async def upload_file(auth: str = Header(), input_file: UploadFile = None):
    user_info = await introspect(auth=auth)
    if user_info is None:
        raise HTTPException(status_code=403, detail="Forbidden")

    prefix = "files/"
    filename = str(uuid.uuid4()) + ".pdf"
    local_path = prefix + filename

    with open(local_path, "wb") as buffer:
        while chunk := await input_file.read(8192):
            buffer.write(chunk)

    remote_path = object_storage_service.put_file(local_path, prefix + filename)

    return {"path": remote_path}
