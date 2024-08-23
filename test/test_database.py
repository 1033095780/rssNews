import os
import unittest
from utils.databaseHandler import DatabaseHandler
from utils.requestHandler import RequestHandler


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("../")
        os.chdir("../")
        print(os.getcwd())
        self.db = DatabaseHandler()

    def test_add_rss_url(self):
        self.db.add_rss_url(
            url="https://ttrss.vercel.app/thepaper/featured",
            desc="澎湃新闻首页头条",
            status=True
        )

    def test_del_rss_url(self):
        self.db.del_rss_url(
            url="www.baidu.com"
        )

    def test_update_rss_url(self):
        self.db.update_rss_url(
            old_url="https://ttrss.vercel.app/thepaper/featured",
            new_url="https://ttrss.vercel.app/thepaper/featured",
            new_desc="澎湃新闻首页头条",
            new_status=True
        )

    def test_get_all_rss(self):
        print(self.db.get_all_rss_url())

    def test_search_rss(self):
        rss_url_list = self.db.search_rss_url(keyword="https://sspai.com/feed")
        print(rss_url_list[0])

    def test_request_rss(self):
        RequestHandler()._request_rss("https://www.zhihu633.com/rss")

    def test_add_rss_notice_keywords(self):
        self.db.add_rss_notice_keywords("佛山")

    def test_del_rss_notice_keywords(self):
        self.db.del_rss_notice_keywords("佛山")

    def test_update_rss_notice_keywords(self):
        self.db.update_rss_notice_keywords(old_keyword="佛山", new_keyword="佛山666")

    def test_search_rss_notice_keywords(self):
        print(self.db.search_rss_notice_keywords("佛山"))

    def test_get_all_rss_notice_keywords(self):
        print(self.db.get_all_rss_notice_keywords())
    # def test_add_data(self):
    #     self.db.add_data(
    #         url="www.baidu.com",
    #         title="高考开始了 语文数学结束了",
    #         content="众所周知 xxxx是高考的好日子xxxxxxx",
    #         detail_url="www.baidu.com/nbnb123123/2333"
    #     )
    #
    # def test_search_data(self):
    #     print(self.db.search_data(keyword="123"))
