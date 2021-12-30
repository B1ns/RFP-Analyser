import socketio
import chart_studio
import plotly.graph_objects as go
import plotly.subplots as make_subplots
import pandas as pd
import dash
import numpy as np
import adi
import math
import time
from dash import dcc
from dash import html
from copy import copy
from time import sleep

sample_rate = 10e6
center_freq = 5.8e9
num_samps = 1024


def dBm():
    sdr = adi.Pluto()
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samps
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.rx_hardwaregain_chan0 = 0.0

    sample = sdr.rx()
    x = copy(sample)
    x_c = copy(sample)

    for index in range(len(sample)):
        x_c[index] = np.conjugate(x_c[index])
    print(x)
    print(x_c)

    result = x * x_c
    result_end = math.sqrt(sum(result.real))
    now = round((10 * math.log10(abs(result_end))) * 2 - 83.51, 1)

    print(now)

    return now


def e_graph_data_load():
    time_end = time.time() + 30
    result_x = []
    append = result_x.append
    append(-24)
    while time.time() < time_end:
        append(dBm())
        append(dBm())
        if len(result_x) >= 181:
            break

    print(result_x)
    print(len(result_x))
    theta = []
    for y in range(0, 361, 2):
        theta.append(y)

    print(theta)

    save = pd.DataFrame(list(zip(result_x, theta)), columns=['dBm', 'theta'])
    save.to_csv('E.csv', index=False, encoding='cp949')

def h_graph_data_load():
    time_end = time.time() + 30
    result_x = []
    append = result_x.append
    append(-24)
    while time.time() < time_end:
        append(dBm())
        append(dBm())
        if len(result_x) >= 181:
            break

    print(result_x)
    print(len(result_x))
    theta = []
    for y in range(0, 361, 2):
        theta.append(y)

    print(theta)

    save = pd.DataFrame(list(zip(result_x, theta)), columns=['dBm', 'theta'])
    save.to_csv('H.csv', index=False, encoding='cp949')

def e_graph_produce():
    app = dash.Dash(__name__)
    e_graph_data_load()
    de = pd.read_csv("/home/jungbin/PycharmProjects/RFP-Analyser/E.csv")
    chart_studio.tools.set_credentials_file(username='Bins', api_key='JwFATh6PlTFaY71p6NZU')

    fig = make_subplots(row=1, cols=1, specs=[{'type': 'polar'}])

    fig.add_trace(
        go.Scatterpolar(
            r=de['dBm'],
            theta=de['theta'],
            mode='lines',
            name='antenna_one',
            line_color='peru',
            subplot="polar"
        )
    )

    fig.update_layout(
        polar - dict(
            radialaxis_range=[-24, 0]
        ),
        title='Radiation Patterns',
        showlegend=False,
        template="plotly_dark",
    )

    fig.update_polars(radialaxis_tick0=-24.0)

    app.layout = html.Div(children=[
        html.H1(children='Radiation Patterns'),
        html.Div(children='''Dash: A web application framework for Python.'''),
        dcc.Graph(
            id='Analyser-Graph',
            figure=fig
        )
    ], style={'color': 'black'})

    fig.show()
    app.run_server(debug=True, port=8080, host='0.0.0.0')

def h_graph_produce():
    app = dash.Dash(__name__)
    graph_data_load()
    de = pd.read_csv("/home/jungbin/PycharmProjects/RFP-Analyser/H.csv")
    chart_studio.tools.set_credentials_file(username='Bins', api_key='JwFATh6PlTFaY71p6NZU')

    fig = make_subplots(row=1, cols=1, specs=[{'type': 'polar'}])

    fig.add_trace(
        go.Scatterpolar(
            r=de['dBm'],
            theta=de['theta'],
            mode='lines',
            name='antenna_one',
            line_color='peru',
            subplot="polar"
        )
    )

    fig.update_layout(
        polar - dict(
            radialaxis_range=[-24, 0]
        ),
        title='Radiation Patterns',
        showlegend=False,
        template="plotly_dark",
    )

    fig.update_polars(radialaxis_tick0=-24.0)

    app.layout = html.Div(children=[
        html.H1(children='Radiation Patterns'),
        html.Div(children='''Dash: A web application framework for Python.'''),
        dcc.Graph(
            id='Analyser-Graph',
            figure=fig
        )
    ], style={'color': 'black'})

    fig.show()
    app.run_server(debug=True, port=8080, host='0.0.0.0')

def main():
    sio = socketio.Client()

    @sio.on('run')
    def start_anlysis(data):
        if data == 1:
            print("Start analysis antenna E-plane")
            e_graph_produce()


        elif data == 2:
            print("Start analysis antenna H-plane")
            h_graph_produce()

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


if __name__ == '__main__':
    while True:
        main()