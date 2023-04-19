import datetime

from models_backend.models import Bookmark

from .mongo import ServiceMongo


class Bookmarks(ServiceMongo):
    COLLECTION_NAME = "bookmarks"

    @classmethod
    async def add(cls, user_uuid, bookmark: Bookmark):
        collection = await cls.get_collection()
        result = await collection.insert_one(
            {
                "user": user_uuid,
                "movie": str(bookmark.movie),
                "time": datetime.datetime.now(),
            }
        )
        return result

    @classmethod
    async def remove(cls, user_uuid, bookmark: Bookmark):
        collection = await cls.get_collection()
        result = await collection.delete_one({"user": user_uuid, "movie": str(bookmark.movie)})
        return result

    @classmethod
    async def list(cls, movie, user_id):
        collection = await cls.get_collection()
        query = {"movie": str(movie.id), 'user': str(user_id)}
        objects = collection.find(query).sort("time", 1)
        objects_list = [
            {
                "user": r["user"],
                "movie": r["movie"],
                "id": str(r["_id"]),
                "time": str(r["time"]),
            }
            async for r in objects
        ]
        return objects_list
