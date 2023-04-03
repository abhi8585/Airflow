import requests

class TwitterStatusUpdate:

    def __init__(self):
        pass

    def tweet_text(self, tweet_content):
        print(f"Tweet to post : {tweet_content}")
        url = f"https://flask-hello-world-phi-two.vercel.app/tweet_text"
        params = {"tweet_content":tweet_content}
        response = requests.post(url,params=params)
        return response.text