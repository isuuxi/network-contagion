import numpy as np
from run_model import run_model
#from parameters import max_dose_threshold
import pandas as pd
import json

###################################
###### set configuration grid #####
###################################
'''''
dosesshort = [ 0, 0.01, 0.05]
noises = [0, 0.00001, 0.005]
times = [100, 500]
max_infprob_indivs = [0.05, 0.1]
#network parameters
sizes = [500, 1000]
experiments = 5
p = 0.1
m_values = [2, 4]
k = 25
betas = [0.1, 0.3]
read_infected = False
initial_infecteds = [1, 20]
#network types: "empirical", "erdos", "barabasi", "watts"
#network_types = ["erdos", "barabasi", "watts"]
network_types = ["erdos"]
methods = ["SI_cont", "generalized_cont"]
'''

dose = 0.01
max_dose_thresholds = [0.5, 1, 1.5]
noises = [0]
times = [5000]
max_infprob_indivs = [0.02, 0.04, 0.08]
#network parameters
sizes = [1600]
experiments = range(10, 99)
#p = 1/12
m_values = [24]
k = 24
betas = [0.1]
read_infected = False
initial_infecteds = [50]
#network types: "empirical", "erdos", "barabasi", "watts"
#network_types = ["erdos", "barabasi", "watts"]
network_types = ["watts"]
methods = ["generalized_cont", "SI_cont"]


#########################################
##### run with given configurations #####
#########################################

for method in methods: 
    if method == "generalized_cont":
        infprobindiv = 0
        for network_type in network_types:
            for initial_infected in initial_infecteds:
                for time_entry in times:
                    for noise in noises:
                        for max_dose_threshold in max_dose_thresholds:
                            if network_type == "empirical":
                                p = 0
                                size = 5289
                                k = 0
                                beta = 0
                                m = 0
                                for experiment in range(experiments): 
                                    if (noise==0) and (dose==0):
                                        pass
                                    else:
                                        #text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                        #if match_string(text) == False:
                                        print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                        run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                        with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/data_empirical/identifiers_empirical.txt", "a") as f:
                                            f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")
                                        #else:
                                        #   pass
                            elif network_type == "erdos":
                                p = 0.024
                                k = 0
                                beta = 0
                                m = 0
                                for size in sizes:
                                    for experiment in range(experiments): 
                                        if (noise==0) and (dose==0):
                                            pass
                                        else:
                                            text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                            #if match_string(text) == False:
                                            print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                            run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                            with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/noise0/data_erdos/identifiers_erdos.txt", "a") as f:
                                                f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"+ "\n")
                                            #else:
                                        #    pass                                        
                            elif network_type == "barabasi":
                                k = 0
                                p = 0
                                beta = 0
                                for m in m_values:
                                    for size in sizes:
                                        for experiment in range(experiments): 
                                            if (noise==0) and (dose==0):
                                                pass
                                            else:
                                                text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                               # if match_string(text) == False:
                                                print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                                run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                                with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/noise0/data_barabasi/identifiers_barabasi.txt", "a") as f:
                                                    f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"+ "\n")
                                               # else:
                                                #    pass
                            elif network_type == "watts":
                                k = 24
                                m = 0
                                p = 0
                                for beta in betas:
                                    for size in sizes:
                                        for experiment in experiments: 
                                            if (noise==0) and (dose==0):
                                                pass
                                            else:
                                                text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                            # if match_string(text) == False:
                                                print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                                run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                                with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/noise0/data_watts/identifiers_watts.txt", "a") as f:
                                                    f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"+ "\n")
                                            # else:
                                                #    pass

    elif method == "SI_cont":
        dose = 0
        max_dose_threshold = 0
        for network_type in network_types:
            for initial_infected in initial_infecteds:
                for time_entry in times:
                    for noise in noises:
                            for infprobindiv in max_infprob_indivs:
                                if network_type == "empirical":
                                    p = 0
                                    size = 5289
                                    k = 0
                                    beta = 0
                                    m = 0
                                    for experiment in range(experiments): 
                                        if (noise==0) and (infprobindiv==0):
                                            pass
                                        else:
                                            text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                            #if match_string(text) == False:
                                            print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                            run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                            with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/data_empirical/identifiers_empirical.txt", "a") as f:
                                                f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")
                                        # else:
                                         #   pass
                                elif network_type == "erdos":
                                    p = 0.024
                                    k = 0
                                    beta = 0
                                    m = 0
                                    for size in sizes:
                                        for experiment in range(experiments): 
                                            if (noise==0) and (infprobindiv==0):
                                                pass
                                            else:
                                                text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                                #if match_string(text) == False:
                                                print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                                run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                                with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/noise0/data_erdos/identifiers_erdos.txt", "a") as f:
                                                    f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")
                                                #else:
                                                # pass 
                                elif network_type == "barabasi":
                                    k = 0
                                    p = 0
                                    beta = 0
                                    for m in m_values:
                                        for size in sizes:
                                            for experiment in range(experiments): 
                                                if (noise==0) and (infprobindiv==0):
                                                    pass
                                                else:
                                                    text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                                    #if match_string(text) == False:
                                                    print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                                    run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                                    with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/noise0/data_barabasi/identifiers_barabasi.txt", "a") as f:
                                                        f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")
                                                    #else:
                                                    #   pass
                                elif network_type == "watts":
                                    k = 24
                                    m = 0
                                    p = 0
                                    for beta in betas:
                                        for size in sizes:
                                            for experiment in experiments: 
                                                if (noise==0) and (infprobindiv==0):
                                                    pass
                                                else:
                                                    text = f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"
                                                    #if match_string(text) == False:
                                                    print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                                    run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, max_dose_threshold, infprobindiv, initial_infected)
                                                    with open(r"C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion/data/noise0/data_watts/identifiers_watts.txt", "a") as f:
                                                        f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")                              
                                                    #else:
                                                        #pass
    else: 
        print("Not a valid contagion method")


