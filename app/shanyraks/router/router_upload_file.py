from fastapi import Depends, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from typing import Any, List
from pydantic import Field
from ..service import Service, get_service
from . import router




@router.post("/{shanyrak_id:str}/media")
def upload_file(
    shanyrak_id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)

    #entity = svc.repository.get_shanyrak(shanyrak_id)
    #entity.items.append({"url": url})
    svc.repository.add_images_to_shanyrak(shanyrak_id, jwt_data.user_id, result)
    return Response(status_code=200)