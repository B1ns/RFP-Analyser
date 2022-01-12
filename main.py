import socketio
import chart_studio
import plotly.graph_objects as go
import pandas as pd
import dash
import numpy as np
import adi
import math
import time
from time import sleep
from dash import dcc
from dash import html
from copy import copy

sample_rate = 10e6
center_freq = 5.8e9
num_samps = 1024

def dBm():
    sdr = adi.Pluto()
    sdr.rx_lo = int(center_freq)
    sdr.rx_hardwaregain_chan0 = 20.0

    sample = sdr.rx()
    x = copy(sample) / 1e6
    x_c = copy(sample) / 1e6

    save = pd.DataFrame(list(x), columns=['dBm'])
    save.to_csv('X.csv', index=False, encoding='cp949')


    for index in range(len(sample)):
        x_c[index] = np.conjugate(x_c[index])

    result = x * x_c
    result_end = sum(result)
    now = 10 * math.log10(result_end) + 34
    print(now)

    return now



def e_graph_data_load():
    print("측정중 입니다")
    time_end = time.time() + 32
    result_x = []
    append = result_x.append

    start = time.time()
    while time.time() < time_end:
        append(dBm())
        sleep(0.06)
        if len(result_x) > 361:
            break

    print("time :", time.time() - start)

    print(result_x)
    print(len(result_x))
    theta = []
    for y in range(0, 361):
        theta.append(y)

    print(theta)

    save = pd.DataFrame(list(zip(result_x, theta)), columns=['dBm', 'theta'])
    save.to_csv('E.csv', index=False, encoding='cp949')
    print("측정 완료.")


def h_graph_data_load():
    print("측정중 입니다")
    time_end = time.time() + 32
    result_x = []
    append = result_x.append

    while time.time() < time_end:
        result_dBm = dBm()
        if result_dBm > 0:
            append(0)
        else:
            append(dBm())
        sleep(0.06)
        if len(result_x) > 361:
            break
    print(result_x)
    print(len(result_x))
    theta = []
    for y in range(0, 361):
        theta.append(y)

    print(theta)

    save = pd.DataFrame(list(zip(result_x, theta)), columns=['dBm', 'theta'])
    save.to_csv('H.csv', index=False, encoding='cp949')
    print("측정 완료.")

def e_graph_produce():
    app = dash.Dash(__name__)
    e_graph_data_load()
    de = pd.read_csv("/home/rfp/PycharmProjects/RFP-Analyser/E.csv")
    chart_studio.tools.set_credentials_file(username='Bins', api_key='JwFATh6PlTFaY71p6NZU')

    fig = go.Figure()

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
        polar=dict(
            radialaxis_range=[-40, 5]
        ),
        title='Radiation Patterns',
        showlegend=False,
        template="plotly_dark",
    )

    app.layout = html.Div(children=[
        html.H1(children='Radiation Patterns'),
        html.Div(children='''E-Plane'''),
        dcc.Graph(
            id='Analyser-Graph',
            figure=fig
        )
    ], style={'color': 'white', 'background': '#111111'})

    fig.show()
    app.run_server(debug=False, port=8080, host='0.0.0.0')


def h_graph_produce():
    app = dash.Dash(__name__)
    h_graph_data_load()
    de = pd.read_csv("/home/rfp/PycharmProjects/RFP-Analyser/H.csv")
    chart_studio.tools.set_credentials_file(username='Bins', api_key='JwFATh6PlTFaY71p6NZU')

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=de['dBm'],
            theta=de['theta'],
            mode='lines',
            name='antenna_one',
            line_color='red',
            subplot="polar"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis_range=[-40, 5]
        ),
        title='Radiation Patterns',
        showlegend=False,
        template="plotly_dark",
    )

    app.layout = html.Div(children=[
        html.H1(children='Radiation Patterns'),
        html.Div(children='''H-Plane'''),
        dcc.Graph(
            id='Analyser-Graph',
            figure=fig
        )
    ], style={'color': 'white', 'background': '#111111'})

    fig.show()
    app.run_server(debug=False, port=8081, host='0.0.0.0')


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

    sio.connect('http://3.34.194.121:8080')


if __name__ == '__main__':
    main()
