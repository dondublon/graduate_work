from typing import Optional

from core.config import settings
from db.mongo import get_mongo_client


class ServiceMongo:
    # Make as a mixin?
    # Don't use directly, only descendants with shadowed Mongo specific.
    COLLECTION_NAME: Optional[str] = None

    @classmethod
    async def get_collection(cls, name=None):
        client = await get_mongo_client()
        db = client[settings.db_name]
        collection = db.get_collection(name or cls.COLLECTION_NAME)
        return collection
