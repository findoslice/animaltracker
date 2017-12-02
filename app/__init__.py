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
        style = "height:1000%;width:150%;position: absolute; alignment:center; margin-top:6%;margin-left:-25%;",
        identifier="view-side",
        lat=55.9444941,
        lng=-3.1863534,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>thicc boi</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 55.9444941,
             'lng': -3.1863534,
             'infobox': "<b>thicc boi</b>"
          }
        ]
    )
        return render_template('map.html', mymap = mymap, critters = ["squirrels", "octopus", "frank"])

