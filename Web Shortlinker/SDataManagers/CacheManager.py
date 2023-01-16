import redis

REDIS_HOST = "cache-slink"
REDIS_PORT = 6379
REDIS_DB = 0


class CacheManager:  # Redis management
    @staticmethod
    def get_original_link(short_url):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        decoded_original_url = ""

        original_url = r.get(short_url)

        if original_url:
            decoded_original_url = original_url.decode()  # .decode() exist and works..

        r.connection_pool.disconnect()
        return decoded_original_url

    @staticmethod
    def is_link_exist(short_url):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        link_exist = r.exists(short_url)

        r.connection_pool.disconnect()
        return link_exist

    @staticmethod
    def add_link(short_url, original_url):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        r.set(short_url, original_url)
        r.save()

        r.connection_pool.disconnect()
