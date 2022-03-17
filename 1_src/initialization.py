from asyncio.windows_events import NULL
import networkx as nx
import random
import numpy as np
from sklearn.preprocessing import normalize
import pandas as pd
import os
from pathlib import Path


from parameters import max_dose_threshold

def create_network(n, p, empirical_network):
    '''
    Creates a network with the networkx package
        Parameters: 
            n: number of nodes
            p: probability for edge creation

        Returns:
            A: nx.graph class that represents a network
    '''
    cwd = os.getcwd()
    current_path = Path.cwd()
    if empirical_network == True:
        blub = pd.read_hdf(os.path.join(
                    current_path.parent,
                    "4_network", 
                    "flightroute_proximity_network_depth2.hdf"
                    )
                )
        network_adj = np.asmatrix(pd.DataFrame(blub).to_numpy())
        unweighted = NULL
        #print(network_adj, type(network_adj))
    else: 
        A = nx.generators.erdos_renyi_graph(n, p) 
        unweighted = nx.to_numpy_matrix(A)
        #print(f"unweighted init is {unweighted}")
        for (u, v) in A.edges():
            A.edges[u,v]['weight'] = random.random()
        network_adj = nx.to_numpy_matrix(A)
        while  np.sum(np.all(network_adj == 0, axis = 1)) > 0:
            A = nx.generators.erdos_renyi_graph(n, p) 
            for (u, v) in A.edges():
                A.edges[u,v]['weight'] = random.random()
            network_adj = nx.to_numpy_matrix(A)
    return network_adj, unweighted
    
def init_network(network_adj, max_infprob_indiv):
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
    normalized_network = get_normalized_weights(network_adj) 
    infected = np.zeros(size)
    first_infection = random.randint(0, size-1)
    infected[first_infection] = True
    infprob_indiv_nodes = max_infprob_indiv
    #print(f"infprob_indiv in method is {infprob_indiv_nodes}")
    #infprob_indiv_nodes = get_infprob_indiv(network_adj, max_infprob_indiv)
    dose_threshold = get_dose_threshold(network_adj)
    nodes_neighbors = [None]*len(network_adj)
    #for i in range(len(network_adj)):
        #print(np.nonzero(network_adj[i]))    
        #nodes_neighbors[i] = np.nonzero(network_adj[i])[1]
    #print(f"Dose threshold is {dose_threshold} with dimension {dose_threshold.ndim}")
    nodes_neighbors = 0
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

def get_infprob_indiv(A, max_infprob_indiv):
    '''
    returns the individual infection probability of each node
       Parameters: 
           A: adjacency matrix of a network
       Returns:
           infprob_indiv: numpy array with randomly chosen infection probabilities of nodes
    '''
    infprob_indiv = np.random.uniform(0, max_infprob_indiv, len(A))
    print(f"infprob_indiv in method is {infprob_indiv}")
    return infprob_indiv