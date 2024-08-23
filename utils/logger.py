# 一个生成日志的模块
from config import config
from utils.fileHandler import FileHandler
from utils.tools import Tools


class Logger:
    def __init__(self):
        # 初始化日志文件
        if not FileHandler.check_file_exists(config.LOG_DIR):
            # 没有日志文件夹就创建一个日志文件夹
            FileHandler.mkdir(config.LOG_DIR)

    def info(self, context):
        info = f"[Info] {Tools.get_date()} {context}"
        print(info)
        if config.LOG_LEVEL == "info":
            self._write(info)

    def error(self, context):
        print("////" * 20)
        error = f"[ERROR] {Tools.get_date()} {context}"
        print(error)
        print("////" * 20)
        if config.LOG_LEVEL == "error":
            self._write(error)

    @staticmethod
    def _write(context):
        file_name = Tools.get_now_date() + ".log"
        file_path = FileHandler.join(FileHandler.get_path(), config.LOG_DIR)
        file_path = FileHandler.join(file_path, file_name)

        FileHandler.write_file(file_path, context)


logger = Logger()
