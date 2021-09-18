import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np

from utils import get_infprob
from utils import get_inf_pressure  
from utils import mc_result 

def create_network(n, p):
    '''
    Creates a network with the networkx package
        Parameters: 
            n: number of nodes
            p: probability for edge creation

        Returns:
            A: Matrix that represents a network
    '''
    A = nx.generators.erdos_renyi_graph(n, p)
    #A = np.array(nx.adjacency_matrix(GA).todense())
    return A

#for node in G.nodes:
#   G.nodes[node]['infected'] = False

def init_network(A):
    '''
    Constructs the attributes of the network 
        Parameter:
            A: matrix that represents a network

        Returns:  
            A: matrix that represents a network
            current_infected_nodes (list): currently infected nodes; has one infected node after initialization
            infprob_nodes (list): infection probabilities of all nodes in network A
    '''
    N = len(A)
    current_infected_nodes = np.zeros(N)
    first_infection = random.randint(0, N-1)
    current_infected_nodes[first_infection]=1
    infprob_nodes = get_infprob(A)
    return A, current_infected_nodes, infprob_nodes

def time_step(A, current_infected_nodes, infprob_nodes, t):
    '''
    Executes t time steps in the infection model
        Parameters:
            A: matrix that represents a network
            current_infected_nodes (list): currently infected nodes; has one infected node after initialization
            infprob_nodes (list): infection probabilities of all nodes in network A
            t: number of time steps

        Returns:
            time_series: time series of the number of infected nodes in all time steps
    '''
    time = np.arange(t)
    time_series = np.zeros(t)
    I = np.sum(current_infected_nodes)  
    for t in range(t):
        time_series[t] = I
        I = np.sum(current_infected_nodes)  
        inf_pressure = get_inf_pressure(A, current_infected_nodes, infprob_nodes)
        decision, c = mc_result(inf_pressure)
        #print("Decision in {} is {}".format(t, decision))
        for j in np.where(decision == 1)[0]:
            if current_infected_nodes[j] == 0:
                current_infected_nodes[j] = decision[j]
        I = np.sum(current_infected_nodes)  
        time_series[t] = I
    return time_series




