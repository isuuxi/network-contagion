
import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle

file = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/data_troubleshooting/identifiers_erdos.txt"
num_lines = sum(1 for line in open(file))
output_folder = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/5_results/spreading_visualization/troubleshooting/erdos/"


with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()
        identifier = str.split(line, "!")[0]
        print(f"+++++identifier is {identifier}+++++++")
        DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/data_troubleshooting/data_erdos/" + identifier  
        #INFECTION_FILE = DATA_DIRECTORY + "surrogates_" + identifier +  ".pickle"
        #inf_df = pd.read_pickle(INFECTION_FILE)
        #print(inf_df)
        INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
        inf_df = pd.read_csv(INFECTION_FILE)
        fig, ax = plt.subplots()
        ax.set_xlabel('Time step')
        ax.set_ylabel('Number of infected nodes')   
        ax.set_title(f'{identifier}', fontsize=7) 
        ax.legend(["infections cumulative", "infections"])
        #for df in inf_df:
        count = inf_df.groupby(['timestep']).size()
        count_cum = count.cumsum()
            #fig, ax = plt.subplots()
        ax.plot(count_cum, c = "black", label = "cumulative infections")
        ax.plot(count, c = "green", label = "infections")
        fig.savefig(os.path.join(output_folder, identifier + ".png"))
        ax.legend()
        plt.clf()
        plt.close()

        
