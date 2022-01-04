import networkx as nx
import random
import numpy as np
from sklearn.preprocessing import normalize

from model import  get_infprob_indiv
from parameters import max_dose_threshold

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
    network_adj = nx.to_numpy_matrix(A)
    while  np.sum(np.all(network_adj == 0, axis = 1)) > 0:
        A = nx.generators.erdos_renyi_graph(n, p) 
        for (u, v) in A.edges():
            A.edges[u,v]['weight'] = random.random()
        network_adj = nx.to_numpy_matrix(A)
    return network_adj
    
def init_network(network_adj):
    '''
    Constructs the attributes of the network 
        Parameter:
            A: nx.graph class that represents a network

        Returns:  
            A: adjacency matrix as pandas dataframe 
            infected (dataframe): currently infected nodes; has one infected node after initialization
            infprob_indiv_nodes (list): infection probabilities of all nodes in network A
    '''
    size = len(network_adj)
    print(f"length of A is {size}")
    normalized_network = get_normalized_weights(network_adj) 
    #connected_normalized_nodes =  normalized_network[~np.all(normalized_network == 0, axis=1)]
    infected = np.zeros(size)
    first_infection = random.randint(0, size-1)
    infected[first_infection] = True
    infprob_indiv_nodes = get_infprob_indiv(network_adj)
    dose_threshold = get_dose_threshold(network_adj)
    nodes_neighbors = [None]*len(network_adj)
    for i in range(len(network_adj)):
        #print(np.nonzero(network_adj[i]))    
        nodes_neighbors[i] = np.nonzero(network_adj[i])[1]
    #print(f"Dose threshold is {dose_threshold} with dimension {dose_threshold.ndim}")
    return network_adj, normalized_network, infected, infprob_indiv_nodes, dose_threshold, nodes_neighbors


def get_normalized_weights(A):
    '''
    returns an adjacency matrix with normalized weights
       Parameters: 
           A: weighted adjacency matrix of a network
       Returns:
           N: weight-normalized adjacency matrix
    '''  
    #normalize matrix by rows (L1 normalization)
    N = normalize(A, axis=1, norm='l1')
    return N

def get_dose_threshold(A):
    '''
    returns the individual infection threshold of doses received of each node
       Parameters: 
           A: adjacency matrix of a network
       Returns:
           dose_threshold: numpy array with randomly chosen dose threshold of nodes
    '''
    dose_threshold = np.random.uniform(0, max_dose_threshold, len(A))
    return dose_threshold