from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from typing import Any 
from pydantic import Field
from ..service import Service, get_service
from . import router


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str



@router.post("/{shanyrak_id:str}/media")
def add_media():
    

    return Response(status_code=200)