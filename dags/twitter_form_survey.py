from datetime import datetime, timedelta
from airflow.decorators import task
from airflow.models import Variable
from airflow import DAG


from utils.logger import Logger
from utils.errors import Error
from utils.general_utils import GeneralUtils
from utils.twitter.twitter_client import TwitterClient
from utils.chatgpt.chat_gpt import ChatGpt

logger, general_utils, error_client = Logger(), GeneralUtils(), Error()
logdata = logger.log_data



with DAG('twitter_form_survey',default_args={"retries": 2},
        schedule_interval="0 */12 * * *",start_date=datetime(2023,4,27)) as dag:
    
    @task
    def kickOff():
        from datetime import datetime
        job_start_time = general_utils.get_current_timestamp()
        logdata(f"twitter_form_survey job started at {job_start_time}")
        return dict(job_start_timestamp=job_start_time)

    @task
    def get_credentials(job_details):
        try:
            job_details['consumer_key'] = Variable.get("dwc_t_consumer_key")
            job_details['consumer_secret'] = Variable.get("dwc_t_consumer_secret")
            job_details['access_token'] = Variable.get("dwc_t_access_token")
            job_details['access_token_secret'] = Variable.get("dwc_t_access_token_secret")
            job_details['chatgpt_api_key'] = Variable.get("chatgpt_api_key")
        except Exception as e:
            error_client.raise_airflow_exception(f"Failed to get Twitter credentials: {e}")
        return job_details

    @task
    def get_hashtags(job_details):
        try:
            twitter_client = TwitterClient(job_details['consumer_key'], job_details['consumer_secret'],
                                             job_details['access_token'], job_details['access_token_secret'])
            job_details['relevant_hashtags'] = twitter_client.get_relevant_hashtags(description='#mensuration',no_of_hashtags=4)
            return job_details
        except Exception as e:
            error_client.raise_airflow_exception(f"Error getting relevant hashtags: {str(e)}")

    @task
    def generate_tweet_content(job_details):
        pass
        logdata(f"Received input : {job_details}")
        try:
            chat_gpt_client = ChatGpt(api_key=job_details['chatgpt_api_key'])
            survey_link = "https://docs.google.com/forms/d/e/1FAIpQLSf7ySR5Od8v5GvM3WKSrIMdU0MWLmUKNFpZ1EnlVIQWKUXJ8Q/viewform"
            news_promt = f"Generate a twitter post content for filling a survey form related to improving menstrual cycle for womens service. keep the tone formal. don't add any sample link"
            tweet_content = chat_gpt_client.generate_tweet_content(news_promt)
            logdata(tweet_content)
            tweet_content = tweet_content + '\n' + f"survey link : {survey_link}"
            tweet_content = tweet_content +'\n'+" ".join(job_details['relevant_hashtags'])
            job_details['tweet_content'] = tweet_content
            return job_details
        except Exception as e:
            error_client.raise_airflow_exception(f"Error while generating twitter content: {str(e)}")

    @task
    def tweet_content(job_details):
        try:
            twitter_client = TwitterClient(job_details['consumer_key'], job_details['consumer_secret'],
                                             job_details['access_token'], job_details['access_token_secret'])
            tweet_content = job_details['tweet_content']
            logdata(tweet_content)
            is_tweeted = twitter_client.tweet_text(tweet_content=tweet_content)
            if is_tweeted['tweet_status']:
                job_details['is_tweeted'] = is_tweeted['tweet_status']
                logdata(f"Tweeted successfully!")
                return job_details
            else:
                job_details['is_tweeted'] = is_tweeted['tweet_status']
                failed_msg = f"Failed while tweeting"
                logdata(failed_msg)
                error_client.raise_airflow_exception(failed_msg)
        except Exception as e:
            error_client.raise_airflow_exception(f"Error while tweeting: {str(e)}")
        

    tweet_content(generate_tweet_content(get_hashtags(get_credentials(kickOff()))))