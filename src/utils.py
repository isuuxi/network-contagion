import random
import numpy as np

def get_inf_pressure(A, current_infected_nodes, infprob):
    '''
    Calculates the infection pressure of each node
        Parameters:
            A: matrix that represents a network
            current_infected_nodes (list): infection status of all nodes; has one infected node after initialization
            infprob_nodes (list): infection probabilities of all nodes in network A

        Returns:
            inf_pressure (list): infection pressure of all nodes in network A
    '''
    inf_pressure = np.zeros(len(A))
    for i, n in enumerate(A):
        sum = 0
        for x in A.neighbors(i):
           if current_infected_nodes[x] ==1:
               sum += 1
        if sum == 1:
            inf_pressure[i] = infprob[i]
        elif sum == 0:
            inf_pressure[i] = 0
        else:
            inf_pressure[i] = infprob[i] + (sum/len((list(A.neighbors(i)))))*infprob[i]
    return inf_pressure

def get_infprob(A):
    infprob = np.random.uniform(0, 0.4, len(A))
    return infprob

def mc_result(inf_pressure):
    c = np.random.uniform(0, 1, size = inf_pressure.shape)
    return c < inf_pressure, c
    

