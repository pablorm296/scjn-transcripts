from pymongo import AsyncMongoClient
from redis import Redis

import scjn_transcripts.collector.managers as collector_managers
import scjn_transcripts.cleaner.managers as cleaner_managers

from scjn_transcripts.utils.mongo import MongoClientFactory
from scjn_transcripts.utils.redis import RedisFactory
from scjn_transcripts.logger import logger

type CacheManagerType = collector_managers.CacheManager | cleaner_managers.CacheManager
type MongoManagerType = collector_managers.MongoManager | cleaner_managers.MongoManager

class BaseDataHandler:
    cache_client: Redis | None = None
    mongo_client: AsyncMongoClient | None = None
    cache_manager: CacheManagerType
    mongo_manager: MongoManagerType

    def __init__(self):
        pass

    def __init_cache_client(self):
        """Initialize the Redis cache client."""
        self.cache_client = RedisFactory.create()

    async def __init_mongo_client(self):
        """Initialize the MongoDB client."""
        self.mongo_client = await MongoClientFactory.create()

    def __check_cache_client(self):
        """Check if the cache client is initialized."""
        if self.cache_client is None:
            raise ValueError("Cache client not initialized")
        
    def __check_mongo_client(self):
        """Check if the MongoDB client is initialized."""
        if self.mongo_client is None:
            raise ValueError("Mongo client not initialized")
        
    def __check_connection_clients(self):
        """Check if both the cache and MongoDB clients are initialized."""
        self.__check_cache_client()
        self.__check_mongo_client()

    def __init_cache_manager(self, manager_class: CacheManagerType):
        """Initialize the CacheManager."""
        self.cache_manager = manager_class(self.cache_client)

    def __init_mongo_manager(self, manager_class: MongoManagerType):
        """Initialize the MongoManager."""
        self.mongo_manager = manager_class(self.mongo_client)

    async def connect(self):
        """Connect to DB and cache clients."""
        logger.debug("Connecting to DB and cache clients")
        await self.__init_mongo_client()
        self.__init_cache_client()
        self.__init_cache_manager()
        self.__init_mongo_manager()

    async def close(self):
        """Close the connection to the DB and cache clients."""
        logger.debug("Closing DB and cache clients")
        self.__check_connection_clients()
        await self.mongo_client.close()
        self.cache_client.close()

