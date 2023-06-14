from fastapi import Depends, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from typing import Any 
from pydantic import Field
from ..service import Service, get_service
from . import router




@router.post("/{shanyrak_id:str}/media")
def upload_file(
    #shanyrak_id: str,
    file: UploadFile,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    svc.s3_service.upload_file(file, file.filename, jwt_data.user_id)

    #entity = svc.repository.get_shanyrak(shanyrak_id)
    #entity.items.append({"url": url})
    
    return Response(status_code=200)