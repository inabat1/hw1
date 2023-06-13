from fastapi import Depends, Response, status

from app.utils import AppModel
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class UpdateUserRequest(AppModel):
    phone: str
    name: str
    city: str


@router.patch("/users/me")
def update_user_data(
    input: UpdateUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    svc.repository.update_user(jwt_data.user_id)
    return Response(status_code=200)
