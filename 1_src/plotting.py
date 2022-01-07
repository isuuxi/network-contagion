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

#path where results are obtained from
results_path = os.path.join(current_path.parent, f'2_results/{method}')

# saving path for plots
saving_path = os.path.join(current_path.parent, f'3_plots/{method}')
if not os.path.exists(saving_path):
        os.makedirs(saving_path)

with open(os.path.join(
            results_path,
            f'results_{method}_t{t}_n{n}_p{p}_noise{noise_level}.json'
        )) as f:
        data = json.load(f)

#os.path.join(
#            results_path,
#            f'results_{method}_t{t}_n{n}_p{p}_noise{noise_level}.json'
#        ))


#with open(results_path + f'/results_{method}_t{t}_n{n}_p{p}_noise{noise_level}.json') as f:
#  data = json.load(f)  

print(f'Data is {data}')

time_series = data['Infection time series'] 
print(f'The time series {time_series}')
x = np.arange(0, t)

fig_results, ax = plt.subplots()
ax.plot(x, time_series, label='time_series') 
plt.suptitle(f'Time series of {method}')
plt.xlabel('time step')
plt.ylabel('number of infections')
if method == "generalized_cont":
        ax.text(100, 140, f'size: {n}, edge probability: {p}, threshold: {max_dose_threshold}, noise:{noise_level}',
        bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
else:
        ax.text(20, 50, f'size: {n}, edge prob: {p}, inf_prob_indiv: {max_infprob_indiv}. noise:{noise_level}',
        bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})       

plt.show()

if method == "generalized_cont":
    fig_results.savefig(
            os.path.join(saving_path, f'{method}_time{t}_size{n}_prob{p}_noiselevel{noise_level}_thresh{max_dose_threshold}.png'),
            dpi=dpi,
            bbox_inches='tight'
    )
else:
     fig_results.savefig(
            os.path.join(saving_path, f'{method}_time{t}_size{n}_prob{p}_noiselevel{noise_level}_infprob{max_infprob_indiv}.png'),
            dpi=dpi,
            bbox_inches='tight'
     )       



