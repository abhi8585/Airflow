import requests

class TwitterRetweet:

    def __init__(self):
        pass

    def retweet(self, hashtag):
        print(f"hashtag to retweet : {hashtag}")
        url = f"https://flask-hello-world-phi-two.vercel.app/re_tweet"
        params = {"retweet_hashtag":hashtag}
        response = requests.post(url,params=params)
        return response.text