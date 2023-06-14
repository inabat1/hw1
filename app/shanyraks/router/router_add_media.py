from fastapi import Depends, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from typing import Any 
from pydantic import Field
from ..service import Service, get_service
from . import router


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str



@router.post("/{shanyrak_id:str}/media")
def add_media(
    file: UploadFile,
    svc: Service = Depends(get_service),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    url = svc.s3_service.upload_file(file.file, file.filename)
    
    return {"msg": url}