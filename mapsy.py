import googlemaps
import datetime
import responses
from event import Location
gmaps = googlemaps.Client(key='AIzaSyCxbvfxL6I4sScgSpwcwTiNY2D4HbGDKoA')


def timeDistance(l1: Location, l2: Location, time: datetime.datetime):
    time = gmaps.distance_matrix(
        l1.latlngtup(), l2.latlngtup(), departure_time=time, traffic_model='best_guess')
    k = time['rows'][0]['elements'][0]['duration']['value']
    delta = datetime.timedelta(seconds=k)
    return delta
