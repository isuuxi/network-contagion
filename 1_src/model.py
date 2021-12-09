import random
import numpy as np
from sklearn.preprocessing import normalize

class ContagionProcess:
    def __init__(self, A, method, infected, method_params, noise_level, dose_level):
        self.A = A
        self.method = method
        self.method_params = method_params
        self.dose_level = dose_level
        self.inf_prob = np.zeros(len(A))
        self.infected = infected
        self.noise_level = noise_level
        self.history = np.empty(len(self.infected))
        self.history[:] = np.NaN
        self.current_step = 0
        self.memory = np.empty(len(self.infected))
        self.memory[:] = np.NaN
        self.memory_storage = []
        self.max_memory = 1000
        self.dose = np.empty(len(self.infected))
        self.decision = np.zeros(len(self.A))
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
            N = get_normalized_weights(self.A) # implement this somewhere else or it will be calculated in every step
            
            sum_inf_neighbors = np.squeeze(np.asarray(self._get_sum_inf_neighbors(self.A, self.infected))).astype(int)
            #print(f"sum_inf_neighbors is {sum__neighbors}")
            #rand_vec = np.vectorize(random.randint)
            sum_neighbors = self._get_sum_neighbors(self.A)
            rand_neighbor = random.randint(1, sum_inf_neighbors) 
            print(f"random neighbor is {rand_neighbor}")
            self.dose = self.dose_level*N[rand_neighbor]*self.infected[rand_neighbor]
            self.memory = self.memory + self.dose 
            self.memory_storage.append(self.dose)
            if len(self.memory_storage) > self.max_memory:
                self.memory = self.memory - self.memory_storage[0]
                self.memory_storage.pop(0)
            self.decision = self.method_params['dose_threshold'] <  self.memory 
        else:
            print("not a valid contagion method")
        self._update_infections(self.decision)
        self.current_step += 1
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
            if self.infected[j] == 0:
                self.infected[j] = decision[j]
                self.history[j] = self.current_step     
        
    def _unvectorized_get_dose_sum(self, sum_inf_neighbors):
        dose_vector = np.sum(np.random.uniform(0, 1, sum_inf_neighbors))
        return dose_vector

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


def get_dose_threshold(A):
    '''
    returns the individual infection threshold of doses received of each node
       Parameters: 
           A: adjacency matrix of a network
       Returns:
           dose_threshold: numpy array with randomly chosen dose threshold of nodes
    '''
    dose_threshold = np.random.uniform(0, 5, len(A))
    return dose_threshold

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

def node_neighbors(A):
    '''
    returns a 2D array (?!) with the neighbors of each node
       Parameters: 
           A: weighted adjacency matrix of a network
       Returns:
           node_neighbors: neighbors of each node
    '''  
    node_neighbors = np.zeros(len(A))
    for i, j in enumerate(A):
        node_neighbors[j] = np.where(A[j] > 1)[i]
    return node_neighbors


     



