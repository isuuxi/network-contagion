import random
import numpy as np
from sklearn.preprocessing import normalize

class ContagionProcess:
    def __init__(self, A, unweighted, method, infected, nodes_neighbors, normalized_network, method_params, noise_level, dose_level, memory_length):
        #if np.sum(np.all(A == 0, axis = 1)) == 0:
        #    self.A = A
        #else:
        #    print("Adjacency matrix contains rows with no entries")
        self.A = A
        self.unweighted = unweighted
        self.method = method
        self.method_params = method_params
        self.dose_level = dose_level
        self.inf_prob = np.zeros(len(A))
        self.infected = infected
        self.nodes_neighbors = nodes_neighbors
        self.normalized_network = normalized_network
        self.noise_level = noise_level
        #print(f"noise_level is {self.noise_level}")
        self.history = np.empty(len(self.infected))
        self.history[:] = np.NaN
        self.current_step = 0
        self.memory = np.zeros(len(self.infected))
        #print(f"in beginning memory has dimension {self.memory.ndim}")
        #self.memory[:] = np.NaN
        self.memory_storage = [] #this should not be a list! better numpy object
        self.memory_length = memory_length
        self.dose = np.empty(len(self.infected))
        self.decision = np.zeros(len(self.A))
        #print(f"in beginning decision has dimension {self.decision.ndim}")
        self._get_dose_sum = np.vectorize(self._unvectorized_get_dose_sum)
        self.noise_inf = 0
        self.contagion_inf = 0


    def step(self):
        '''
        Executes one time step of a contagion process 
        '''
        if self.noise_level > 0:
            self._update_noise_infections(self.noise_process(self.A, self.noise_level)) #+self.current_step/100000))
        if self.method == "SI_cont":
            sum_inf_neighbors = self._get_sum_inf_neighbors(self.unweighted, self.infected)
            self.inf_prob = 1 - np.power((1-self.method_params['infprob_indiv']), sum_inf_neighbors) 
            self.decision = self._mc_result(self.inf_prob)
        elif self.method == "threshold_cont":
            pass
        elif self.method == "fractional_cont":
            pass
        elif self.method == "generalized_cont":            
            rand_neighbor = np.squeeze(np.array((self.normalized_network.cumsum(1) > np.random.rand(self.normalized_network.shape[0])[:,None]).argmax(1).T))
            self.dose = self.infected[rand_neighbor]*self.dose_level 
            #self.dose = self._get_rand_neighbor_weight(rand_neighbor)*self.infected[rand_neighbor]*self.dose_level 
            #print(f"dose in step {self.current_step} is {self.dose} with dimension {self.dose.ndim}")
            self.memory = self.memory + self.dose 
            self.memory_storage.append(self.dose)
            if len(self.memory_storage) > self.memory_length:
                self.memory = self.memory - self.memory_storage[0]
                self.memory_storage.pop(0)
        else:
            print("not a valid contagion method")
        self._update_infections(self.decision)
        self.current_step += 1
        return None

    def _get_sum_inf_neighbors(self, A_unweighted, infected):  
        sum_inf_neighbors = np.dot(A_unweighted, infected)   
        return np.squeeze(np.asarray(sum_inf_neighbors))

    def _get_sum_neighbors(self, A):
        sum_neighbors = np.sum(A, axis = 1)
        return sum_neighbors

    def _mc_result(self, inf_prob):
        c = np.random.uniform(0, 1, size = inf_prob.shape)
        #print(f"infection result is {c < inf_prob }")
        return c < inf_prob 

    def _update_noise_infections(self, decision): 
        a = np.ones_like(len(decision))
        b = np.zeros(len(decision))
        x = np.where((decision == True) & (self.infected == 0), a, b)
        #print(f"variable x for update inf is {x} in step {self.current_step}")
        y = np.array(x)
        self.noise_inf = self.noise_inf + np.sum(y)
        #print(f"decision is {decision}")
        #print(f"variable for update infection is {y} with type {type(y)} in step {self.current_step}")
        self.infected[np.where(y > 0)] = 1
        self.history[np.where(y > 0)] = self.current_step


    def _update_infections(self, decision): 
        a = np.ones_like(len(decision))
        b = np.zeros(len(decision))
        x = np.where((decision == True) & (self.infected == 0), a, b)
        #print(f"variable x for update inf is {x} in step {self.current_step}")
        y = np.array(x)
        self.contagion_inf = self.contagion_inf + np.sum(y)
        #print(f"decision is {decision}")
        #print(f"variable for update infection is {y} with type {type(y)} in step {self.current_step}")
        self.infected[np.where(y > 0)] = 1
        self.history[np.where(y > 0)] = self.current_step
        

    def _unvectorized_get_dose_sum(self, sum_inf_neighbors):
        dose_vector = np.sum(np.random.uniform(0, 1, sum_inf_neighbors))
        return dose_vector

    '''''
    def _get_dose_strength(self, connected_network_nodes, x):
        dose = np.zeros(len(connected_network_nodes))
        for i in range(len(connected_network_nodes)):
            dose[i] = connected_network_nodes[i,x[i]]
        return dose
    '''
    
    def _get_rand_neighbor_weight(self, rand_neighbor):
        rand_neighbor_weight = np.zeros(len(self.normalized_network))
        for i in range(len(self.normalized_network)):
            rand_neighbor_weight[i] = self.normalized_network[i, rand_neighbor[i]]
            #N[5, rand_neighbor[5]]
        return rand_neighbor_weight


    def noise_process(self, A, noise_level):
        c = np.random.uniform(0, 1, size = len(A))
        #print(f"non zero elements in noise decision are {np.count_nonzero(c < noise_level)}")
        return c < noise_level 



''''
def node_neighbors(A):
    
    #returns a 2D array (?!) with the neighbors of each node
     #  Parameters: 
      #     A: weighted adjacency matrix of a network
       #Returns:
        #   node_neighbors: neighbors of each node
     
    node_neighbors = np.zeros(len(A))
    for i, j in enumerate(A):
        node_neighbors[j] = np.where(A[j] > 1)[i]
    return node_neighbors

'''
     



