from flask import Flask, render_template, request
import csv
from geopy.geocoders import Nominatim
from geopy import distance

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


geolocator = Nominatim(user_agent="api")


def calculateDistance():
    reader = csv.reader(open('pharmacies.csv'))
    header = next(reader)
    location = geolocator.geocode(request.form('address'))
    location_lat_long = (location.latitude, location.longitude)
    default_closest = distance.distance(location_lat_long, (reader[1][6], reader[1][7]))
    if header is not None:
        for row in reader:
            row_lat_long = (row['latitude'], row['longitude'])
            if distance.distance(location_lat_long, row_lat_long) < default_closest:
                closest = row
    return closest


app.run()
