import random
import numpy as np
from sklearn.preprocessing import normalize

class ContagionProcess:
    def __init__(self, A, method, infected, nodes_neighbors, normalized_network, method_params, noise_level, dose_level):
        if np.sum(np.all(A == 0, axis = 1)) == 0:
            self.A = A
        else:
            print("Adjacency matrix contains rows with no entries")
        self.method = method
        self.method_params = method_params
        self.dose_level = dose_level
        self.inf_prob = np.zeros(len(A))
        self.infected = infected
        self.nodes_neighbors = nodes_neighbors
        self.normalized_network = normalized_network
        self.noise_level = noise_level
        self.history = np.empty(len(self.infected))
        self.history[:] = np.NaN
        self.current_step = 0
        self.memory = np.zeros(len(self.infected))
        print(f"in beginning memory has dimension {self.memory.ndim}")
        #self.memory[:] = np.NaN
        self.memory_storage = [] #this should not be a list! better numpy object
        self.max_memory = 1000
        self.dose = np.empty(len(self.infected))
        self.decision = np.zeros(len(self.A))
        print(f"in beginning decision has dimension {self.decision.ndim}")
        self._get_dose_sum = np.vectorize(self._unvectorized_get_dose_sum)


    def step(self):
        '''
        Executes one time step of a contagion process 
        '''
        self._update_infections(self.noise_process(self.A, self.noise_level + self.current_step/100))
        if self.method == "SI_cont":
            sum_inf_neighbors = np.squeeze(np.asarray(self._get_sum_inf_neighbors(self.A, self.infected)))
            self.inf_prob = 1 - np.power((1-self.method_params['infprob_indiv']), sum_inf_neighbors) 
            self.decision = self._mc_result(self.inf_prob)
        elif self.method == "threshold_cont":
            pass
        elif self.method == "fractional_cont":
            pass
        elif self.method == "generalized_cont":            
            #sum_inf_neighbors = np.squeeze(np.asarray(self._get_sum_inf_neighbors(self.A, self.infected))).astype(int)
            #print(f"sum_inf_neighbors is {sum__neighbors}")
            #sum_neighbors = self._get_sum_neighbors(self.A)
            #rand_neighbor = random.randint(1, sum_inf_neighbors) 
            #print(f"random neighbor is {rand_neighbor}")
            #print(self.nodes_neighbors)
            #rand_neighbor = random.choice(self.nodes_neighbors)
            print(f"Adjacency matrix is {self.A} with dimension {self.A.ndim} and shape {self.A.shape}")
            rand_neighbor = (self.A.cumsum(1) > np.random.rand(self.A.shape[0])[:,None]).argmax(1)
            print(f"Random neighbour in step {self.current_step} is {rand_neighbor} with shape {rand_neighbor.shape} and dimension {rand_neighbor.ndim}")
            #dose_strength = self._get_dose_strength(self.A, rand_neighbor)*self.infected #choose different variable name
            self.dose = (rand_neighbor*self.infected)*self.dose_level
            #print(f"dose in step {self.current_step} is {self.dose} with dimension {self.dose.ndim}")
            self.memory = self.memory + self.dose 
            self.memory_storage.append(self.dose)
            #print(f"memory in step {self.current_step} is {self.memory}")
            if len(self.memory_storage) > self.max_memory:
                self.memory = self.memory - self.memory_storage[0]
                self.memory_storage.pop(0)
            self.decision = self.method_params['dose_threshold'] <  self.memory 
            #print(f"decision is {self.decision}")
        else:
            print("not a valid contagion method")
        self._update_infections(self.decision)
        self.current_step += 1
        print(f"Dose threshold is {self.method_params['dose_threshold']} with dimension {self.method_params['dose_threshold'].ndim}")
        return None


    def _get_sum_inf_neighbors(self, A, infected):  
        sum_inf_neighbors = np.dot(A, infected)       
        return np.squeeze(np.asarray(sum_inf_neighbors)).astype(int)

    def _get_sum_neighbors(self, A):
        sum_neighbors = np.sum(A, axis = 1)
        return sum_neighbors

    def _mc_result(self, inf_prob):
        c = np.random.uniform(0, 1, size = inf_prob.shape)
        return c < inf_prob 

    def _update_infections(self, decision): 
        for j in np.where(decision == 1)[0]:
            #print(f"decision in loop is {decision[j]}")
            if self.infected[j] == 0:
                self.infected[j] = decision[j]
                self.history[j] = self.current_step     
        
    def _unvectorized_get_dose_sum(self, sum_inf_neighbors):
        dose_vector = np.sum(np.random.uniform(0, 1, sum_inf_neighbors))
        return dose_vector

    def _get_dose_strength(self, connected_network_nodes, x):
        dose = np.zeros(len(connected_network_nodes))
        for i in range(len(connected_network_nodes)):
            dose[i] = connected_network_nodes[i,x[i]]
        return dose

    def noise_process(self, A, noise_level):
        c = np.random.uniform(0, 1, size = len(A))
        return c < noise_level 

def get_infprob_indiv(A):
    '''
    returns the individual infection probability of each node
       Parameters: 
           A: adjacency matrix of a network
       Returns:
           infprob_indiv: numpy array with randomly chosen infection probabilities of nodes
    '''
    infprob_indiv = np.random.uniform(0, 0.4, len(A))
    return infprob_indiv



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
     



