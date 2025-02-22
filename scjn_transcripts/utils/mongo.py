from pymongo import AsyncMongoClient

from scjn_transcripts.config import CONFIG

class MongoClientFactory:

    @staticmethod
    def build_connection_string():
        return f"mongodb://{CONFIG.mongo.user}:{CONFIG.mongo.password}@{CONFIG.mongo.host}:{CONFIG.mongo.port}"

    @staticmethod
    async def create():
        mongo_uri = MongoClientFactory.build_connection_string()

        return AsyncMongoClient(mongo_uri)