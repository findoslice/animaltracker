from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
GOOGLEMAPS_KEY = 'AIzaSyASapvCGZXKKA7yu71uWIJ-KvvgHM3TRkM'
app.config['GOOGLEMAPS_KEY'] = GOOGLEMAPS_KEY
GoogleMaps(app)

@app.route('/map', methods = ['GET', 'POST'])
def print_map():
    if request.method == 'GET':
        mymap = Map(
        style = "height:70%;width:90%;margin:5%;margin-top:10%;position: absolute; alignment:center;",
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
        return render_template('map.html', mymap = mymap)
