from flask import Flask, render_template, request, flash
import csv
from geopy.geocoders import Nominatim
from geopy import distance

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'A basic secret key, for testing purposes'


@app.route('/', methods=['GET', 'POST'])
def index():
    # Set up nominatim in Geopy to be able to take in an address
    geolocator = Nominatim(user_agent="api")
    # Check to see if request method is POST
    if request.method == 'POST':
        # Take in address, city, and state, then format them into a single string to be used with Geopy
        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        address = '{street} {city} {state}'.format(street=street_address, city=city, state=state)
        if address is None:
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
            # Format the results of the closest pharmacy into a string to be returned
            results = "{name}, {address}, {city}, {state}, {zip} , {distance} miles away".format(name=closest['name'],
                                                                                                 address=closest[
                                                                                                     'address'],
                                                                                                 city=closest['city'],
                                                                                                 state=closest['state'],
                                                                                                 zip=closest['zip'],
                                                                                                 distance=round(closest_distance, 2))
            # Render the template 'index.html' and pass the results and address to it
            return render_template('index.html', results=results, address=location)
    return render_template('index.html')


app.run()
