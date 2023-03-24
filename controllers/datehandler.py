import datetime


class DateHandler:

    @staticmethod
    def getdatehours():
        date = datetime.datetime.now()
        return date.strftime("%Y-%m-%d %H:%M:%S")
