import googlemaps
from datetime import datetime
import responses

gmaps = googlemaps.Client(key='AIzaSyCxbvfxL6I4sScgSpwcwTiNY2D4HbGDKoA')

#origins,destinations - listy krotek (lat,lng)
#conveyance - środek transportu ('walking','driving','bycycling','transit')
#when - moment wyjazdu (datetime)
def howlong(origins,destinations,conveyance,when):
    time=gmaps.distance_matrix(origins,destinations,mode=conveyance,departure_time=when, traffic_model='best_guess')
    return time['rows'][0]['elements'][0]['duration']['value']
