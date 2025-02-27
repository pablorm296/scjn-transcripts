from pymongo import AsyncMongoClient
import urllib

from scjn_transcripts.config import CONFIG

class MongoClientFactory:

    @staticmethod
    def build_connection_string():
        escaped_password = urllib.parse.quote(CONFIG.mongo.password)
        escaped_user = urllib.parse.quote(CONFIG.mongo.user)

        return f"mongodb://{escaped_user}:{escaped_password}@{CONFIG.mongo.host}:{CONFIG.mongo.port}"

    @staticmethod
    async def create():
        mongo_uri = MongoClientFactory.build_connection_string()

        return AsyncMongoClient(mongo_uri)