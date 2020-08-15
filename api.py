from flask import Flask, render_template, request, flash
import csv
from geopy.geocoders import Nominatim
from geopy import distance

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'A basic secret key, for testing purposes'


@app.route('/', methods=['GET', 'POST'])
def index():
    geolocator = Nominatim(user_agent="api")
    if request.method == 'POST':
        address = request.form['address']
        address_entered = address
        if not address:
            flash('Address is required')
        else:
            pharmacies = []
            # open csv and read it in as a dict
            with open('pharmacies.csv') as File:
                reader = csv.DictReader(File)
                for row in reader:
                    pharmacies.append(row)
            # Use Geopy to get full address and lat/long of location
            location = geolocator.geocode(address)
            location_lat_long = (location.latitude, location.longitude)
            # Set the first location in pharmacy dict to default as the closest in order to compare
            closest = pharmacies[1]
            closest_distance = distance.distance(location_lat_long, (closest['latitude'], closest['longitude'])).mi
            # Iterate through the pharmacies dict, starting by grabbing the lat/long of the current row
            for row in pharmacies:
                row_lat_long = row['latitude'], row['longitude']
                # Compare distance between the user's entered location and compare to the distance of the last distance
                if distance.distance(location_lat_long, row_lat_long) < closest_distance:
                    # Set the current pharmacy's full info and distance to closest if it is closer than the previous
                    closest = row
                    closest_distance = distance.distance(location_lat_long, row_lat_long).mi
            results = "{name}, {address}, {city}, {state}, {zip} , {distance} miles away".format(name=closest['name'],
                                    address=closest['address'], city = closest['city'], state=closest['state'],
                                    zip=closest['zip'], distance=closest_distance)
            return render_template('index.html', results=results, address_entered=address_entered)
    return render_template('index.html')


app.run()
