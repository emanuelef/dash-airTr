import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = dash.Dash('AirTrApp')
server = app.server

mapbox_access_token = 'pk.eyJ1IjoiZW1hZnVtYSIsImEiOiJjamh1ZGVoZGowbGExM3duMDkwMnhtNDhiIn0.xgW6mtfaTEgFNw8jC6i_Yw'

df = pd.read_json(
    'http://ec2-18-130-36-119.eu-west-2.compute.amazonaws.com/all?from=1529335903&to=1529350308'
)

df = pd.DataFrame(list(df["items"]))

df["Date/Time"] = pd.to_datetime(df['time'], unit='s')
df.index = df["Date/Time"]
df.drop("Date/Time", 1, inplace=True)

df = df.drop(df.columns[[0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 13, 14]], axis=1)
df = df.rename(columns={'latitude': 'Lat', 'longitude': 'Lon', 'galtM': 'Alt'})

app.layout = html.Div(
    [
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure={
                'data': [
                    go.Scattermapbox(
                        lat=df['Lat'],
                        lon=df['Lon'],
                        text=df['Alt'],
                        hoverinfo="lat+lon+text",
                        mode='markers',
                        opacity=0.7,
                        marker=Marker(
                            color=df['Alt'],
                            colorscale=[[0, "#F4EC15"], [0.04167, "#DAF017"], [
                                0.0833, "#BBEC19"
                            ], [0.125, "9DE81B"], [0.1667, "#80E41D"], [
                                0.2083, "#66E01F"
                            ], [0.25, "#4CDC20"], [0.292, "#34D822"], [
                                0.333, "#24D249"
                            ], [0.375, "#25D042"], [0.4167, "#26CC58"], [
                                0.4583, "#28C86D"
                            ], [0.50, "#29C481"], [0.54167, "#2AC093"],
                                        [0.5833, "#2BBCA4"], [1.0, "#613099"]],
                            opacity=0.5,
                        ))
                ],
                'layout':
                go.Layout(
                    autosize=True,
                    hovermode='closest',
                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=0,
                        center=dict(lat=51.443874, lon=-0.342588),
                        pitch=0,
                        zoom=10),
                )
            }),
    ],
    style={"padding-top": "10px"})

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    "//fonts.googleapis.com/css?family=Raleway:400,300,600",
    "//fonts.googleapis.com/css?family=Dosis:Medium",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
