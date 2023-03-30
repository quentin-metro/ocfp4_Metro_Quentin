import datetime


class DateHandler:

    @staticmethod
    def getdatehours():
        date = datetime.datetime.now()
        return date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def validate(date_text):
        try:
            datetime.date.fromisoformat(date_text)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
