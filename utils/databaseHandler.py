# 数据库的相关操作
import sqlite3
from config import config
from utils.fileHandler import FileHandler
from utils.logger import logger
from utils.tools import tools


class DatabaseHandler(object):
    def __init__(self):
        self.database_path = config.DATABASE_PATH
        self.database_setup_path = config.DATABASE_SETUP_PATH
        # 要先测试数据库存在还是不存在
        if not FileHandler.check_file_exists(self.database_path):
            # sqlite3 建立连接conn
            self.conn = sqlite3.connect(self.database_path)
            # 生成操作游标cursor
            self.cursor = self.conn.cursor()
            # 如果数据库不存在的话就创建数据库
            sql_setup_command = FileHandler.read_file(self.database_setup_path)

            # 初始化数据库
            self.cursor.executescript(sql_setup_command)
            # 保存修改
            self.conn.commit()

            logger.info("初始化数据库成功")

        # 数据库已经存在了
        else:
            # sqlite3 建立连接conn
            self.conn = sqlite3.connect(self.database_path)
            # 生成操作游标cursor
            self.cursor = self.conn.cursor()

    # rss_url 增加
    def add_rss_url(
            self,
            url: str,
            desc: str,
            status: bool
    ):
        sql = "INSERT OR REPLACE INTO rss_url (url, desc, status, last_update) VALUES (?,?,?,?)"
        data = (url, desc, str(status), tools.get_date())
        logger.info(f"{sql} {data}")
        self.cursor.execute(
            sql, data
        )
        self.save()

    # rss_url删除
    def del_rss_url(
            self,
            url: str
    ):
        sql = "DELETE FROM rss_url WHERE url=?"
        data = (url,)
        logger.info(f"{sql} {data}")
        self.cursor.execute(
            sql, data
        )
        self.save()

    # rss_url修改
    def update_rss_url(
            self,
            old_url: str,
            new_url: str,
            new_desc: str,
            new_status: bool
    ):
        sql = "UPDATE rss_url set url=?, desc=?, status=?, last_update=? where url=?"
        data = (new_url, new_desc, str(new_status), tools.get_date(), old_url)
        logger.info(f"{sql} {data}")
        self.cursor.execute(
            sql, data
        )
        self.save()

    # rss_url查询 所有
    def get_all_rss_url(
            self
    ) -> list:
        sql = "SELECT * from rss_url"
        logger.info(sql)
        self.cursor.execute(
            sql
        )

        return self.cursor.fetchall()

    # rss_url查询包含的关键词
    def search_rss_url(
            self,
            keyword: str
    ) -> list:
        sql = f"SELECT * FROM rss_url WHERE url LIKE '%{keyword}%' OR " \
              f"`desc` LIKE '%{keyword}%' OR " \
              f"status LIKE '%{keyword}%' OR " \
              f"last_update LIKE '%{keyword}%'"
        self.cursor.execute(
            sql
        )

        return self.cursor.fetchall()

    # data增加新数据
    def add_rss_news(
            self,
            url: str,
            title: str,
            detail_url: str,
            published: str
    ):
        sql = f"INSERT OR REPLACE INTO rss_news (url, title, detail_url, published, last_update) VALUES (?,?,?,?,?)"
        logger.info((url, title, detail_url, published, tools.get_date()))

        self.cursor.execute(
            sql, (url, title, detail_url, published, tools.get_date())
        )

        self.save()

    # data删除(无需实现删除)

    # data修改(无需实现修改)

    # data查询包含的关键词
    def search_rss_news(
            self,
            keyword: str
    ) -> list:
        sql = f"SELECT * FROM rss_news WHERE " \
              f"url LIKE '%{keyword}%' OR " \
              f"title LIKE '%{keyword}%' OR " \
              f"published LIKE '%{keyword}%' OR " \
              f"detail_url LIKE '%{keyword}%'"
        logger.info(f"{sql}")
        self.cursor.execute(
            sql
        )
        return self.cursor.fetchall()

    # rss_notice关键词 添加
    def add_notice_keywords(self, keyword: str):
        sql = "INSERT OR REPLACE INTO notice_keywords (keyword, last_update) VALUES (?,?)"
        data = (keyword, tools.get_date())
        logger.info(f"{sql} {data}")
        self.cursor.execute(
            sql, data
        )
        self.save()

    def del_notice_keywords(self, keyword):
        sql = "DELETE FROM notice_keywords WHERE keyword=?"
        data = (keyword,)
        logger.info(f"{sql} {data}")
        self.cursor.execute(
            sql, data
        )
        self.save()

    def update_notice_keywords(self, old_keyword, new_keyword):
        sql = "UPDATE notice_keywords SET keyword=?, last_update=? WHERE keyword=?"
        data = (new_keyword, tools.get_date(), old_keyword)
        logger.info(f"{sql} {data}")
        self.cursor.execute(
            sql, data
        )
        self.save()

    def search_notice_keywords(self, keyword: str):
        sql = f"SELECT * FROM notice_keywords WHERE " \
              f"keyword LIKE '%{keyword}%' OR " \
              f"last_update LIKE '%{keyword}%'"
        logger.info(f"{sql}")
        self.cursor.execute(
            sql
        )
        return self.cursor.fetchall()

    def get_all_notice_keywords(self):
        sql = "SELECT * from notice_keywords"
        logger.info(sql)
        self.cursor.execute(
            sql
        )

        return self.cursor.fetchall()

    def add_notice_history(
            self,
            keyword: str,
            title: str,
            detail_url: str
    ):
        sql = f"INSERT OR REPLACE INTO notice_history (keyword, title, detail_url, last_update) VALUES (?,?,?,?)"
        logger.info((keyword, title, detail_url, tools.get_date()))

        self.cursor.execute(
            sql, (keyword, title, detail_url, tools.get_date())
        )

        self.save()

    def register(self, username, password):
        sql = "INSERT INTO users (username, password, last_update) VALUES (?,?,?)"
        data = (username, password, tools.get_date())
        logger.info(f"{sql} {data}")
        self.cursor.execute(
            sql, data
        )
        self.save()

    def check_user(self, username: str):
        sql = "select count(username) from users where username=?"
        self.cursor.execute(
            sql, (username,)
        )
        if self.cursor.fetchall()[0][0] == 0:
            print(False)
            return False
        else:
            print(True)
            return True

    def login(self, username):
        sql = "select password from users where username=?"
        self.cursor.execute(
            sql, (username,)
        )
        return self.cursor.fetchall()

    def query(self, query: str):
        self.cursor.execute(
            query
        )

        return self.cursor.fetchall()


    def save(self):
        self.conn.commit()
        self.conn.close()