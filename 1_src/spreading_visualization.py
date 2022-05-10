
import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np
from scipy.ndimage import gaussian_filter1d

file = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/noise0/data_barabasi/identifiers_barabasi.txt"
num_lines = sum(1 for line in open(file))
output_folder = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/5_results/spreading_visualization/noise0/networks/barabasi/"



with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()
        identifier = str.split(line, "!")[0]
        print(f"+++++identifier is {identifier}+++++++")
        DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/noise0/data_barabasi/data_barabasi/" + identifier  
        INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
        inf_df = pd.read_csv(INFECTION_FILE)
        inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
        fig, ax = plt.subplots()
        ax.set_xlabel('Time step')
        ax.set_ylabel('Number of infected nodes')   
        ax.set_title(f'{identifier}', fontsize=7) 
        ax.legend(["infections cumulative", "infections"])
        #for df in inf_df:
        count = inf_df.groupby(['timestep']).size()
        #print(inf_df)
        count_cum = count.cumsum()
            #fig, ax = plt.subplots()
        ax.plot(count_cum, c = "black", label = "cumulative infections")
        ax.hist(inf_df['timestep'].dropna().values, bins=25, label = "infections")
        fig.savefig(os.path.join(output_folder, identifier + ".png"))
        ax.legend()
        plt.clf()
        plt.close()

with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()
        identifier = str.split(line, "!")[0]
        print(f"+++++identifier is {identifier}+++++++")
        DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/noise0/data_barabasi/data_barabasi/"  + identifier  
        INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
        inf_df = pd.read_csv(INFECTION_FILE)
        inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
        fig, ax = plt.subplots()
        ax.set_xlabel('Time step')
        ax.set_ylabel('Number of infected nodes')   
        ax.set_title(f'{identifier}', fontsize=7) 
        count = inf_df.groupby(['timestep']).size()
        count = pd.DataFrame(count)
        y_smoothed = gaussian_filter1d(count, sigma=5)
        ax.plot(y_smoothed, label = "infections")
        fig.savefig(os.path.join(output_folder, "infections" + identifier + ".png"))
        ax.legend()
        plt.clf()
        plt.close()



method = str.split(identifier, "_")[0]
threshold = str.split(identifier, "_")[8]
infprobindiv = str.split(identifier, "_")[8]