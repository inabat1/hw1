from fastapi import Depends, HTTPException, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.delete("/shanyraks/{shanyrak_id}/comments/{comment_id}")
def delete_comment(
    shanyrak_id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    
):
    
    
    shanyrak = svc.repository.get_shanyrak(shanyrak_id, jwt_data.user_id)
    if not shanyrak:
        raise HTTPException(status_code=404, detail="Shanyrak not found")

  
    comment = svc.repository.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

  
    if comment["shanyrak_id"] != shanyrak_id:
        raise HTTPException(status_code=404, detail="Comment not found")


    if comment["user_id"] != jwt_data.user_id:
        raise HTTPException(status_code=403, detail="Cannot delete another user's comment")

    result = svc.repository.delete_comment(comment_id, jwt_data.user_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete comment")

    return Response(status_code=204)
