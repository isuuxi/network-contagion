import initialization
import numpy as np
import networkx as nx
import model
import time 
import csv
import math
import os
from pathlib import Path
import json
import random
import pandas as pd

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

#plt.style.use('_mpl-gallery-nogrid')

# make data: correlated + noise

d = {'nodes': [100, 100, 100, 100, 100, 100, 100], 'contagion_inf': [50, 40, 40, 60, 70, 70, 70], 'noise_inf': [30, 20, 60, 5, 10, 10, 10]}
infection_data = pd.DataFrame(data = d)
infection_data['signal_to_noise'] = infection_data['contagion_inf']/infection_data['noise_inf']
infection_data['infected_fraction'] = (infection_data['contagion_inf']+infection_data['noise_inf'])/infection_data['nodes']
Q = [0, 0, 0.01, 0, 0.1, 0.05, 0.08]

print(infection_data)

np.random.seed(1)
x = infection_data['signal_to_noise']
y = infection_data['infected_fraction']

new_range = include_in_range([xbins, ybins], self.emp_DRF_params)

# plot:
fig, ax = plt.subplots()

ax.hist2d(x, y, bins=(np.arange(0, 15, 0.1), np.arange(0, 1, 0.005)))

patch = mpatches.Patch(color='#D9CBDC', label='Q '.format(Q))
ax.set(xlim=(0, 13), ylim=(0, 1))
ax.set_xlabel("signal to noise ratio")
ax.set_ylabel("percentage of network infected")
plt.colorbar(im, ax=ax, label="Probability density")

plt.show()



#G = initialization.create_network(6, 0.1)
#network_adj, normalized_network, infected, infprob_indiv_nodes, dose_threshold, nodes_neighbors = initialization.init_network(G)

#def _update_infections(decision): 
    #x = np.where((decision == True) & (infected == 0))
   # y = np.array(x)
    #print(f"decision is {decision}")
    #print(f"variable for update infection is {y} with type {type(y)} in step {self.current_step}")
  #  infected[y] = 1
 #   history[y] = current_step
    #for j in np.where(decision == 1)[0]:
        #   print(f"decision in loop is {decision[j]}")
        #  if self.infected[j] == 0:
        #     self.infected[j] = decision[j]
        #    self.history[j] = self.current_step     
        
#'dose_threshold' <  memory 



#print(f"adj matrix after creation is {G}")
#A, N, infected, infprob_indiv_nodes, dose_threshold, nodes_neighbors = initialization.init_network(G)
#print(f"A[0] is {A[0]}")
#print(f"A[1] is {A[1]}")
#print(f"A[2] is {A[2]}")

##############update infections########################
#print(N)
#rand_neighbor = np.squeeze(np.array((N.cumsum(1) > np.random.rand(N.shape[0])[:,None]).argmax(1).T))

#def _get_rand_neighbor_weight(rand_neighbor, normalized_network):
#    rand_neighbor_weight = np.zeros(len(normalized_network))
#    for i in range(len(normalized_network)):
#        rand_neighbor_weight[i] = normalized_network[rand_neighbor[i], i]
#    return rand_neighbor_weight

#print(f"weight of 5 is {N[5, rand_neighbor[5]]}")
#x = range(len(N))
#print(x)
#rand_neighbor_weight = _get_rand_neighbor_weight(rand_neighbor, N)
#print(f"rand neighbor  is {rand_neighbor}")
#print(f"rand neighbor weight is {rand_neighbor_weight}")
#decision = np.array([False, False, True, False, False, False, True, False])
#arr = np.array([0, 1, 0, 1, 0, 1, 5, 5])
#weights = np.array([0.1, 0.2, 0.3, 0.2, 0.1, 0.3, 0.4, 0.1])
#print(len(weights))
#dose_level = 0.1
#product = weights * arr * dose_level
#print(product)
#print(decision)
#x = np.where((decision == True) & (arr > 4))
#y = np.array(x)
#print(f"x is {x} with type {type(x)} and y is {y}")

#combined = np.stack((decision, arr))
#print(combined)
#sumup = np.sum(combined, axis = 0)
#print(sumup)

