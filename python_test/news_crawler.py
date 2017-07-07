from datetime import timedelta, datetime

class NewCrawler:
    def __init__(self):
        pass

    @classmethod
    def getDatesSet(cls, inputValue):
        delta = inputValue.endDate - inputValue.startDate
        datesSet = []
        for i in range(delta.days + 1):
            rawDates = inputValue.startDate + timedelta(days=i)
            datesSet.append(str(rawDates).replace("00:00:00", "").rstrip())
        return datesSet
