import pandas as pd
import numpy as np
import re
from geopy import distance

df = pd.read_csv('NY_realestate2023-02-17.csv')



#removing apt number from address
red_address = []
for i in range(len(df.index)):
    red_address.append(re.sub('#.*?,', '', df.loc[i, 'address']))

df['red_address'] = red_address


#getting coordinates
import geopy
from geopy.geocoders import Nominatim
geopy.geocoders.options.default_timeout = 100
geolocator = Nominatim(user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0')

lat = []
long = []

from time import sleep
for i in range(len(df.index)):
#for i in range(20):
    print(i)
    sleep(.5)
    location = geolocator.geocode(df.loc[i, 'red_address'])
    if location is None:
        lat.append(np.NaN)
        long.append(np.NaN)
    else:
        lat.append(location.latitude)
        long.append(location.longitude)


df['latitude'] = lat
df['longitude'] = long



#central park
park = (40.785091, -73.968285)
dist = []

for lat, lon in zip(df['latitude'], df['longitude']):
	try:
		dist.append(distance.distance((lat, lon), park).km)
	except:
		dist.append(np.NaN)


df['distance'] = dist







df.to_csv('NY_realestate2023-02-17-coords.csv', index = False)
