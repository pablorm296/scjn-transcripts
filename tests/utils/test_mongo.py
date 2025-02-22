import pytest

from scjn_transcripts.utils.mongo import MongoClientFactory

@pytest.mark.asyncio
async def test_create_mongo_client():
    # Create
    client = await MongoClientFactory.create()
    # Assert
    assert client is not None
