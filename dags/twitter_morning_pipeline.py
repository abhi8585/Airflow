import json
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from utils.twitter_status_update import TwitterStatusUpdate
from utils.news_api import DailyNews
from utils.chat_gpt import ChatGpt

def logData(message):
    if message is not None:
        print(message)
    else:
        print("No message provided")

@dag(
    schedule_interval="30 4 * * *",
    start_date=datetime(2023,4,4),
    catchup=False,
    default_args={
        "retries": 2, 
    },
    tags=['twitter','status','morning', 'tweet'])

def twitter_morning_update():
    @task
    def kickOff():
        from datetime import datetime
        return dict(job_start_timestamp=datetime.today().strftime('%Y-%m-%d'))

    @task
    def get_daily_news(job_details):
        news_client = DailyNews()
        # TODO :  need to pass trending topic after getting from twitter
        daily_news_title = news_client.get_article_title(topic="crypto")
        job_details["daily_news_title"] = daily_news_title
        return job_details

    @task
    def generate_tweet_content(job_details):
        try:
            chat_gpt_client = ChatGpt()
            article_title = job_details["daily_news_title"]
            # TODO : keep hashtags dynamic
            prompt = f"""
        Generate a morning tweet with hashtags #datewithcrypto and #cryptocoffee.
        "The tweet should be crisp, wishing good morning with some crypto news, and based on the context '{article_title}'. "
        "End some relevant hashtags at the end of tweet"
         "Limit the tweet to 220 characters."
                    """  
            job_details["tweet_content"] = chat_gpt_client.generate_content(prompt=prompt)
            return job_details
        except Exception as e:
            logData(e)
            job_details["tweet_content"] = ""
            return job_details
    
    @task()
    def tweet_morning_status(job_details):
        tweet_content = job_details["tweet_content"]
        logData(f"{tweet_content} tweet to post from morning pipeline")
        ins = TwitterStatusUpdate()
        is_posted = ins.tweet_text(tweet_content)
        logData(f"{tweet_content} posted from morning pipeline")
        return is_posted

    is_posted = tweet_morning_status(generate_tweet_content(get_daily_news(kickOff())))

twitter_morning_update()