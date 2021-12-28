import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import ticker
import csv
import json
from pathlib import Path
import os
import math
from parameters import *

###############################################################################
### Matplotlib Settings
###############################################################################

settings = {
    'text.usetex': True,
    'font.weight': 'normal',
    'font.size': 14
}

# resolution for plots
dpi = 300

cwd = os.getcwd()

current_path = Path.cwd()
# saving path for plots
saving_path = os.path.join(current_path, '3_plots')
if not os.path.exists(saving_path):
        os.makedirs(saving_path)

with open(cwd + f'/2_results/results_{method}_{t}_{n}_{p}_noiselevel{noise_level}.json') as f:
  data = json.load(f)

print(f'Data is {data}')

time_series = data['Infection time series'] 
print(f'The time series {time_series}')
x = np.arange(0, t)

fig_results, ax = plt.subplots()
ax.plot(x, time_series, label='time_series') 
plt.suptitle(f'Time series of {method}')
plt.xlabel('time step')
plt.ylabel('number of infections')
ax.text(310, 15, f'size: {n}, edge probability: {p}, threshold: {max_dose_threshold}',
        bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
plt.show()

fig_results.savefig(
        os.path.join(saving_path, f'{method}_time{t}_size{n}_prob{p}_noiselevel{noise_level}_thresh{max_dose_threshold}.png'),
        dpi=dpi,
        bbox_inches='tight'
)