#x = np.where((decision == True) & (arr == 1))
#print(x[0])
#arr[x] = 1
#print(f"updated array is {arr}")

#x = 

#ich möchte eine Liste/ array in dem jeder Node alle benachbarten Node-Indizes zugeordnet sind.

#nodes_neighbors = [None]*(len(A))
#print(nodes_neighbors)
#print(len(A))
#print(f"Network is {A}")
#for i in range(len(N)):
    #print(A[i])
    #print(f"i is {i}")
    #nodes_neighbors[i] = np.squeeze(np.nonzero(N[i])[1])
    #nodes_neighbors[i] = (np.nonzero(A[i]))
    #print(f"This is i: {i} and this is j:{j}")
    #print(f"Element wise is {A[i]}")
    #nodes_neighbors[i] = np.where(A[j] > 0 , j)
##    for j in A[i]:
#        print(A[i][j])

#print(nodes_neighbors)
#print(nodes_neighbors[1])
#print(f"random choices are {random.choice(nodes_neighbors)}")
#nonzero = np.apply_along_axis(np.ndarray.nonzero(A))
#print(f"nonzero is {nonzero}")

#for i in range(len(nodes_neighbors)):
    #choice = random.choice(nodes_neighbors[i])

#print(f"choice is {choice}")

#print(f"Normalized network is {N}")

#x = (N.cumsum(1) > np.random.rand(N.shape[0])[:,None]).argmax(1)
#x = np.where(N.cumsum(1) >= 1, (N.cumsum(1) > np.random.rand(N.shape[0])[:,None]).argmax(1), "None")
#connected_network_nodes = N[~np.all(N == 0, axis = 1)]
#connected_network_nodes = connected_network_nodes[:, ~np.all(connected_network_nodes == 0, axis = 0)]

#sum = np.sum(N, axis = 1) 

#o = np.array([[0, 1, 1],[0, 0, 1], [0, 0, 1]])
#giveout = o[:, np.all(o == 0, axis = 0)]

#if np.any(np.sum == 0):
#    print("contains not connected nodes")
#print(f"givout of network is {giveout}")
#print(f"dim is {o.ndim}")

#print(f"Connected network is {connected_network_nodes}")
#print(f"shape of connected network is {connected_network_nodes.shape}")
#sum = np.sum(N, axis = 1)
#print(f"sum is {sum}")
#x = np.where(np.sum(N, axis = 1) >= 1, 1, 0)
#print(x)

#x = (connected_network_nodes.cumsum(1) > np.random.rand(connected_network_nodes.shape[0])[:,None]).argmax(1) #wkt einer exposure hängt von weight ab?!
#print(f"x is {x}")


#def calc_dose(connected_network_nodes, x):
#    dose = np.zeros(len(connected_network_nodes))
#    for i in range(len(connected_network_nodes)):
#        dose[i] = connected_network_nodes[i,x[i]]
#    return dose

#inf = [0, 1, 0, 1, 0, 1]
#vec_calc_dose = np.vectorize(calc_dose)

#dose = calc_dose(connected_network_nodes, x)

#inf_dose = dose*inf
#print(f"inf_dose is {inf_dose}")

#print(f"dose is {dose}")
#print(f"selected nodes are {connected_network_nodes}")
#print(x[3])
#print(x[2])
#print(x[1])
#print(connected_network_nodes[1][1])

''''
def random_choice(N):
    if any(N):
       x = (N.cumsum(1) > np.random.rand(N.shape[0])[:,None]).argmax(1)
    else:
        x = "None"
    return x
'''


# v_random_choice = np.vectorize(random_choice)
#x = random_choice(N)
#print(x)

#print(N)

''''
count = 0
count2 = 0
for i in range(0, len(A)):
    temp = len(A[i])
    for j in range(0, temp):
        count = count + 1
        print(count, " Item of array is: ", A[i][j])
        temp2 = len(A[j])
        for z in range(0, temp2):
            count2 = count2 + 1
            print(count2, " Item of array is: ", A[i][j][z])
'''
