from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
from geopy.geocoders import Nominatim
import json
from pprint import pprint

app = Flask(__name__)
GOOGLEMAPS_KEY = 'AIzaSyASapvCGZXKKA7yu71uWIJ-KvvgHM3TRkM'
app.config['GOOGLEMAPS_KEY'] = GOOGLEMAPS_KEY
GoogleMaps(app)

def get_coords(loc):
    geolocator = Nominatim()
    location = geolocator.geocode(loc)
    try:
        x,y = location.latitude, location.longitude
        return x,y
    except:
        raise
        location = geolocator.geocode("pyongyang")
        return location.latitude, location.longitude

def parse_json(filter, jsonfile):
    out = []
    bork = []
    with open(jsonfile, 'r') as f:
        datastore = json.load(f)

    for key in datastore:
        if key.lower() == filter.lower():
            for elem in datastore[key]:
                bork.append(elem)
    for elem in bork:
        out = out + [{'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                     'lat': elem['lat'],
                     'lng': elem['lng'],
                     'infobox' : elem['description']
            }]
    pprint(out)
    return out
    

@app.route('/map', methods = ['GET', 'POST'])
def print_map():
    if request.method == 'POST':
        try:
            markers= parse_json(request.form['critters'], "template.json")
        except:
            raise
        mymap = Map(
        style = "height:1000%;width:150%;position: absolute; alignment:center; margin-top:6%;margin-left:-25%;",
        identifier="view-side",
        lat= markers[0]['lat'] or 55.9444941,
        lng=markers[0]['lng'] or -3.1863534,
        markers= markers,
        zoom=5
    )
        return render_template('map.html', mymap = mymap, critters = ["squirrels", "octopus", "frank"])
    
    if request.method == 'GET':
        mymap = Map(
        style = "height:1000%;width:150%;position: absolute; alignment:center; margin-top:6%;margin-left:-25%;",
        identifier="view-side",
        lat= 55.9444941,
        lng=-3.1863534,
        zoom=10
    )
        return render_template('map.html', mymap = mymap, critters = ["squirrels", "octopus", "frank"])
