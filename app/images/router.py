import shutil

from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/{image_id}")
async def get_image(image_id: int):
    return FileResponse(f"app/static/images/{image_id}.webp")


@router.post("")
async def create_image(image_id: int, file: UploadFile):
    with open(f"app/static/images/{image_id}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return None
