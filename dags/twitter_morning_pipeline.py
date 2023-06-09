import json
from datetime import datetime, timedelta
from airflow.decorators import task
from utils.twitter_status_update import TwitterStatusUpdate
from utils.news_api import DailyNews
from utils.chat_gpt import ChatGpt
from airflow.models import Variable
from airflow import DAG

def logData(message):
    if message is not None:
        print(message)
    else:
        print("No message provided")


with DAG('twitter_morning_pipeline',default_args={"retries": 2},
        schedule_interval="30 4 * * *",start_date=datetime(2023,4,27)) as dag:
    @task
    def kickOff():
        from datetime import datetime
        return dict(job_start_timestamp=datetime.today().strftime('%Y-%m-%d'))

    @task
    def get_daily_news(job_details):
        logData(f"Received input : {job_details}")
        api_key = Variable.get("news_api_key")
        news_client = DailyNews(api_key=api_key)
        daily_news_title = news_client.get_article_title(topic="crypto")
        logData(daily_news_title)
        job_details["daily_news_title"] = daily_news_title
        return job_details

    @task
    def generate_tweet_content(job_details):
        logData(f"Received input : {job_details}")
        try:
            chat_gpt_client = ChatGpt()
            article_title = job_details["daily_news_title"]
            hash_tags = ["#datewithcrypto☀️", "#cryptocoffee☕","#bitcoin₿","#gm"]
            gm_prompt = f"Generate a tweet description to wish good morning"
            gm_tweet_content = chat_gpt_client.generate_tweet_content(gm_prompt)
            news_promt = f"""Generate a tweet based on "{article_title}" """
            news_tweet_content = chat_gpt_client.generate_tweet_content(news_promt)
            tweet_content = gm_tweet_content+'\n'+news_tweet_content+'\n'+" ".join(hash_tags)
            logData(f"tweet_content : {tweet_content}")
            tweet_content = tweet_content.replace("to your followers","")
            tweet_content = tweet_content.replace("to your friends","")
            tweet_content = tweet_content.strip()
            job_details["tweet_content"] = tweet_content
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

    tweet_morning_status(generate_tweet_content(get_daily_news(kickOff())))