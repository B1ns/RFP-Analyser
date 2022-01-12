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


sdr = adi.Pluto()
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 0.0

sample = sdr.rx()
x = copy(sample) / 1e6
x_c = copy(sample) / 1e6

print(x)
print(x_c)

for index in range(len(sample)):
    x_c[index] = np.conjugate(x_c[index])

result = x * x_c
result_end = math.sqrt(sum(result.real))
now = round((10 * math.log10(result_end) * 2 + 53.12), 1)
print(now)