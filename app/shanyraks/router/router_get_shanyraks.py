from typing import Any, List

from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetMyShanyraks(AppModel):
    id: Any = Field(alias="_id")
    content: str


class GetMyShanyraksResponse(AppModel):
    shanyraks: List[GetMyShanyraks]


@router.get("/{id}", response_model=GetMyShanyraksResponse)
def get_shanyraks(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    shanyraks = svc.repository.get_shanyrak_by_user_id(user_id)

    resp = {"shanyraks": shanyraks}

    return resp
