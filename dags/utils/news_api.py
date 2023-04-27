import requests
import json
import random
from datetime import date, timedelta

class DailyNews:

    def __init__(self,api_key):
        self.api_key = api_key

    def get_daily_article(self, topic):
        # TODO : add credential from some other way
        # TODO : add exception handling

        api_key = self.api_key
        endpoint = 'https://newsapi.org/v2/everything'
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        yesterday_date_str = yesterday_date.isoformat()
        params = {
            'q': f"{topic}",
            'from': today_date,
            'to': yesterday_date_str,
            'sortBy': 'relevancy',
            'apiKey': api_key
        }
        response = requests.get(endpoint, params=params)
        data = json.loads(response.text)
        daily_random_article = data["articles"][random.randint(0,3)]
        return daily_random_article

    def get_article_title(self, topic):
        daily_article = self.get_daily_article(topic)
        return daily_article["title"]


