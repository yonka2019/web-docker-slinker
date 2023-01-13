from DBManager import DBManager
from CacheManager import CacheManager


class SlinkManager:  # Slink management (sqlite + cache + msg)
    @staticmethod
    def get_original_link(short_url):
        cache_original_link = CacheManager.get_original_link(short_url)

        if cache_original_link:  # if cache have
            return cache_original_link
        else:  # if cache don't have the short url -> check in main DB
            db_original_link = DBManager.get_original_link(short_url)

            if db_original_link:  # if DB have this short link, save it in cache for future requests
                CacheManager.add_link(short_url, db_original_link)

            return db_original_link

    @staticmethod
    def is_link_exist(short_url):
        cache_link_exist = CacheManager.is_link_exist(short_url)

        if cache_link_exist:  # already have in cache -> so also have in the DB (not necessary to check there)
            return True
        else:  # not in cache, maybe in DB?
            db_link_exist = DBManager.is_link_exist(short_url)

            return db_link_exist

    @staticmethod
    def add_link(short_url, original_url):
        DBManager.add_link(short_url, original_url)  # add in DB
