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
dosesshort = [0.001, 0.1, 0.5, 1]
noises = [0]
times = [500]
sizes = [500]
experiments = 10
p = 0.01
empirical_network = False
current_path = Path.cwd()
mypath = os.path.join(current_path.parent)
print(f"current path parent is {current_path.parent}")
print(f"current path  is {mypath}")

#assert os.path.isfile(path)
#with open(path, "r") as f:
#    pass

for size in sizes:
    for time_entry in times:
        for noise in noises:
            for dose in dosesshort:
                for experiment in range(experiments):
                    print(f"running for {size, time_entry, noise, dose, experiment}")
                    run_model(time_entry, size, p, noise, dose, experiment, empirical_network)
                    with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion\identifiers.txt", "a") as f:
                        f.write(f"network_{method}_t{time_entry}_n{size}_p{p}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_experiment{experiments}-config_cluster.py" + "\n")


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