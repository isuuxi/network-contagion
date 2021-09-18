import SI_model
import numpy as np

from utils import get_inf_pressure
from utils import mc_result


A = SI_model.create_network(5000, 0.009)
A, current_infected_nodes, infprob_nodes = SI_model.init_network(A)
#print("Current infected nodes are {} ".format(current_infected_nodes))
#print(infprob_nodes)
#print(list(G.nodes))
#print(list(G.edges))

time_series = SI_model.time_step(A, current_infected_nodes, infprob_nodes, 30)
print("Time series of infections is {} ".format(time_series))
#print(len(time_series))



#inf_p = get_inf_pressure(A, current_infected_nodes, infprob_nodes)

#decision, c = mc_result(inf_p)

#print ("Infection pressure is {} ".format(inf_p))
#print("Infection decision list for all nodes is {}".format(decision))

#print("Criterion is {}".format(c))

#print(np.where(current_infected_nodes ==1))

#def inf_index(list):
 #   for i, j in enumerate(list):
 #      if j ==1:
 #           index = i
 #  return index

#index = inf_index(current_infected_nodes)
#print("Index of first infection is {}".format(index))
#print("Neighbors of infected node are {}".format([n for n in A[index]]))