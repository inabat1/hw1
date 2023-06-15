from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class UpdateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.delete("/{shanyrak_id:str}/media")
def delete_shanyrak_image(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    result = svc.repository.delete_all_images_from_shanyrak(shanyrak_id, jwt_data.user_id)
    
    if result.modified_count == 0:
        return Response(status_code=404, content="No images found")
    
    return Response(status_code=200)