import datetime
class GeneralUtils:

    def get_current_timestamp(self):
        try:
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return None