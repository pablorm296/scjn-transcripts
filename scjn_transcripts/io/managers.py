from pymongo.asynchronous.database import AsyncDatabase
from pymongo import AsyncMongoClient
from redis import Redis

from scjn_transcripts.models.cleaner.transcript import Transcript
from scjn_transcripts.config import CONFIG

class CacheManager:
    def __init__(self, cache_client: Redis):
        pass
    
class MongoManager:
    db: AsyncDatabase

    def __init__(self, mongo_client: AsyncMongoClient):
        self.mongo_client = mongo_client
        self.db = mongo_client[CONFIG.mongo.database]

    async def get_documents(self, query: dict) -> list[Transcript]:
        """Get all cleaned documents that match the query

        Args:
            query (dict): A valid MongoDB query

        Returns:
            list[Transcript]: A list of cleaned documents
        """

        documents = self.db.transcripts_clean.find(query)
        documents = await documents.to_list(length = None)
        return [Transcript(**document) for document in documents]