import socketio
import chart_studio
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc
from dash import html

state = 0


def main():
    sio = socketio.Client()

    @sio.on('run')
    def start_anlysis(data):
        if data == 1:
            print("Start analysis antenna E-plane")

        elif data == 2:
            print("Start analysis antenna H-plane")

    @sio.event
    def connect():
        print("I'm connected!")

    @sio.event
    def connect_error(data):
        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")

    sio.connect('http://3.34.49.162:8080')


def graph():
    app = dash.Dash(__name__)

    de = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/polar_dataset.csv")
    dh = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/polar_dataset.csv")
    chart_studio.tools.set_credentials_file(username='Bins', api_key='JwFATh6PlTFaY71p6NZU')

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=de['x'],
        theta=de['theta'],
        mode='lines',
        name='antenna_one',
        line_color='peru'
    ))
    fig.add_trace(go.Scatterpolar(
        r=dh['x'],
        theta=dh['theta'],
        mode='lines',
        name='antenna_one',
        line_color='blue'
    ))

    fig.update_layout(
        title='Radiation Patterns',
        showlegend=False,
        template="plotly_dark",
    )

    app.layout = html.Div(children=[

        html.H1(children='Radiation Patterns'),
        html.Div(children='''Dash: A web application framework for Python.'''),
        dcc.Graph(
            id='Analyser-Graph',
            figure=fig
        )
    ], style={'color': 'black'})

    app.run_server(debug=True, port=8080, host='0.0.0.0')


if __name__ == '__main__':
    while True:
        main()