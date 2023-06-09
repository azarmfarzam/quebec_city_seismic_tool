# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 15:15:19 2021

@author: azarm
"""
import dash_html_components as html
import dash_leaflet as dl
from dash import Dash

# Some shapes.
markers = [dl.Marker(position=[56, 10]), dl.CircleMarker(center=[55, 10])]
polygon = dl.Polygon(positions=[[57, 10], [57, 11], [56, 11], [57, 10]])
# Some tile urls.
keys = ["watercolor", "toner", "terrain"]
url_template = "http://{{s}}.tile.stamen.com/{}/{{z}}/{{x}}/{{y}}.png"
attribution = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, ' \
              '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data ' \
              '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
# Create app.


app = Dash()
app.layout = html.Div(dl.Map([
    dl.LayersControl(
        [dl.BaseLayer(dl.TileLayer(url=url_template.format(key), attribution=attribution),
                      name=key, checked=key == "toner") for key in keys] +
        [dl.Overlay(dl.LayerGroup(markers), name="markers", checked=True),
         dl.Overlay(dl.LayerGroup(polygon), name="polygon", checked=True)]
    )
], zoom=7, center=(56, 10)), style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})