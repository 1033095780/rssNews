# 流程控制
from config import config
from utils.databaseHandler import DatabaseHandler
from utils.requestHandler import requestHandler
from utils.logger import logger
import time


def rss():
    logger.info("启动rss服务")
    while True:
        rss_url_dict = DatabaseHandler().get_all_rss_url()
        for rss_detail in rss_url_dict:
            requestHandler.get_rss(rss_detail[0])

        logger.info(f"等待: {config.UPDATE_INTERVAL}秒")
        time.sleep(config.UPDATE_INTERVAL)
