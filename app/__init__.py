from flask import Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps, Map
from geopy.geocoders import Nominatim
import json
import wikipedia
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
        loc = loc.split(',')
        print (loc)
        loc = loc[1:]
        ", ".join(loc)
        print (loc)
        location = geolocator.geocode(loc)
        x,y = location.latitude, location.longitude
        return x,y


def parse_json(filter, jsonfile):
    out = []
    bork = []
    with open(jsonfile, 'r') as f:
        datastore = json.load(f)

    for key in datastore:
        if (SequenceMatcher(None, key.lower(), filter.lower()).ratio() > 0.8) or filter == "":
            for elem in datastore[key]:
                bork.append(elem)
    for elem in bork:
        out = out + [{
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
            markers= parse_json(request.form['critterinos'], "database.json")
        except:
            raise
        try:
            lat= markers[0]['lat'] or 55.9444941
            lng=markers[0]['lng'] or -3.1863534
        except:
            lat=55.9444941
            lng=-3.1863534
        mymap = Map(
        style = "height:1500%;width:150%;position: absolute; alignment:center; margin-top:6%;margin-left:-25%;",
        identifier="view-side",
        lat = lat,
        lng = lng,
        markers= markers,
        zoom=8,
        cluster=True, cluster_gridsize=10,
        maptype="TERRAIN"
    )
        try:
            page = wikipedia.page(request.form['critterinos'])
            pagecontent = page.summary
            print(imagelink, pagecontent)
            return render_template('map.html', mymap = mymap, critters = ["squirrels", "octopus", "frank"], pagecontent = pagecontent)
        except:
            return render_template('map.html', mymap = mymap, critters = ["squirrels", "octopus", "frank"])

        
    
    if request.method == 'GET':
        markers = parse_json("",'database.json')
        mymap = Map(
        style = "height:1500%;width:150%;position: absolute; alignment:center; margin-top:6%;margin-left:-25%;",
        identifier="view-side",
        lat = 55.9444,
        lng = -3.1870,
        zoom=8,
        markers=markers,
        cluster=True, cluster_gridsize=10,
        maptype="TERRAIN"
    )
        return render_template('map.html', mymap = mymap, critters = ["squirrels", "octopus", "frank"])


@app.route('/', methods = ['GET', 'POST'])
@app.route('/submit', methods = ['GET', 'POST'])
def print_submit():
    if request.method == 'GET':
        return render_template('submit.html', result = True)
    if request.method == 'POST':
        if not (request.form['location'] and request.form['critter'] and request.form['date']):
            return render_template('submit.html', result = True)
        latitude, longitude = get_coords(request.form['location'])
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
                      'description':str('<b>' + str(request.form['critter']) +'</b><br>Spotted on ' + str(request.form['date']) + '<br>' + str(request.form['location']))
                        })
        data[name] = array
        pprint(data)
        with open("database.json", 'w') as outfile:
            json.dump(data, outfile)

        try:
            markers= parse_json(request.form['critter'], "database.json")
        except:
            raise
        try:
            lat= markers[0]['lat'] or 55.9444941
            lng=markers[0]['lng'] or -3.1863534
        except:
            lat=55.9444941
            lng=-3.1863534
        mymap = Map(
        style = "height:550%;width:140%;position: absolute; alignment:center; margin-top:6%; margin-left:-20%;",
        identifier="view-side",
        lat = lat,
        lng = lng,
        markers= markers,
        zoom=8,
        cluster=True, cluster_gridsize=10,
        maptype="TERRAIN"
    )


        try:
            return render_template('submitted.html', mymap = mymap)
        except:
            raise

@app.route('/gay', methods = ["GET"])
def gay():
    if request.method == "GET":
        markers = parse_json("",'database.json')
        mymap = Map(
        style = "height:40%;width:100%;position: absolute; alignment:left; margin-top:6%;margin-left:-25%;",
        identifier="view-side",
        lat = 55.9444,
        lng = -3.1870,
        zoom=8,
        markers=markers,
        cluster=False,
        maptype="TERRAIN",
        fullscreen_control=False,
        streetview_control=False
    )
        return render_template('gay.html', mymap = mymap, critters = ["squirrels", "octopus", "frank"])
                
@app.route('/api/<string:critter>', methods = ["GET"])
def api_request():
    if request.method == "GET":
        try:
            x = parse_json(critter, 'database.json')
            return jsonify(x)
        except:
            raise