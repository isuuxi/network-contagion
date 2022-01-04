import initialization
import numpy as np
import networkx as nx
import model
import time 
import csv
import math
import os
from pathlib import Path
import json
from parameters import *

def run_model(t, n, p, noise_level):
    '''
    Wrapper for time_step to execute t time steps of the infection process
        Parameters:
            t: number of time steps
            n: number of nodes
            p: probability for edge creation
            

        Returns:
            time_series: time series of the number of infected nodes in all time steps
            history: time step of infection for each node
    '''
    start_time = time.time()
    G = initialization.create_network(n, p)
    network_adj, normalized_network, infected, infprob_indiv_nodes, dose_threshold, nodes_neighbors = initialization.init_network(G)
    time_series = np.zeros(t) 
    #noise_level = 0.0001
    process = model.ContagionProcess(network_adj, method, infected, nodes_neighbors, normalized_network, method_params = {'infprob_indiv': infprob_indiv_nodes, 'dose_threshold': dose_threshold}, noise_level = noise_level, dose_level = dose_level)
    for t in range(t):
        process.step()
        time_series[t] = np.sum(process.infected)
    runtime = (time.time() - start_time)
    print(f"--- contagion method is {process.method} ---")
    print(f"--- runtime is {runtime:.4f} seconds ---")
    print(f"Normalized network is {normalized_network}")
    print(f"infected node is {infected}")
    #print(f"Dose threshold is {dose_threshold} with dimension {dose_threshold.ndim}")
    return time_series, process.history, runtime 

parameters = [t, n, p, noise_level]
#print(parameters)
time_series, history, runtime = run_model(parameters[0], parameters[1], parameters[2], parameters[3])
results_dict = {"Infection time series": time_series.tolist(), "Infection node history": history.tolist(), "Runtime": runtime}
print(f"infection time series is {results_dict}")
#header = ['Parameters', 'Time_series', 'Node_history', 'runtime in seconds']
#data = [parameters, time_series, history, runtime]

## Export ##
cwd = os.getcwd()
current_path = Path.cwd()

# path for json files
results_path = os.path.join(current_path, '2_results')
if not os.path.exists(results_path):
        os.makedirs(results_path)

#export
with open(
        os.path.join(
            results_path,
            f'results_{method}_{parameters[0]}_{parameters[1]}_{parameters[2]}_noiselevel{parameters[3]}.json'
        ), 'w') as json_file: 
        json.dump(results_dict, json_file)




