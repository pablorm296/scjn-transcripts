import redis

from scjn_transcripts.config import CONFIG

class RedisFactory:
    @staticmethod
    def create():
        return redis.Redis(
            host = CONFIG.cache.host,
            port = CONFIG.cache.port,
            password = CONFIG.cache.password,
            decode_responses = True
        )