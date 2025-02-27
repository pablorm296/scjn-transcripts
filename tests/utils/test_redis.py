from typing import Generator
from redis import Redis
import pytest

from scjn_transcripts.utils.redis import RedisFactory

# Fixture: yield MongoClientFactory.create(), then close the client
@pytest.fixture(scope = 'module')
def redis_client() -> Generator[Redis, None]:
    """Create a MongoDB client and yield it to the test, then delete the test database and close the client"""

    client = RedisFactory.create()
    yield client

    # Delete all keys with the test prefix
    keys = client.keys('test*')
    for key in keys:
        client.delete(key)

def test_redis_client(redis_client: Redis):
    """Test the creation of a Redis client"""

    assert redis_client is not None

def test_redis_set_get(redis_client: Redis):
    """Test setting and getting a key-value pair in Redis"""

    key = 'test:123'
    value = 'test_value'

    redis_client.set(key, value)
    assert redis_client.get(key) == value

def test_redis_hash(redis_client: Redis):
    """Test setting and getting a hash in Redis"""

    key = 'test:hash'
    mapping = {
        'field1': 'value1',
        'field2': 'value2'
    }

    redis_client.hset(key, mapping = mapping)
    assert redis_client.hgetall(key) == mapping
