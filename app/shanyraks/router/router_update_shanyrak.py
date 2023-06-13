from fastapi import Depends, Response, status

from app.utils import AppModel
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class UpdateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{shanyrak_id}")
def update_shanyrak(
    input: UpdateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    svc.repository.update_user(jwt_data.user_id, input.dict())
    return Response(status_code=200)