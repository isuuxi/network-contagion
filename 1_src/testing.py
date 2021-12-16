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

def run_model(t, n, p):
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
    #print(f"Not connected nodes are {not_connected}")
    time_series = np.zeros(t) 
    process = model.ContagionProcess(network_adj, "generalized_cont", infected, nodes_neighbors, normalized_network, method_params = {'infprob_indiv': infprob_indiv_nodes, 'dose_threshold': dose_threshold}, noise_level = 0.001, dose_level = 0.00001)
    for t in range(t):
        process.step()
        time_series[t] = np.sum(process.infected)
    runtime = (time.time() - start_time)
    print(f"--- contagion method is {process.method} ---")
    print(f"--- runtime is {runtime:.4f} seconds ---")
    return time_series, process.history, runtime 

parameters = [80, 100, 0.09]
#print(parameters)
time_series, history, runtime = run_model(parameters[0], parameters[1], parameters[2])
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
            f'results_{parameters[0]}_{parameters[1]}_{parameters[2]}.json'
        ), 'w') as json_file: 
        json.dump(results_dict, json_file)




