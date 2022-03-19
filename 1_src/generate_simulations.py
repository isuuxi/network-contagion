import numpy as np
from run_model import *
from parameters import max_dose_threshold, method
import pandas as pd

###################################
###### set configuration grid #####
###################################
dosesshort = [ 0.1]
noises = [0.001]
times = [20]
sizes = [200]
experiments = 1
p = 0.1
empirical_network = False
max_infprob_indivs = [0.8]
read_infected = True

if read_infected == True:
    infected = pd.read_csv(filepath_or_buffer="C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/SI_cont_t500_n200_p0.1_infprobindiv0.01_noise0.0001/infected_SI_cont_t500_n200_p0.1_threshold1.6_dose0_noise0.0001_experiment0.csv")
    infected = np.squeeze(infected.to_numpy())
    print(f"infected is {infected}")
else:
    infected = "no"
    
#########################################
##### run with given configurations #####
#########################################
if method == "Generalized_cont":
    max_infprob_indivs = [0]
    for size in sizes:
        for time_entry in times:
            for noise in noises:
                for dose in dosesshort:
                    for infprobindiv in max_infprob_indivs:
                        for experiment in range(experiments):
                            print(f"running for {size, time_entry, noise, dose, experiment}")
                            run_model(time_entry, size, p, noise, dose, experiment, empirical_network, infprobindiv, infected)
                            with open(r"C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/identifiers.txt", "a") as f:
                                if empirical_network:
                                    f.write(f"{method}_t{time_entry}_empricalnetwork_threshold{max_dose_threshold}_dose{dose}_noise{noise}_experiment{experiment}!config_cluster.py" + "/n")
                                else:
                                    f.write(f"{method}_t{time_entry}_n{size}_p{p}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_experiment{experiment}!config_cluster.py" + "/n")
elif method == "SI_cont":
     doses = [0]
     for size in sizes:
        for time_entry in times:
            for noise in noises:
                for dose in doses:
                    for infprobindiv in max_infprob_indivs:
                        for experiment in range(experiments): 
                            print(f"running for {size, time_entry, noise, dose, experiment, infprobindiv}")
                            run_model(time_entry, size, p, noise, dose, experiment, empirical_network, infprobindiv, infected)
                            with open(r"C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/identifiers.txt", "a") as f:
                                if empirical_network:
                                    f.write(f"{method}_t{time_entry}_empricalnetwork_noise{noise}_experiment{experiment}_infprobindiv{infprobindiv}_experiment{experiment}!config_cluster.py" + "/n")
                                else:
                                    f.write(f"{method}_t{time_entry}_n{size}_p{p}_noise{noise}_experiment{experiment}_infprobindiv{infprobindiv}_experiment{experiment}!config_cluster.py" + "/n")
else: 
    print("Not a valid contagion method")
