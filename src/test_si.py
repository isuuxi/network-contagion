import SI_model
import numpy as np
import networkx as nx
import utils

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
    G = SI_model.create_network(n, p)
    A, infected, infprob_indiv_nodes = SI_model.init_network(G)
    time = np.arange(t)
    time_series = np.zeros(t) 
    process = utils.ContagionProcess(A, infprob_indiv_nodes, "SI_cont", infected)
    for t in range(t):
        process.step()
        time_series[t] = np.sum(process.infected)
    return time_series, process.history

time_series, history = run_model(20, 500, 0.01)
print (f"Infections are {time_series} and the history is {history}")