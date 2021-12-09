import networkx as nx
import random
import numpy as np

from model import get_dose_threshold, get_infprob_indiv

def create_network(n, p):
    '''
    Creates a network with the networkx package
        Parameters: 
            n: number of nodes
            p: probability for edge creation

        Returns:
            A: nx.graph class that represents a network
    '''
    A = nx.generators.erdos_renyi_graph(n, p)
    for (u, v) in A.edges():
        A.edges[u,v]['weight'] = random.random()
    return A
    
def init_network(A):
    '''
    Constructs the attributes of the network 
        Parameter:
            A: nx.graph class that represents a network

        Returns:  
            A: adjacency matrix as pandas dataframe 
            infected (dataframe): currently infected nodes; has one infected node after initialization
            infprob_indiv_nodes (list): infection probabilities of all nodes in network A
    '''
    network_adj = nx.to_numpy_matrix(A)
    N = len(network_adj)
    infected = np.zeros(len(network_adj))
    first_infection = random.randint(0, N-1)
    infected[first_infection] = True
    infprob_indiv_nodes = get_infprob_indiv(network_adj)
    dose_threshold = get_dose_threshold(network_adj)
    nodes_neighbors = [None]*(len(A))
    for i in range(len(A)):
        nodes_neighbors[i] = (np.nonzero(A[i])[1])
    N = get_normalized_weights(self.A) # implement this somewhere else or it will be calculated in every step
    return network_adj, infected, infprob_indiv_nodes, dose_threshold, nodes_neighbors, N
