import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import time

application = dash.Dash('AirTrApp')
server = application.server

mapbox_access_token = 'pk.eyJ1IjoiZW1hZnVtYSIsImEiOiJjamh1ZGVoZGowbGExM3duMDkwMnhtNDhiIn0.xgW6mtfaTEgFNw8jC6i_Yw'

application.layout = html.Div(
    [
        html.H2('Flights passages'),
        dcc.DatePickerSingle(id='date-picker-single', date=dt(2018, 6, 10)),
        dcc.Graph(id='passage-flights'),
        dcc.RangeSlider(
            marks={i: 'H {}'.format(i)
                   for i in range(0, 24)},
            min=0,
            max=24,
            value=[0, 24])
    ],
    style={'margin': 'auto auto'})


@application.callback(
    dash.dependencies.Output('passage-flights', 'figure'),
    [dash.dependencies.Input('date-picker-single', 'date')])
def update_figure(selected_day):
    print(selected_day)
    selected_day=selected_day.split()[0]

    pattern = '%Y-%m-%d'
    epochStart = int(time.mktime(time.strptime(selected_day, pattern)))
    epochEnd = epochStart + 60 * 60 * 24

    print(epochStart)
    print(epochEnd)

    urlRequest = 'http://air-api-gateway-dev.eu-west-2.elasticbeanstalk.com/all?from={}&to={}'.format(epochStart, epochEnd)
    #urlRequest = 'http://macbook-pro-di-emanuele.local:3001/all?from={}&to={}'.format(epochStart, epochEnd)

    print(urlRequest)

    df = pd.read_json(urlRequest)

    df = pd.DataFrame(list(df["items"]))

    df["Date/Time"] = pd.to_datetime(df['time'], unit='s')
    df.index = df["Date/Time"]
    df.drop("Date/Time", 1, inplace=True)

    df = df.drop(df.columns[[0, 1, 2, 4, 5, 8, 9, 10, 11, 12, 13, 14]], axis=1)
    df = df.rename(columns={
        'latitude': 'Lat',
        'longitude': 'Lon',
        'galtM': 'Alt'
    })
    return {
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
                    colorscale='Hot',
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
                style='dark',
                zoom=9),
        )
    }


external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    "//fonts.googleapis.com/css?family=Raleway:400,300,600",
    "//fonts.googleapis.com/css?family=Dosis:Medium",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
]

for css in external_css:
    application.css.append_css({"external_url": css})

if __name__ == '__main__':
    application.run_server(debug=True)
