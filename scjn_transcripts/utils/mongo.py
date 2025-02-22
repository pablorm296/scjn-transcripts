from pymongo import AsyncMongoClient
from scjn_transcripts.config import CONFIG

class MongoClientFactory:
    
    @staticmethod
    async def create():
        return AsyncMongoClient(
            host = CONFIG.mongo.host,
            port = CONFIG.mongo.port,
            username = CONFIG.mongo.user,
            password = CONFIG.mongo.password,
            database = CONFIG.mongo.database
        )