from pymongo.asynchronous.database import AsyncDatabase
from pymongo import AsyncMongoClient
from redis import Redis

from scjn_transcripts.models.collector.response.document import DocumentDetailsResponse
from scjn_transcripts.models.cleaner.transcript import Transcript
from scjn_transcripts.config import CONFIG

class CacheManager:
    def __init__(self, cache_client: Redis):
        self.cache_client = cache_client

    def document_exists(self, id: str) -> bool:
        result = self.cache_client.exists(f"scjn_transcripts:document_details:{id}")
        return result == 1

    def get_document_details(self, id: str) -> str:
        mapping = self.cache_client.hgetall(f"scjn_transcripts:document_details:{id}")
        return mapping

    def document_is_cleaned(self, id: str) -> bool:
        document_details = self.get_document_details(id)
        return "cleaned" in document_details
    
    def update_cleaning_status(self, id: str, status: bool):
        document_details = self.get_document_details(id)
        if not document_details:
            raise ValueError(f"Document with id {id} does not exist in cache")
        
        self.cache_client.hset(f"scjn_transcripts:document_details:{id}", "cleaned", status)

        return status
    
class MongoManager:
    db: AsyncDatabase

    def __init__(self, mongo_client: AsyncMongoClient):
        self.mongo_client = mongo_client
        self.db = mongo_client[CONFIG.mongo.database]

    async def get_documents(self, query: dict) -> list[DocumentDetailsResponse]:
        documents = self.db.transcripts.find(query)
        return [DocumentDetailsResponse(**document) for document in documents]
    
    async def save_document(self, document: Transcript):
        result = await self.db.transcripts_clean.insert_one(**document.model_dump())
        return result.inserted_id