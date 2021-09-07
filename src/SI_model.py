import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np

#parametrize this
def create_network(n, p):
    GA = nx.generators.erdos_renyi_graph(n, p)
    A = np.array(nx.adjacency_matrix(GA).todense())
    return A

def init_network(A):
    N = len(A)
    current_infected_nodes = np.zeros(N)
    centrality_nodes = np.zeros(N)
    infprob_nodes = np.zeros(N)
    first_infection = random.randint(0, N-1)
    current_infected_nodes[first_infection]=1
    return current_infected_nodes, centrality_nodes, infprob_nodes

def time_step():
    pass

def node_infprob():
    pass

def mc_result():
    pass

