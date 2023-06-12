from fastapi import Depends, HTTPException, status

from app.utils import AppModel
from app.auth.utils import get_current_user_id

from ..service import Service, get_service
from . import router


class UpdateUserRequest(AppModel):
    phone: str
    name: str
    city: str


class UpdateUserResponse(AppModel):
    


@router.patch(
    "/auth/users/me",
    status_code=status.HTTP_200_OK
)
def update_user(
    input: UpdateUserRequest,
    current_user_id: int = Depends(get_current_user_id),
    svc: Service = Depends(get_service)
):
    user = svc.repository.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    updated_data = {
        "phone": input.phone,
        "name": input.name,
        "city": input.city
    }
    svc.repository.update_user(current_user_id, updated_data)