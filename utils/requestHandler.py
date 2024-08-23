# 只负责发送请求 获取rss源的数据然后交给rssHandler进行处理
from concurrent.futures import ThreadPoolExecutor
from utils.rssHandler import rssHandler
from utils.databaseHandler import DatabaseHandler
from utils.logger import logger
from config import config
import feedparser
import ssl


class RequestHandler:
    def __init__(self):
        # ssl验证要设置一下 不然灰报错
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        self.pool = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)
        self.rssHandler = rssHandler

    def _request_rss(self, rss_url):
        try:
            logger.info(f"开始请求rss_url:{rss_url}")
            rss_data_dict = feedparser.parse(rss_url)
            logger.info(f"请求rss_url成功")
            self.rssHandler.write_into_database(rss_data_dict, rss_url)
        except Exception as e:
            rss_url_list = DatabaseHandler().search_rss_url(rss_url)
            DatabaseHandler().update_rss_url(
                old_url=rss_url_list[0][0], new_url=rss_url_list[0][0],
                new_desc=rss_url_list[0][1], new_status=False
            )

            logger.error(f"{e}\n "
                         f"file:{e.__traceback__.tb_frame.f_globals['__file__']} "
                         f"line:{e.__traceback__.tb_lineno}")

        else:
            rss_url_list = DatabaseHandler().search_rss_url(rss_url)
            DatabaseHandler().update_rss_url(
                old_url=rss_url_list[0][0], new_url=rss_url_list[0][0],
                new_desc=rss_url_list[0][1], new_status=True
            )

    def get_rss(self, rss_url: str):
        self.pool.submit(self._request_rss, (rss_url))
        logger.info(f"pool.submit rss_url:{rss_url}")


requestHandler = RequestHandler()
