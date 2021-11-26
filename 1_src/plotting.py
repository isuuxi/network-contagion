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


with open(cwd + '/2_results/results_20_500_0.1.json') as f:
  data = json.load(f)

print(f'Data is {data}')

time_series = data['Infection time series'] 
print(f'The time series {time_series}')
x = np.arange(0, 20)

fig_results, ax = plt.subplots()
ax.plot(x, time_series, label='time_series') 
plt.show()

fig_results.savefig(
        os.path.join(saving_path, 'time_series_20_500_0.1.png'),
        dpi=dpi,
        bbox_inches='tight'
)


