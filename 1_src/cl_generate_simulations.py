import numpy as np
from cl_run_model import run_model
from parameters import max_dose_threshold
import pandas as pd
import json

###################################
###### set configuration grid #####
###################################
dosesshort = [ 0, 0.01, 0.1]
noises = [0, 0.00001, 0.01]
times = [100, 250, 500]
max_infprob_indivs = [0.05, 0.1]
#network parameters
#sizes = [500, 1000, 5000]
sizes = [500, 1000]
experiments = 5
p = 0.1
m_values = [2, 4]
k = 25
betas = [0.1, 0.3]
read_infected = False
initial_infecteds = [1, 20]
#network types: "emprical", "erdos", "barabasi", "barabasi"
network_types = ["barabasi"]
methods = ["SI_cont", "generalized_cont"]

if read_infected == True:
    infected = pd.read_csv(filepath_or_buffer="/p/tmp/isabellf/data_5/SI_cont_t500_n200_p0.1_infprobindiv0.01_noise0.0001/infected_SI_cont_t500_n200_p0.1_threshold1.6_dose0_noise0.0001_experiment0.csv")
    infected = np.squeeze(infected.to_numpy())
    print(f"infected is {infected}")
else:
    infected = "no"


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
                        for dose in dosesshort:
                            if network_type == "empirical":
                                p = 0
                                size = 5289
                                k = 0
                                beta = 0
                                m = 0
                                for experiment in range(experiments): 
                                    print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                    run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                    with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                        f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"+ "\n")
                            elif network_type == "erdos":
                                p = 0.1
                                k = 0
                                beta = 0
                                m = 0
                                for size in sizes:
                                    for experiment in range(experiments): 
                                        print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                        run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                        with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                            f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"+ "\n")
                            elif network_type == "barabasi":
                                k = 0
                                p = 0
                                beta = 0
                                for m in m_values:
                                    for size in sizes:
                                        for experiment in range(experiments): 
                                            print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                            run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                            with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                                f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"+ "\n")
                            elif network_type == "barabasi":
                                k = 25
                                m = 0
                                p = 0
                                for beta in betas:
                                    for size in sizes:
                                        for experiment in range(experiments): 
                                            print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                            run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                            with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                                f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_threshold{max_dose_threshold}_dose{dose}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py"+ "\n")
    elif method == "SI_cont":
        dose = 0
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
                                        print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                        run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                        with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                            f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")
                                elif network_type == "erdos":
                                    p = 0.1
                                    k = 0
                                    beta = 0
                                    m = 0
                                    for size in sizes:
                                        for experiment in range(experiments): 
                                            print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                            run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                            with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                                f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")
                                elif network_type == "barabasi":
                                    k = 0
                                    p = 0
                                    beta = 0
                                    for m in m_values:
                                        for size in sizes:
                                            for experiment in range(experiments): 
                                                print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                                run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                                with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                                    f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")
                                elif network_type == "barabasi":
                                    k = 25
                                    m = 0
                                    p = 0
                                    for beta in betas:
                                        for size in sizes:
                                            for experiment in range(experiments): 
                                                print(f"running for {method, network_type, size, time_entry, noise, dose, experiment, infprobindiv}")
                                                run_model(method, time_entry, size, p, k, beta, m, noise, dose, experiment, network_type, infprobindiv, initial_infected)
                                                with open(r"/p/tmp/isabellf/data_barabasi/identifiers.txt", "a") as f:
                                                    f.write(f"{method}_t{time_entry}_network{network_type}_n{size}_p{p}_beta{beta}_m{m}_infprobindiv{infprobindiv}_noise{noise}_initialinf{initial_infected}_experiment{experiment}!config_cluster.py" + "\n")                              
    else: 
        print("Not a valid contagion method")
