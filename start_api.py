import os
import sys

import jwt
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.databaseHandler import DatabaseHandler
from utils.fileHandler import FileHandler
from utils.tools import tools
from collections import Counter
import jieba
import re
from fastapi import Body


name = os.path.basename(sys.argv[0]).split(".")[0]
app = FastAPI()

origins = ["*"]

# 3、配置 CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)


@app.get('/api/home')
async def home():
    news_count = DatabaseHandler().query("select count(1) from rss_news")[0][0]
    news_count_day = DatabaseHandler().query(f"select count(1) from rss_news where last_update BETWEEN '{tools.get_now_date()} 00:00:00' AND '{tools.get_now_date()} 23:59:59'")[0][0]
    sub_live = DatabaseHandler().query(f"select count(1) from rss_url where status='True'")[0][0]
    sub_total = DatabaseHandler().query(f"select count(1) from rss_url")[0][0]
    run_day = len(DatabaseHandler().query(f"select * from rss_news GROUP BY strftime('%Y-%m-%d', last_update)"))
    keyword_times = DatabaseHandler().query(f"select count(1) from notice_history")[0][0]
    sub_update_time = tools.get_now_time()

    if not news_count_day:
        news_count_day = 666

    return {
        'news_count': news_count,
        "news_count_day": news_count_day,
        "sub_live": sub_live,
        "sub_total": sub_total,
        "run_day": run_day,
        "keyword_times": keyword_times,
        "sub_update_time": sub_update_time
    }

@app.get('/api/word_cloud_data')
async def word_cloud_data(range: str, num: int):
    print(range, num)
    if not num:
        num = 30
    range_map = {
        "所有": -30000,
        "一年": -365,
        "半年": -180,
        "一季度": -90,
        "一月": -31,
        "一周": -7,
        "一天": -1
    }
    ago = range_map.get(range, -1)
    # word_cloud_data
    word_cloud_data = DatabaseHandler().query(
        f"select title from rss_news where last_update > '{tools.get_x_day_ago(ago)}'")
    words = ""
    for i in word_cloud_data:
        words += i[0]
    words = re.sub('([^\u4e00-\u9fa5\u0030-\u0039])', '', words)
    words = re.sub(r'[0-9]+', '', words)
    text_cut = jieba.lcut(words)
    stopWords = FileHandler().read_file("assets/stopWords.txt")
    stopWords = stopWords.split("\n")
    word_cloud_data = []
    for i in text_cut:
        if str(i) not in stopWords:
            if len(str(i)) > 1:
                word_cloud_data.append(i)

    word_cloud_data = Counter(word_cloud_data).most_common(num)
    word_cloud_data_list = []
    for i in word_cloud_data:
        keyword, count = i
        word_cloud_data_list.append({"name": keyword, "value": count})

    return word_cloud_data_list

@app.get('/api/news_line_chart_data')
async def news_line_chart_data(period: str, range: str):
    print(period, range)
    period_map = {
        "年": "%Y",
        "月": "%Y-%m",
        "日": "%Y-%m-%d",
        "时": "%Y-%m-%d %H",
        "分": "%Y-%m-%d %H:%M",
        "秒": "%Y-%m-%d %H:%M:%S",
    }

    range_map = {
        "所有": -30000,
        "一年": -365,
        "半年": -180,
        "一季度": -90,
        "一月": -31,
        "一周": -7,
        "一天": -1
    }
    ago = range_map.get(range, -30000)
    strftime = period_map.get(period, "%Y-%m-%d")
    sql = f"select strftime('{strftime}', last_update), count(title) from rss_news where last_update > '{tools.get_x_day_ago(ago)}' group by strftime('{strftime}', last_update) order by last_update desc "
    # print(sql)
    data = DatabaseHandler().query(
        sql
    )
    # print(data)
    x, y = [], []
    for r in data:
        t, n = r
        # t = t.split(" ")[0]
        x.append(t)
        y.append(n)

    x.reverse()
    y.reverse()
    data = {
        "x": x,
        "y": y
    }
    print(data)
    return data

@app.get('/api/search_news/{keywords}')
async def search_news(keywords: str):
    sql = f"select title, detail_url, rss_news.last_update, rss_url.desc from rss_news " \
          f"left join rss_url on rss_news.url = rss_url.url where " \
          f"title like '%{keywords}%' or " \
          f"'desc' like '%{keywords}%' order by rss_news.last_update desc"
    search_news = DatabaseHandler().query(
        sql
    )

    data = []
    for i in search_news:
        data.append(
            {
                "title": i[0],
                "detail_url": i[1],
                "last_update": i[2],
                "desc": i[3]
            }
        )
    return data

