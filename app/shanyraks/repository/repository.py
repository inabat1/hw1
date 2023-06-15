from datetime import datetime
from typing import List, Any, Optional


from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database
        

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id:str, user_id:str)-> Optional[dict]:
        user = self.database["shanyraks"].find_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        return user
    
    def update_shanyrak(self, shanyrak_id: str, user_id: str, data: dict()) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id":ObjectId(user_id)},
            update={
                "$set": data,
            }
        )
    
    def delete_shanyrak(self, shanyrak_id: str, user_id:str, data: dict())-> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id":ObjectId(user_id)}
        )
    
    def add_images_to_shanyrak(self, shanyrak_id: str, user_id: str, urls: List[str]) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={"$push": {"images": {"$each": urls}}}
        )
