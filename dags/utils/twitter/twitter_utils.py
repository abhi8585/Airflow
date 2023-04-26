import re
from collections import Counter
from utils.logger import Logger

logger = Logger()

class TwitterUtils:

    def __init__(self):
        logger.log_data(f"TwitterUtils client created successfully")
    
    @staticmethod
    def get_top_hashtags(hashtags, no_of_hashtags):
        try:
            flattened_hashtags = [tag for sublist in hashtags for tag in sublist]
            counter = Counter(flattened_hashtags)
            top_hashtags = [tag for tag, count in counter.most_common(no_of_hashtags)]
            logger.log_data(f"Top hashtags are {top_hashtags}")
            return top_hashtags
        except Exception as e:
            err_message = f"Error occurred while getting top hashtags, {str(e)}"
            logger.log_data(err_message)

    @staticmethod
    def extract_hashtags(text):
        try:
            logger.log_data(f"Extract hashtags from this text {text}")
            return re.findall(r'#\w+', text)
        except Exception as e:
            err_message = f"Error occurred while extracting hashtags, {str(e)}"
            logger.log_data(err_message)
