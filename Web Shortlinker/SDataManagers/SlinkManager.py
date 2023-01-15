import logging
logging.basicConfig(level=logging.INFO)

import sys
sys.path.append('SDataManagers')  # python imports from /app (relative path is /app), this will make him to import from /app/SDataManagers

from DBManager import DBManager
from CacheManager import CacheManager


class SlinkManager:  # Slink management (sqlite + cache + msg)
    @staticmethod
    def get_original_link(short_url):
        cache_original_link = CacheManager.get_original_link(short_url)

        if cache_original_link:  # if cache have
            logging.info(" [CACHE] Found original link in cache")
            return cache_original_link

        else:  # if cache not have the short url -> check in main DB
            logging.info(" [CACHE] Original link couldn't be found in cache (checking in DB)")
            db_original_link = DBManager.get_original_link(short_url)

            if db_original_link:  # if DB have this short link, save it in cache for future requests
                CacheManager.add_link(short_url, db_original_link)
                logging.info(" [DB] Found original link in DB, saved to cache")
            else:
                logging.info(" [DB] Original link couldn't be found in DB")  # db_original_link will be None

            return db_original_link

    @staticmethod
    def is_link_exist(short_url):
        cache_link_exist = CacheManager.is_link_exist(short_url)

        if cache_link_exist:  # already have in cache -> so also have in the DB (not necessary to check there)
            logging.info(" [CACHE] Link already exist in cache (exist in DB for sure)")
            return True

        else:  # not in cache, maybe in DB?
            logging.info(" [CACHE] Link doesn't exist in cache (checking in DB)")
            db_link = DBManager.is_link_exist(short_url)

            if db_link:
                logging.info(f" [DB] Link already exist in DB ['{short_url}' : '{db_link}']")
                return True
            else:
                logging.info(" [DB] Link doesn't exist in DB")
                return False

    @staticmethod
    def add_link(short_url, original_url):
        DBManager.add_link(short_url, original_url)  # add in DB
