from pymongo import AsyncMongoClient
from typing import AsyncGenerator
import pytest_asyncio
import pytest

from scjn_transcripts.utils.mongo import MongoClientFactory

# Fixture: yield MongoClientFactory.create(), then close the client
@pytest_asyncio.fixture(scope = 'module')
async def mongo_client() -> AsyncGenerator[AsyncMongoClient, None]:
    """Create a MongoDB client and yield it to the test, then delete the test database and close the client"""

    client = await MongoClientFactory.create()
    yield client

    # Delete the test database
    await client.drop_database('test_db')

    # Close the client
    await client.close()

@pytest.mark.asyncio
async def test_mongo_client(mongo_client: AsyncMongoClient):
    """Test the creation of a MongoDB client"""

    assert mongo_client is not None

@pytest.mark.asyncio
async def test_mongo_collection(mongo_client: AsyncMongoClient):
    """Test the creation of a MongoDB collection"""

    collection = mongo_client['test_db']['test_collection']
    assert collection is not None

@pytest.mark.asyncio
async def test_mongo_insert_one(mongo_client: AsyncMongoClient):
    """Test inserting a document into a MongoDB collection"""

    collection = mongo_client['test_db']['test_collection']
    result = await collection.insert_one({'test': 'test_value'})
    assert result.acknowledged