from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateUserRequest(AppModel):
    email: str
    password: str


class UpdateUserResponse(AppModel):
    email: str


@router.patch(
    "/auth/users/me",
    status_code=status.HTTP_200_OK,
    response_model=UpdateUserResponse
)
def update_user(
    user_id: int,
    input: UpdateUserRequest,
    svc: Service = Depends(get_service)
) -> dict[str, str]:
    user = svc.repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    updated_user = svc.repository.update_user(user_id, input.dict())

    return UpdateUserResponse(email=updated_user.email)