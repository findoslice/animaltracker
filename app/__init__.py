from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
from geopy.geocoders import Nominatim
import json
from pprint import pprint
from difflib import SequenceMatcher

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
        location = geolocator.geocode("pyongyang")
        return location.latitude, location.longitude

def parse_json(filter, jsonfile):
    out = []
    bork = []
    with open(jsonfile, 'r') as f:
        datastore = json.load(f)

    for key in datastore:
        if SequenceMatcher(None, key.lower(), filter.lower()).ratio() > 0.8:
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
        try:
            lat= markers[0]['lat'] or 55.9444941
            lng=markers[0]['lng'] or -3.1863534
        except:
            lat=55.9444941
            lng=-3.1863534
        mymap = Map(
        style = "height:1000%;width:150%;position: absolute; alignment:center; margin-top:6%;margin-left:-25%;",
        identifier="view-side",
        lat = lat,
        lng = lng,
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


@app.route('/', methods = ['GET', 'POST'])
@app.route('/submit', methods = ['GET', 'POST'])
def print_submit():
    if request.method == 'GET':
        return render_template('submit.html', result = False)
    if request.method == 'POST':
        latitutde, longitude = get_coords(request.form['location'])
        with open('database.json', 'r') as f:
            data = json.load(f)
        count = 0
        for key in data:
            if SequenceMatcher(None, key.lower(), request.form['critter'].lower()).ratio() > 0.8:
                array = data[key]
                name = key
                count = 1
                break
        if count == 0:
            array = []
            name = request.form['critter']
        array.append({'lat':latitude,
                      'lng':longitude,
                      'date':request.form['date'],
                      'description':str('<b>' + str(request.form['critter']) +'</b><br>Spotted on ' + str(request.form['date']))
                        })
        data[name] = array
        json.dump('database.json', data)
        try:
            return render_template('submit.html', result = True)
        except:
            raise
                
