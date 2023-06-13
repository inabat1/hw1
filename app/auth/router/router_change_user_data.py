from fastapi import Depends, HTTPException, status

from app.utils import AppModel
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class UpdateUserRequest(AppModel):
    phone: str
    name: str
    city: str


@router.patch("/users/me", status_code=status.HTTP_200_OK)
def update_user_data(
    data: UpdateUserRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id

    user = svc.repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    updated_user = {
        "phone": data.phone,
        "name": data.name,
        "city": data.city,
    }

    svc.repository.update_user(user_id, updated_user)
    return {"message": "ok"}