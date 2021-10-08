import random
import numpy as np

class ContagionProcess:
    def __init__(self, A, infprob_indiv, method, infected):
        self.A = A
        self.infprob_indiv = infprob_indiv 
        self.method = method
        self.inf_prob = np.zeros(len(A))
        self.infected = infected
        self.history = np.empty(len(self.infected))
        self.history[:] = np.NaN
        self.current_step = 0

    def step(self):
        if self.method == "SI_cont":
            sum_inf_neighbors = np.squeeze(np.asarray(self._get_sum_inf_neighbors(self.A, self.infected)))
            for i in range(len(self.A)):
                self.inf_prob[i] = 1 - np.power((1-self.infprob_indiv[i]), sum_inf_neighbors[i])
        elif self.method == "threshold_cont":
            pass
        elif self.method == "fractional_cont":
            pass
        elif self.method == "generalized_cont":
            pass
        else:
            print("not a valid contagion method")
        decision = self._mc_result(self.inf_prob)
        self._update_infections(decision)
        self.current_step += 1
        return None

    def _get_sum_inf_neighbors(self, A, infected):         
        return np.dot(A, infected)

    def _mc_result(self, inf_prob):
        c = np.random.uniform(0, 1, size = inf_prob.shape)
        return c < inf_prob 

    def _update_infections(self, decision): 
        for j in np.where(decision == 1)[0]:
            if self.infected[j] == 0:
                self.infected[j] = decision[j]
                self.history[j] = self.current_step     
        
def get_infprob_indiv(A):
    infprob_indiv = np.random.uniform(0, 0.4, len(A))
    return infprob_indiv

