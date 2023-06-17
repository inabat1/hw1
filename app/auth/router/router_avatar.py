import imghdr

from fastapi import Depends, Response, status, UploadFile, HTTPException

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.delete(
    "/users/avatar",
    status_code=status.HTTP_200_OK,
)
def delete_avatar(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    svc.repository.delete_avatar(jwt_data.user_id)
    return Response(status_code=200)


@router.post(
    "/users/avatar",
    status_code=status.HTTP_200_OK,
)
def upload_avatar(
    file: UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    if not is_image(file.file.read()):
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not image")
    url = svc.s3_service.upload_file(file.file, file.filename)
    if url is None:
        raise HTTPException(status_code=500, detail=f"File {file.filename} not uploaded")
    url = svc.repository.save_avatar(jwt_data.user_id, url)
    print(url)
    return Response(status_code=200)


def is_image(file_contents: bytes) -> bool:
    image_type = imghdr.what(None, file_contents)
    return image_type is not None

@router.get(
    "/auth/users/avatar",
    status_code=status.HTTP_200_OK,
)
def get_avatar(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    avatar_url = svc.repository.get_avatar(jwt_data.user_id)
    if avatar_url is None:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return Response(content=avatar_url, media_type="text/plain")