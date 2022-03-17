import json
import numpy as np
from run_model import *
from parameters import max_dose_threshold, method

##parameters to change##
#dose level to control contagion spread: 0.001 to 1 in steps of
#noise: 0 to 0.1 in steps of 
#time to control contagion development: 200 to 1000
#size ? 500, 1000, 1500

#doses = np.arange(0.1, 1, 0.2)
dosesshort = [ 0.1]
noises = [0.0001]
times = [500]
sizes = [200]
experiments = 1
p = 0.1
empirical_network = True
max_infprob_indivs = [0.01]
current_path = Path.cwd()
mypath = os.path.join(current_path.parent)

if method == "Generalized_cont":
    max_infprob_indivs = [0]
    for size in sizes:
        for time_entry in times:
            for noise in noises:
                for dose in dosesshort:
                    for infprobindiv in max_infprob_indivs:
                        for experiment in range(experiments):
                            print(f"running for {size, time_entry, noise, dose, experiment}")
                            run_model(time_entry, size, p, noise, dose, experiment, empirical_network, infprobindiv)
                            with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion\identifiers.txt", "a") as f:
                                if empirical_network:
                                    f.write(f"{method}_t{time_entry}_empricalnetwork_threshold{max_dose_threshold}_dose{dose}_noise{noise}_experiment{experiment}!config_cluster.py" + "\n")
                                else:
                                    f.write(f"{method}_t{time_entry}_n{size}_p{p}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_experiment{experiment}!config_cluster.py" + "\n")
elif method == "SI_cont":
     doses = [0]
     for size in sizes:
        for time_entry in times:
            for noise in noises:
                for dose in doses:
                    for infprobindiv in max_infprob_indivs:
                        for experiment in range(experiments):
                            print(f"running for {size, time_entry, noise, dose, experiment, infprobindiv}")
                            run_model(time_entry, size, p, noise, dose, experiment, empirical_network, infprobindiv)
                            with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion\identifiers.txt", "a") as f:
                                if empirical_network:
                                    f.write(f"{method}_t{time_entry}_empricalnetwork_noise{noise}_experiment{experiment}_infprobindiv{infprobindiv}!config_cluster.py" + "\n")
                                else:
                                    f.write(f"{method}_t{time_entry}_n{size}_p{p}_noise{noise}_experiment{experiment}_infprobindiv{infprobindiv}!config_cluster.py" + "\n")
else: 
    print("Not a valid contagion method")


                    #file1 = open("C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion\identifiers.txt", "a") #append mode
                    #file1.write(f"network_{method}_t{time_entry}_n{size}_p{p}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_experiment{experiments}")
                    #file1.close()


#run_model(100, 0, 0, 0.0001, 0.1, 1, True)
#config = {
 #   "size" : sizes,
 #   "timesteps" : times,
 #   "noise" : noises,
 #   "dose" : doses
#}
#myJSON = json.dumps(config)

#with open(f"config_{sizes}_{}_{}_{}_{}_.json", "w") as jsonfile:
#    jsonfile.write(myJSON)
#    print("Write successful")