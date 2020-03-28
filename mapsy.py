import googlemaps
from datetime import datetime
import responses

gmaps = googlemaps.Client(key='AIzaSyCxbvfxL6I4sScgSpwcwTiNY2D4HbGDKoA')


def timeDistance(l1:Location, l2:Location,time:datatime.datatime):
    time=gmaps.distance_matrix(l1,l2,departure_time=time, traffic_model='best_guess')
    k=time['rows'][0]['elements'][0]['duration']['value']
    delta=datatime.timedelta(seconds=k)
    return delta
