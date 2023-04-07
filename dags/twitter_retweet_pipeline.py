import json
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from utils.twitter_retweet import TwitterRetweet
from utils.news_api import DailyNews
from utils.chat_gpt import ChatGpt
import random

def logData(message):
    if message is not None:
        print(message)
    else:
        print("No message provided")

@dag(
    schedule_interval="0 */3 * * *",
    start_date=datetime(2023,4,4),
    catchup=False,
    default_args={
        "retries": 2, 
    },
    tags=['twitter','status','morning', 'tweet'])

def twitter_retweet_pipeline():
    @task
    def kickOff():
        from datetime import datetime
        return dict(job_start_timestamp=datetime.today().strftime('%Y-%m-%d'))
    
    @task()
    def retweet(job_details):
        retweet_topics = ["#bitcoin","#btc","#dating","#crypto","#eth","#ethereum","#chatgpt"]
        twitter_client = TwitterRetweet()
        is_retweeted = twitter_client.retweet(random.choice(retweet_topics))
        logData(is_retweeted)
        return is_retweeted

    is_posted = retweet(kickOff())

twitter_retweet_pipeline()