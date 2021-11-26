import random
import numpy as np

class ContagionProcess:
    def __init__(self, A, method, infected, method_params):
        self.A = A
        self.method = method
        self.method_params = method_params
        self.inf_prob = np.zeros(len(A))
        self.infected = infected
        self.history = np.empty(len(self.infected))
        self.history[:] = np.NaN
        self.current_step = 0
        self.memory = np.empty(len(self.infected))
        self.memory[:] = np.NaN
        self.dose = np.empty(len(self.infected))
        self.decision = np.zeros(len(self.A))
        self._get_dose_sum = np.vectorize(self._unvectorized_get_dose_sum)

    def step(self):
        '''
        Executes one time step of a contagion process 
        '''
        if self.method == "SI_cont":
            sum_inf_neighbors = np.squeeze(np.asarray(self._get_sum_inf_neighbors(self.A, self.infected)))
            self.inf_prob = 1 - np.power((1-self.method_params['infprob_indiv']), sum_inf_neighbors)
            self.decision = self._mc_result(self.inf_prob)
        elif self.method == "threshold_cont":
            pass
        elif self.method == "fractional_cont":
            pass
        elif self.method == "generalized_cont":
            sum_inf_neighbors = np.squeeze(np.asarray(self._get_sum_inf_neighbors(self.A, self.infected))).astype(int)
            self.dose = self._get_dose_sum(sum_inf_neighbors)
            self.memory = self.memory + self.dose
            self.decision = self.method_params['dose_threshold'] < self.dose #MEMORY!!
        else:
            print("not a valid contagion method")
        self._update_infections(self.decision)
        self.current_step += 1
        return None

    def _get_sum_inf_neighbors(self, A, infected):  
        sum_inf_neighbors = np.dot(A, infected)       
        return np.squeeze(np.asarray(sum_inf_neighbors)).astype(int)

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