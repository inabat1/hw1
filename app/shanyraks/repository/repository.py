from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, input: dict):
        payload = {
            "content": input["content"],
            "user_id": ObjectId(input["user_id"]),
            "created_at": datetime.utcnow(),
        }

        self.database["shanyraks"].insert_one(payload)

    def get_shanyrak_by_user_id(self, user_id: str) -> List[dict]:
        shanyraks = self.database["shanyraks"].find(
            {
                "user_id": ObjectId(user_id),
            }
        )
        result = []
        for shanyrak in shanyraks:
            result.append(shanyrak)

        return result
