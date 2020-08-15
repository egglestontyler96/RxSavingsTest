from flask import Flask, render_template, request, flash
import csv
from geopy.geocoders import Nominatim
from geopy import distance

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'A basic secret key, for testing purposes'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        if not address:
            flash('Address is required')
        else:
            pharmacies = []
            with open('pharmacies.csv') as File:
                reader = csv.DictReader(File)
                for row in reader:
                    pharmacies.append(row)
            location = geolocator.geocode(address)
            location_lat_long = (location.latitude, location.longitude)
            closest = pharmacies[1]
            closest_distance = distance.distance(location_lat_long, (closest['latitude'], closest['longitude'])).mi
            print closest
            for row in pharmacies:
                row_lat_long = row['latitude'], row['longitude']
                if distance.distance(location_lat_long, row_lat_long) < closest_distance:
                    closest = row
                    closest_distance = distance.distance(location_lat_long, row_lat_long).mi
        return render_template('index.html', closest=closest)
    return render_template('index.html')


geolocator = Nominatim(user_agent="api")


# def calculate_distance():
#     pharmacies = []
#     with open('pharmacies.csv') as File:
#         reader = csv.DictReader(File)
#         for row in reader:
#             pharmacies.append(row)
#     location = geolocator.geocode(request.form('address'))
#     location_lat_long = (location.latitude, location.longitude)
#     print(location)
#
#     closest = distance.distance(location_lat_long, (pharmacies[1]['latitude'], pharmacies[1]['longitude']))
#     for row in pharmacies:
#         row_lat_long = row['latitude'], row['longitude']
#         if distance.distance(location_lat_long, row_lat_long) < closest:
#             closest = row
#     return closest


app.run()
