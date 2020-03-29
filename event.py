
class Event:
    def __init__(self, name, type, desc, location, is_fixed, timeframe):
        if(is_fixed):
            if(timeframe.duration == None):
                raise Exception("fixed event Timeframe has to have a duration")
            self.scheduled_datetime = timeframe
        else:
            self.scheduled_datetime = Timeframe(None, None, None, None)

        self.id = None
        self.name = name
        self.type = type
        self.desc = desc
        self.location = location
        self.is_fixed = is_fixed
        self.timeframe = timeframe

    def isFixed(self):
        if(self.is_fixed):
            return 1
        else:
            return 0

    def setId(self, id):
        self.id = id

    def reschedule(self, new_scheduled_datetime):
        self.scheluded_datetime = new_scheduled_datetime


class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def latlngtup(self):
        return self.lat, self.lng

    def getGoogleMapsLink(self):
        # TODO
        return None


class Timeframe:
    def __init__(self, start_date, start_time, end_date, end_time,  duration=None):
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.duration = duration
