from datetime import datetime
from typing import List, Any, Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        shanyrak = self.database["shanyraks"].insert_one(data)
        return shanyrak.inserted_id

    def get_shanyrak(self, shanyrak_id:str, user_id:str)-> Optional[dict]:
        user = self.database["shanyraks"].find_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        return user