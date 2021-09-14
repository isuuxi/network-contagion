import SI_model
import numpy as np

from utils import get_inf_pressure

A = SI_model.create_network(200, 0.06)
A, current_infected_nodes, infprob_nodes = SI_model.init_network(A)
print("Current infected nodes are {} ".format(current_infected_nodes))
#print(infprob_nodes)
#print(list(G.nodes))
#print(list(G.edges))

inf_p = get_inf_pressure(A, current_infected_nodes, infprob_nodes)

print ("Infection pressure is {} ".format(inf_p))

print(np.where(current_infected_nodes ==1))

def inf_index(list):
    for i, j in enumerate(list):
        if j ==1:
            index = i
    return index

index = inf_index(current_infected_nodes)
print("Index of first infection is {}".format(index))
print("Neighbors of infected node are {}".format([n for n in A[index]]))