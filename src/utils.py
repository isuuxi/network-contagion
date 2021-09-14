import random
import numpy as np

def get_inf_pressure(G, current_infected_nodes, infprob):
    inf_pressure = np.zeros(len(G))
    for n in G:
        sum = 0
        for x in G.neighbors(n):
           if current_infected_nodes[x] ==1:
               sum += 1
               print("one infection {}".format(sum))
        if sum == 1:
            inf_pressure[n] = infprob[n]
        elif sum == 0:
            inf_pressure[n] = 0
        else:
            inf_pressure[n] = infprob[n] + sum/G.neighbors(n)*infprob[n]
    return inf_pressure

def get_infprob(A):
    infprob = np.random.uniform(0, 0.5, len(A))
    return infprob

def mc_result(inf_pressure):
    return decision


