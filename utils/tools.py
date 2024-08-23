# 获取当前时间戳 毫秒级别
import time
import datetime
import jwt


class Tools:
    @staticmethod
    def timestamp() -> str:
        return str(round(time.time() * 1000))

    @staticmethod
    def get_now_date() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_now_time() -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def get_now_date_and_time() -> str:
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def get_date() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_x_day_ago(i: int) -> str:
        day = ((datetime.datetime.now()) + datetime.timedelta(days=i)).strftime("%Y-%m-%d 00:00:00")
        return day

    @staticmethod
    def gmt_to_date(gmt: str):
        # Sat, 11 Jun 2022 06:37:00 GMT
        #
        if "GMT" in gmt:
            gmt_format = "%a, %d %b %Y %H:%M:%S GMT"
        elif "+0800" in gmt:
            gmt_format = "%a, %d %b %Y %H:%M:%S +0800"
        else:
            return gmt

        return datetime.datetime.strptime(gmt, gmt_format)

    @staticmethod
    def get_token(username=None):
        # exp过期时间 1小时
        token_dict = {
            "exp": int(Tools.timestamp()) + int(1000 * 60 * 60),
            "username": str(username)
        }
        return jwt.encode(token_dict, 'TT', algorithm='HS256')

    @staticmethod
    def check_token(token):
        if token["exp"] <= int(Tools.timestamp()):
            return False
        else:
            return True


tools = Tools()
