from fastapi import Depends, Response, status
from fastapi.responses import JSONResponse

from pydantic import Field
from typing import Any
from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class UserShanyraksLikes(AppModel):
    id: Any = Field(alias="_id")
    address: str


class Likes(AppModel):
    shanyraks: list[UserShanyraksLikes]



@router.get("/users/favorites/shanyraks", status_code=status.HTTP_200_OK, response_model=Likes)
def get_user_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    result = svc.repository.get_shanyraks(jwt_data.user_id)
    print(result)
    return Likes(shanyraks=result)