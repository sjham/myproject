from datetime import datetime

class InputValue:
    def __init__(self, startDate, endDate):
        self.startDate = datetime.strptime(startDate, "%Y,%m,%d")
        self.endDate = datetime.strptime(endDate, "%Y,%m,%d")
