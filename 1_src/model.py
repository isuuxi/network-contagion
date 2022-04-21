import numpy as np

class ContagionProcess:
    def __init__(self, A, method, infected, nodes_neighbors, A_norm, method_params, noise_level, dose_level, memory_length):
        #if np.sum(np.all(A == 0, axis = 1)) == 0:
        #    self.A = A
        #else:
        #    print("Adjacency matrix contains rows with no entries")
        self.A = A
        self.method = method
        self.method_params = method_params
        self.dose_level = dose_level
        self.infected = infected
        self.nodes_neighbors = nodes_neighbors
        self.A_norm = A_norm
        self.noise_level = noise_level
        self.history = np.zeros(len(infected))
        self.history[:] = np.NaN
        self.history[np.where(self.infected == 1)] = 0
        self.current_step = 0
        self.memory = np.zeros(len(self.infected))
        self.memory_length = memory_length
        self.memory_storage = []
        self.dose = np.empty(len(self.infected))
        self.decision = np.zeros(len(self.A))
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
            self.infprob = self._get_infprob(self.A_norm, self.infected)
            self.decision = self._mc_result(self.infprob)
        elif self.method == "generalized_cont":            
            rand_neighbor = np.squeeze(np.array((self.A_norm.cumsum(1) > np.random.rand(self.A_norm.shape[0])[:,None]).argmax(1).T))
            self.dose = self.infected[rand_neighbor]*self.dose_level 
            self.memory = self.memory + self.dose 
            self.memory_storage.append(self.dose)
            if len(self.memory_storage) > self.memory_length:
                self.memory = self.memory - self.memory_storage[0]
                self.memory_storage.pop(0)
            self.decision = self.method_params['dose_threshold'] <  self.memory
        else:
            print("not a valid contagion method")
        self._update_infections(self.decision)
        self.current_step += 1
        return None

    def _get_infprob(self, A_norm, infected):
        A_infected = np.multiply(A_norm, infected[np.newaxis, :])
        P = 1 - A_infected*self.method_params['infprob_indiv']
        infprob = 1 - np.prod(P, axis = 1)
        return infprob

    def _get_sum_inf_neighbors(self, A_unweighted, infected):  
        sum_inf_neighbors = np.dot(A_unweighted, infected)   
        return np.squeeze(np.asarray(sum_inf_neighbors))

    def _get_sum_neighbors(self, A):
        sum_neighbors = np.sum(A, axis = 1)
        return sum_neighbors

    def _mc_result(self, inf_prob):
        c = np.random.uniform(0, 1, size = inf_prob.shape)
        return c < inf_prob 

    def _update_noise_infections(self, decision): 
        a = np.ones_like(len(decision))
        b = np.zeros(len(decision))
        x = np.where((decision == True) & (self.infected == 0), a, b)
        y = np.array(x)
        self.noise_inf = self.noise_inf + np.sum(y)
        self.infected[np.where(y > 0)] = 1
        self.history[np.where(y > 0)] = self.current_step + 1

    def _update_infections(self, decision): 
        a = np.ones_like(len(decision))
        b = np.zeros(len(decision))
        x = np.where((decision == True) & (self.infected == 0), a, b)
        y = np.array(x)
        self.contagion_inf = self.contagion_inf + np.sum(y)
        self.infected[np.where(y > 0)] = 1
        self.history[np.where(y > 0)] = self.current_step + 1
        
    def _unvectorized_get_dose_sum(self, sum_inf_neighbors):
        dose_vector = np.sum(np.random.uniform(0, 1, sum_inf_neighbors))
        return dose_vector

    def noise_process(self, A, noise_level):
        c = np.random.uniform(0, 1, size = len(A))
        return c < noise_level 

    '''''
    def _get_rand_neighbor_weight(self, rand_neighbor):
        rand_neighbor_weight = np.zeros(len(self.A_norm))
        for i in range(len(self.A_norm)):
            rand_neighbor_weight[i] = self.A_norm[i, rand_neighbor[i]]
        return rand_neighbor_weight
    
    def _get_dose_strength(self, connected_network_nodes, x):
        dose = np.zeros(len(connected_network_nodes))
        for i in range(len(connected_network_nodes)):
            dose[i] = connected_network_nodes[i,x[i]]
        return dose
    '''
    
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
     



