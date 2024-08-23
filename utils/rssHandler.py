#  处理rss的结构化数据 然后存入数据库 数据清洗 关键词检测等功能件
from utils.databaseHandler import DatabaseHandler
from utils.tools import tools
from utils.logger import logger
from utils.noticeHandler import noticeHandler


class RssHandler:
    def __init__(self):
        self.databaseHandler = DatabaseHandler

    def write_into_database(self, rss_data_list: dict, rss_url: str):
        logger.info(f"开始处理数据: {rss_url}")
        entries = rss_data_list["entries"]
        if not entries:
            raise Exception(f"{rss_url}:空内容错误")
        for entity in entries:
            title = entity["title"]
            if not title:
                # 标题没有数据就忽略
                logger.info(f"无标题的空数据:{entity}")
                continue
            detail_url = entity["link"]
            if not detail_url:
                detail_url = rss_url
                logger.info(f"空详细页url:{entity}")
            published = self._clean_published(entity["published"])

            # 检查是否有重复
            if self.databaseHandler().search_rss_news(keyword=detail_url) or self.databaseHandler().search_rss_news(keyword=title):
                logger.info(f"重复出现:{detail_url}")
                continue

            # 检查是否触发了关键词
            for keyword, last_update in self.databaseHandler().get_all_notice_keywords():
                if str(keyword).upper() in str(title).upper():
                    self.databaseHandler().add_notice_history(
                        keyword=keyword,
                        title=title,
                        detail_url=detail_url
                    )
                    logger.info(f"检测到关键词:{keyword} - {title}")
                    noticeHandler.send(title)

            logger.info(f"开始写入数据库")
            self.databaseHandler().add_rss_news(
                url=rss_url,
                title=title,
                detail_url=detail_url,
                published=published
            )

    @staticmethod
    def _clean_published(context: str):
        return tools.gmt_to_date(context)


rssHandler = RssHandler()
