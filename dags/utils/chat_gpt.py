import openai
import random
openai.api_key = ""

class ChatGpt:

    def __init__(self):
        pass

    def generate_tweet_content(self, twitter_promt):
        tweet_content = ""
        try:
            model_engine = "text-davinci-002"
            response = openai.Completion.create(
            engine=model_engine,
            prompt=twitter_promt,
            temperature=0.5,
            max_tokens=50,
            n=1,
            stop=None,
            timeout=25)
            tweet_content = response.choices[0].text.strip()
            while len(tweet_content) > 220:
                response = openai.Completion.create(
                    engine=model_engine,
                    prompt=twitter_promt,
                    temperature=0.5,
                    max_tokens=50,
                    n=1,
                    stop=None,
                    timeout=15,
                )
                tweet_content = response.choices[0].text.strip()
                # print(tweet_content)
        except Exception as e:
            print(e)
        return tweet_content   
