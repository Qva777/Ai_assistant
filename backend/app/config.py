import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TOKEN = os.getenv("TOKEN")

    url_search_usr = "https://flaidata.tiktok-alltrends.com:442/api/datapoint/authors?Search="
    url_search_usr_id = "https://flaidata.tiktok-alltrends.com:442/api/datapoint/author?authorId="
    url_base_video = "https://www.tiktok.com/@/video/"
    url_sound = "https://flaidata.tiktok-alltrends.com:442/api/datapoint/sounds?sorting=rat&Category=100&Days="
