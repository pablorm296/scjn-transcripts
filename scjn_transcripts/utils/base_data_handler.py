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
    cache_manager_class: CacheManagerType
    mongo_manager_class: MongoManagerType

    def __init__(self, cache_manager_class: CacheManagerType, mongo_manager_class: MongoManagerType):
        """Initialize the BaseDataHandler instance."""
        self.cache_manager_class = cache_manager_class
        self.mongo_manager_class = mongo_manager_class

    def _init_cache_client(self):
        """Initialize the Redis cache client."""
        self.cache_client = RedisFactory.create()

    async def _init_mongo_client(self):
        """Initialize the MongoDB client."""
        self.mongo_client = await MongoClientFactory.create()

    def _check_cache_client(self):
        """Check if the cache client is initialized."""
        if self.cache_client is None:
            raise ValueError("Cache client not initialized")
        
    def _check_mongo_client(self):
        """Check if the MongoDB client is initialized."""
        if self.mongo_client is None:
            raise ValueError("Mongo client not initialized")
        
    def _check_connection_clients(self):
        """Check if both the cache and MongoDB clients are initialized."""
        self._check_cache_client()
        self._check_mongo_client()

    def _init_cache_manager(self, manager_class: CacheManagerType):
        """Initialize the CacheManager."""
        self.cache_manager = manager_class(self.cache_client)

    def _init_mongo_manager(self, manager_class: MongoManagerType):
        """Initialize the MongoManager."""
        self.mongo_manager = manager_class(self.mongo_client)

    async def connect(self):
        """Connect to DB and cache clients."""
        logger.debug("Connecting to DB and cache clients")
        await self._init_mongo_client()
        self._init_cache_client()

        logger.debug("Initializing cache and DB managers")
        self._init_cache_manager(self.cache_manager_class)
        self._init_mongo_manager(self.mongo_manager_class)

    async def close(self):
        """Close the connection to the DB and cache clients."""
        logger.debug("Closing DB and cache clients")
        self._check_connection_clients()
        await self.mongo_client.close()
        self.cache_client.close()