@app.get('/api/search_news_line_chart')
async def search_news_line_chart(keywords: str, limit: int = 30):
    sql = f"select last_update, count(title) from rss_news where " \
          f"title like '%{keywords}%' or " \
          f"'desc' like '%{keywords}%' " \
          f"group by strftime('%Y-%m-%d', last_update) " \
          f"order by last_update desc"

    search_news_line_chart_data = DatabaseHandler().query(
        sql
    )
    data_x = []
    data_y = []
    for i in search_news_line_chart_data:
        data_x.append(i[0].split(" ")[0])
        data_y.append(i[1])

    data_x.reverse()
    data_y.reverse()

    return {
        "x": data_x,
        "y": data_y
    }

@app.get('/api/rss_url')
async def rss_url():
    datas = DatabaseHandler().query(f"select url, desc, status, last_update from rss_url")
    data = []
    for i in datas:
        data.append(
            {
                "rss_url": i[0],
                "rss_desc": i[1],
                "status": "在线" if i[2] == "True" else "离线",
                "rss_time": i[3]
            }
        )
    data.reverse()
    return data

@app.post('/api/rss_url')
async def rss_url(rss_url=Body(None), rss_desc=Body(None)):
    print(rss_url, rss_desc)
    if not rss_desc or not rss_url:
        return {"status": "no"}
    if "http" in str(rss_url):
        pass
    else:
        return {"status": "no"}
    try:
        DatabaseHandler().add_rss_url(url=rss_url, desc=rss_desc, status=False)
    except Exception as e:
        print(e)
        return {"status": "no"}
    else:
        return {"status": "ok"}

@app.post('/api/rss_url_del')
async def rss_url_del(rss_url=Body(None)):
    rss_url = rss_url["rss_url"]
    try:
        DatabaseHandler().del_rss_url(url=rss_url)
        DatabaseHandler().query(f'delete from rss_news where url = "{rss_url}"')
        print(f'delete from rss_news where url = "{rss_url}"')
    except Exception as e:
        print(e)
        return {"status": "no"}
    else:
        return {"status": "ok"}


@app.post('/api/keyword')
async def keyword(keyword=Body(None)):
    keyword = keyword["keyword"]
    if not keyword:
        return {"status": "no"}
    try:
        DatabaseHandler().add_notice_keywords(keyword=keyword)
    except Exception as e:
        print(e)
        return {"status": "no"}
    else:
        return {"status": "ok"}

@app.post('/api/keyword_del')
async def keyword(keyword=Body(None)):
    keyword = keyword["keyword"]
    try:
        DatabaseHandler().del_notice_keywords(keyword=keyword)
    except Exception as e:
        print(e)
        return {"status": "no"}
    else:
        return {"status": "ok"}

@app.get('/api/keyword')
async def keyword():
    datas = DatabaseHandler().get_all_notice_keywords()
    data = []
    for i in datas:
        data.append({"keyword": i[0], "time": i[1]})
    return data

@app.get('/api/news')
async def news():
    days_7_line_data = DatabaseHandler().query(
        f"select detail_url, title, last_update, url from rss_news order by last_update desc limit 50"
    )
    rss_url = DatabaseHandler().get_all_rss_url()
    rss_url_dict = {}
    for i in rss_url:
        url, desc, status, update_time = i
        rss_url_dict[url] = desc

    data = []
    for i in days_7_line_data:
        detail_url, title, update_time, url = i
        data.append({
            "title": title,
            "detail_url": detail_url,
            "update_time": update_time,
            "desc": rss_url_dict[url]
        })
    return data


@app.get('/api/notice_keyword_pie_data')
async def notice_keyword_pie_data():
    datas = DatabaseHandler().query(
        f"select keyword, count(keyword) from notice_history group by keyword"
    )
    data = []
    for i in datas:
        data.append(
            {"value": i[1], "name": i[0]}
        )
    return data

@app.get('/api/test')
async def notice_keyword_pie_data():
    return {
        "y": [150, 230, 224, 218, 135, 147, 260],
        "x": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    }

@app.post('/api/login')
async def login(username: str, password: str):
    # 解密

    res = DatabaseHandler().login(username)
    if not res:
        return {
            "status": False
        }
    if password == res[0][0]:
        print(tools.get_token(username))
        return {
            "status": True,
            "token": tools.get_token(username)
        }
    else:
        return {"status": False}

@app.post('/api/checklogin')
async def checklogin(token: str):
    token = jwt.decode(token, 'TT', algorithms='HS256')
    if tools.check_token(token) and DatabaseHandler().check_user(token["username"]):
        return {"status": True}
    else:
        return {"status": False}

@app.post('/api/register')
async def register(username: str, password: str):
    try:
        DatabaseHandler().register(username, password)
    except Exception as e:
        # print(e)
        return {"status": False}
    else:
        return {"status": True}

if __name__ == '__main__':
    uvicorn.run(app=f"{name}:app", debug=True)
