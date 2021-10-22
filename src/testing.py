import SI_model
import numpy as np
import networkx as nx
import utils
import time 
import csv
import math

def run_model(t, n, p):
    '''
    Wrapper for time_step to execute t time steps of the infection process
        Parameters:
            n: number of nodes
            p: probability for edge creation
            t: number of time steps

        Returns:
            time_series: time series of the number of infected nodes in all time steps
            history: time step of infection for each node
    '''
    start_time = time.time()
    G = SI_model.create_network(n, p)
    A, infected, infprob_indiv_nodes, dose_threshold = SI_model.init_network(G)
    time_series = np.zeros(t) 
    process = utils.ContagionProcess(A, "generalized_cont", infected, method_params = {'infprob_indiv': infprob_indiv_nodes, 'dose_threshold': dose_threshold})
    for t in range(t):
        process.step()
        time_series[t] = np.sum(process.infected)
    runtime = (time.time() - start_time)
    print(f"--- contagion method is {process.method} ---")
    print(f"--- runtime is {runtime:.4f} seconds ---")
    return time_series, process.history, runtime 

parameters = [20, 400, 0.04]
#print(parameters)
time_series, history, runtime = run_model(parameters[0], parameters[1], parameters[2])
print (f"Infections are {time_series} ")
#and the history is {history}")

header = ['Parameters', 'Time_series', 'Node_history', 'runtime in seconds']
data = [parameters, time_series, history, runtime]

with open('results.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerow(data)