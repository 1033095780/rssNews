#  配置文件


class Config:
    def __init__(self):
        # 数据库存放路径
        self.DATABASE_PATH = "database/rssDataBase.db"
        # 初始化数据库sql存放路径
        self.DATABASE_SETUP_PATH = "database/setup.sql"
        # 更新速度 3分钟更新一次
        self.UPDATE_INTERVAL = 180
        # 线程池的并发数
        self.MAX_WORKERS = 6
        # ifttt的token
        self.IFTTT_TOKEN = "bBNLmWQTgwYnbV6dQloKT1"
        # 日志文件夹名字
        self.LOG_DIR = "logs"
        # 日志等级 只有达到error级别到才会记录
        self.LOG_LEVEL = "error"


config = Config()