import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np

from utils import get_infprob
from utils import get_inf_pressure  
from utils import mc_result 

def create_network(n, p):
    A = nx.generators.erdos_renyi_graph(n, p)
    #A = np.array(nx.adjacency_matrix(GA).todense())
    return A

#for node in G.nodes:
#   G.nodes[node]['infected'] = False

def init_network(A):
    N = len(A)
    current_infected_nodes = np.zeros(N)
    first_infection = random.randint(0, N-1)
    current_infected_nodes[first_infection]=1
    infprob_nodes = get_infprob(A)
    return A, current_infected_nodes, infprob_nodes

def time_step(A, current_infected_nodes, infprob_nodes, t):
    time = np.arange(t)
    for t in range(time):
        inf_pressure = get_inf_pressure(A, current_infected_nodes, infprob_nodes)
        decision = mc_result(inf_pressure)
        for j in np.where(decision == 1)[0]:
            if current_infected_nodes[j] == 0:
                current_infected_nodes[j] = decision[j]
    I = np.sum(current_infected_nodes)
    time_series[t] = I
    return time_series




