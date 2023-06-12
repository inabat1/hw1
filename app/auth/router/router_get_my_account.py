from typing import Any

from fastapi import Depends
from pydantic import Field

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.utils import AppModel
from app.auth.utils import get_current_user_id

from ..service import Service, get_service
from . import router


class GetMyAccountResponse(AppModel):
    _id: str = Field(alias="_id")
    email: str
    phone: str
    name: str
    city: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/me", response_model=GetMyAccountResponse)
def get_my_account(
    current_user_id: int = Depends(get_current_user_id),
    svc: Service = Depends(get_service),
) -> GetMyAccountResponse:
    user = svc.repository.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return GetMyAccountResponse(
        _id=user["_id"],
        email=user["email"],
        phone=user["phone"],
        name=user["name"],
        city=user["city"]
    )
