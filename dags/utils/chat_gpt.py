import requests
import json
class ChatGpt:

    def __init__(self):
        pass

    def generate_content(self, prompt):
        generated_content = ""
        params = {
            "prompt": prompt
        }
        url = "https://flask-hello-world-phi-two.vercel.app/generate_content"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            generated_content = json.loads(response.text)["message"]
            return generated_content
        return generated_content

