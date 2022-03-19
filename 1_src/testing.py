from networkx.algorithms.shortest_paths import unweighted
import initialization
import numpy as np
import networkx as nx
import model
import time 
import os
from pathlib import Path
import json
import pandas as pd
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
    G, unweighted = initialization.create_network(n, p)
    A, A_norm, infected, infprob_indiv_nodes, dose_threshold, nodes_neighbors = initialization.init_network(G)
    time_series = np.zeros(t) 
    process = model.ContagionProcess(A, unweighted, method, infected, nodes_neighbors, A_norm, method_params = {'infprob_indiv': infprob_indiv_nodes, 'dose_threshold': dose_threshold}, noise_level = noise_level, dose_level = dose_level, memory_length = memory_length)
    for t in range(t):
        process.step()
        time_series[t] = np.sum(process.infected)
    runtime = (time.time() - start_time)
    noise_inf = process.noise_inf
    contagion_inf = process.contagion_inf
    print(f"--- contagion method is {process.method} ---")
    print(f"--- runtime is {runtime:.4f} seconds ---")
    return time_series, process.history, runtime, A, unweighted, noise_inf, contagion_inf

parameters = [t, n, p, noise_level]
#print(parameters)
time_series, history, runtime, A, unweighted, noise_inf, contagion_inf = run_model(parameters[0], parameters[1], parameters[2], parameters[3])
divisor = 10
print(f"noise infections are {noise_inf} and contagion infections are {contagion_inf} while total infections are {time_series[t-1]}")
#print(f"history was {history}")
#history = np.floor_divide(history, where = ~np.isnan(history), signature = int)
history = np.floor(history/divisor)


#print(f"history is {history}")
results_dict = {"Infection time series": time_series.tolist(), "Infection node history": history.tolist(), "Runtime": runtime}
#print(f"infection time series is {results_dict}")
#header = ['Parameters', 'Time_series', 'Node_history', 'runtime in seconds']
#data = [parameters, time_series, history, runtime]


results_df = pd.DataFrame(history, columns = ['timestep'])
d = {'nodes': [n], 'contagion_inf': [contagion_inf], 'noise_inf': [noise_inf]}
infection_data = pd.DataFrame(data = d)
print(infection_data)

## Export ##
cwd = os.getcwd()
current_path = Path.cwd()
if method == "generalized_cont":
    current_run = f'data/{method}_t{t}_n{n}_p{p}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}'
elif method == "SI_cont":
    current_run = f'data/{method}_t{t}_n{n}_p{p}_infprobindiv{max_infprob_indiv}_noise{noise_level}'

# path for export
export_path = os.path.join(current_path.parent, current_run)
if not os.path.exists(export_path):
        os.makedirs(export_path)

#export infection data for plotting
if method == "generalized_cont":
    with open(
            os.path.join(
                current_path.parent,
                "2_results", 
                f'results_{method}_t{t}_n{n}_p{p}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}.json'
            ), 'w') as json_file: 
            json.dump(results_dict, json_file)
elif method == "SI_cont":
      with open(
            os.path.join(
                current_path.parent,
                "2_results", 
                f'results_{method}_t{t}_n{n}_p{p}_infprobindiv{max_infprob_indiv}_noise{noise_level}.json'
            ), 'w') as json_file: 
            json.dump(results_dict, json_file)  


## Export data for validation ##
#network
df_network = pd.DataFrame(A)
if method == "generalized_cont":
    output_file = os.path.join(export_path, f'network_{method}_t{t}_n{n}_p{p}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}.csv')
    df_network.to_csv(output_file,index=False)
#infections
    output_file = os.path.join(export_path, f'anaresults_{method}_t{t}_n{n}_p{p}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}.csv')
    results_df.to_csv(output_file,index=False)
#infection_data
    output_file = os.path.join(export_path, f'infectiondata_{method}_t{t}_n{n}_p{p}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}.csv')
    infection_data.to_csv(output_file,index=False)
elif method == "SI_cont": 
#network
    output_file = os.path.join(export_path, f'network_{method}_t{t}_n{n}_p{p}_infprobindiv{max_infprob_indiv}_noise{noise_level}.csv')
    df_network.to_csv(output_file,index=False)
#infections
    output_file = os.path.join(export_path, f'anaresults_{method}_t{t}_n{n}_p{p}_infprobindiv{max_infprob_indiv}_noise{noise_level}.csv')
    results_df.to_csv(output_file,index=False)    
#infection_data
    output_file = os.path.join(export_path, f'infectiondata_{method}_t{t}_n{n}_p{p}_infprobindiv{max_infprob_indiv}_noise{noise_level}.csv')
    infection_data.to_csv(output_file,index=False)
