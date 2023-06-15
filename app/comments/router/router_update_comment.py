from fastapi import Depends, HTTPException, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service

from . import router

class UpdateCommentRequest(AppModel):
    comment: str


@router.patch("/shanyraks/{shanyrak_id:str}/comments/{comment_id:str}")
def update_comment(
    shanyrak_id: str,
    comment_id: str,
    request: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    
    shanyrak = svc.repository.get_shanyrak(shanyrak_id, jwt_data.user_id)
    if not shanyrak:
        raise HTTPException(status_code=404, detail="Shanyrak not found")

   
    comment = svc.repository.get_comment(comment_id)
    if not comment or comment["shanyrak_id"] != shanyrak_id:
        raise HTTPException(status_code=404, detail="Comment not found")

   
    if comment["user_id"] != jwt_data.user_id:
        raise HTTPException(status_code=403, detail="User does not own the comment")

   
    result = svc.repository.update_comment_text(comment_id, request.comment)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to update comment")

    return Response(status_code=200)
