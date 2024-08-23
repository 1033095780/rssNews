import requests
from config import config


class NoticeHandler:
    @staticmethod
    def send(message):
        url = f'https://maker.ifttt.com/trigger/notice/with/key/{config.IFTTT_TOKEN}'
        post = {'value1': str(message)}
        r = requests.post(url, data=post).text
        if "Congratulations! You've fired the notice event" in r:
            return True
        else:
            return False


noticeHandler = NoticeHandler()
