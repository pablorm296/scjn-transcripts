from pymongo.asynchronous.database import AsyncDatabase
from pymongo import AsyncMongoClient
from redis import Redis

from scjn_transcripts.models.collector.response.document import DocumentDetailsResponse
from scjn_transcripts.config import CONFIG

class CacheManager:
    def __init__(self, cache_client: Redis):
        self.cache_client = cache_client

    def set_search_page(self, page: int):
        self.cache_client.set("scjn_transcripts:search_page", page)

    def get_search_page(self) -> int:
        page = self.cache_client.get("scjn_transcripts:search_page")
        return int(page) if page else 1

    def set_document_details(self, id: str, digest: str):
        mapping = {"id": id, "digest": digest}
        self.cache_client.hset(f"scjn_transcripts:document_details:{id}", mapping = mapping)

    def check_document_details(self, id: str) -> bool | str:
        exists = self.cache_client.exists(f"scjn_transcripts:document_details:{id}")
        if exists:
            mapping = self.cache_client.hgetall(f"scjn_transcripts:document_details:{id}")
            return mapping["digest"]
        return False
    
class MongoManager:
    db: AsyncDatabase

    def __init__(self, mongo_client: AsyncMongoClient):
        self.mongo_client = mongo_client
        self.db = mongo_client[CONFIG.mongo.database]

    async def save_document_details(self, document_details: DocumentDetailsResponse):
        result = await self.db.transcripts.insert_one(document_details.model_dump())
        return result.inserted_id

    async def patch_document_details(self, document_details: DocumentDetailsResponse) -> int:
        result = await self.db.transcripts.update_one(
            {"id": document_details.id},
            {"$set": document_details.model_dump()}
        )
        return result.modified_count