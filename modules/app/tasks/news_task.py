import logger
import os
from newsapi import NewsApiClient
from .source_list import news_source
from datetime import date

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


def get_todays_titles(mongo):
    d = date.today()
    d = d.strftime("%Y-%m-%d")
    cursor = mongo.db.news.find({"publishedAt": {"$regex": d}})
    return [document['title'] for document in cursor]


def get_news(mongo):
    LOG.info("inside news")
    try:
        newsapi = NewsApiClient(api_key='223203f6d6024df3ab547aaacd86be12')
        top_headlines = newsapi.get_top_headlines(sources=news_source)
        if top_headlines['status'] == 'ok':
            LOG.info(top_headlines['articles'])
            todays_news_titles = get_todays_titles(mongo)
            if len(todays_news_titles) != 0:
                LOG.info("already news are there for today")
                for news_record in top_headlines['articles']:
                    if(news_record['title'] not in todays_news_titles):
                        mongo.db.news.insert(news_record)
            else:
                LOG.info("no news yet for today")
                mongo.db.news.insert_many(top_headlines['articles'])
        else:
            LOG.error("request failed")
    except Exception as e:
        LOG.error("exception e")
        print("exception is ",e)
    
