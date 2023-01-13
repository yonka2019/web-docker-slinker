import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0


class CacheManager:  # Redis management
    @staticmethod
    def get_original_link(short_url):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        original_url = r.get(short_url)

        r.connection.disconnect()
        return original_url

    @staticmethod
    def is_link_exist(short_url):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        link_exist = r.exists(short_url)

        r.connection.disconnect()
        return link_exist

    @staticmethod
    def add_link(short_url, original_url):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        r.set(short_url, original_url)

        r.connection.disconnect()
