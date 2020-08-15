from flask import Flask, render_template, request
import csv
from geopy.geocoders import Nominatim
from geopy import distance

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address = ''
        address = request.form
        print address
        calculateDistance(address)
    return render_template('index.html')


geolocator = Nominatim(user_agent="api")


def calculateDistance(address):
    # reader = csv.reader(open('pharmacies.csv'))
    # header = next(reader)
    # location = geolocator.geocode(request.form('address'))
    # location_lat_long = (location.latitude, location.longitude)
    # default_closest = distance.distance(location_lat_long, (reader.next['latitude'], reader.next['longitude']))
    # if header is not None:
    #     for row in reader:
    #         row_lat_long = (row['latitude'], row['longitude'])
    #         if distance.distance(location_lat_long, row_lat_long) < default_closest:
    #             closest = row
    # return closest

    pharmacies = []
    with open('pharmacies.csv') as File:
        reader = csv.DictReader(File)
        for row in reader:
            pharmacies.append(row)
    location = geolocator.geocode(address)
    location_lat_long = (location.latitude, location.longitude)
    print(location)

    closest = distance.distance(location_lat_long, (pharmacies[1]['latitude'], pharmacies[1]['longitude']))
    for row in pharmacies:
        row_lat_long = row['latitude'], row['longitude']
        if distance.distance(location_lat_long, row_lat_long) < closest:
            closest = row
    return closest


app.run()
