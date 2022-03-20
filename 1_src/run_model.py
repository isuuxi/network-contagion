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
from parameters import max_dose_threshold

def run_model(method, t, n, p, k, beta, m, noise_level, dose_level, experiment, network_type, max_infprob_indiv, initial_infected):
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
    print("starting model")
    initial_infected = np.sum(initial_infected)
    start_time = time.time()
    memory_length = 1000
    G = initialization.create_network(n, p, k, beta, m, network_type)
    A, A_norm, infected, infprob_indiv_nodes, dose_threshold, nodes_neighbors,  = initialization.init_network(G, max_infprob_indiv, initial_infected)
    time_series = np.zeros(t) 
    process = model.ContagionProcess(A, method, infected, nodes_neighbors, A_norm, method_params = {'infprob_indiv': max_infprob_indiv, 'dose_threshold': dose_threshold}, noise_level = noise_level, dose_level = dose_level, memory_length = memory_length)
    time_series[0] = initial_infected
    for i in range(t):
        process.step()
        if i < t -1:
            time_series[i + 1] = np.sum(process.infected)
        else:
            break
    runtime = (time.time() - start_time)
    noise_inf = process.noise_inf
    history = process.history
    contagion_inf = process.contagion_inf
    infected = process.infected
    print(f"--- contagion method is {process.method} ---")
    print(f"--- runtime is {runtime:.4f} seconds ---")
    print(f"time is {t}")
    #print(f"history is {history}")
    divisor = 10
    history = np.floor(history/divisor)
    results_dict = {"Infection time series": time_series.tolist(), "Infection node history": history.tolist(), "Runtime": runtime}
    #print(f"noise infections are {noise_inf} and contagion infections are {contagion_inf} and inital inf are {initial_infected} while total infections are {time_series[t-1]}. Time series is {time_series}")
    results_df = pd.DataFrame(history, columns = ['timestep'])
    d = {'nodes': [n], 'contagion_inf': [contagion_inf], 'noise_inf': [noise_inf], "initial_inf": [initial_infected]}
    infection_data = pd.DataFrame(data = d)
    print(infection_data)
    ## Export ##
    cwd = os.getcwd()
    current_path = Path.cwd()
    if method == "generalized_cont":
        current_run = f'data/{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}_experiment{experiment}'
    elif method == "SI_cont":
        current_run = f'data/{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_infprobindiv{max_infprob_indiv}_noise{noise_level}'

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
                    f'results_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}_experiment{experiment}.json'
                ), 'w') as json_file: 
                json.dump(results_dict, json_file)
    elif method == "SI_cont":
        with open(
                os.path.join(
                    current_path.parent,
                    "2_results", 
                    f'results_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_infprobindiv{max_infprob_indiv}_noise{noise_level}_experiment{experiment}.json'
                ), 'w') as json_file: 
                json.dump(results_dict, json_file)  
    
    infected = pd.DataFrame(infected)
    ## export the process.infected file ##
    if method == "generalized_cont":
        output_file = os.path.join(export_path, f'infected_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}_experiment{experiment}.csv')
        infected.to_csv(output_file,index=False)
    elif method == "SI_cont": 
        output_file = os.path.join(export_path, f'infected__{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_infprobindiv{max_infprob_indiv}_noise{noise_level}.csv')
        infected.to_csv(output_file,index=False)
    
    ## Export data for validation ##
    #network
    df_network = pd.DataFrame(A)
    if method == "generalized_cont":
        output_file = os.path.join(export_path, f'network_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}_experiment{experiment}.csv')
        df_network.to_csv(output_file,index=False)
    #infections
        output_file = os.path.join(export_path, f'spreading_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}_experiment{experiment}.csv')
        results_df.to_csv(output_file,index=False)
    #infection_data
        output_file = os.path.join(export_path, f'infectiondata_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose_level}_noise{noise_level}_experiment{experiment}.csv')
        infection_data.to_csv(output_file,index=False)
    elif method == "SI_cont": 
    #network
        output_file = os.path.join(export_path, f'network_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_infprobindiv{max_infprob_indiv}_noise{noise_level}.csv')
        df_network.to_csv(output_file,index=False)
    #infections
        output_file = os.path.join(export_path, f'spreading_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_infprobindiv{max_infprob_indiv}_noise{noise_level}.csv')
        results_df.to_csv(output_file,index=False)    
    #infection_data
        output_file = os.path.join(export_path, f'infectiondata_{method}_t{t}_network{network_type}_n{n}_p{p}_beta{beta}_m{m}_infprobindiv{max_infprob_indiv}_noise{noise_level}.csv')
        infection_data.to_csv(output_file,index=False)

