from genericpath import exists
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#load identifier
#get Q values from identifieres
#get metadata from identifiers
#extract infected fraction and noise infections frmo metadata
#merge into one dataframe
#Q_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/Q_values"
 
file = 'C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/identifiers_erdos.txt'
num_lines = sum(1 for line in open(file))
mylist = []

#df = pd.DataFrame(columns = ['nodes', 'contagion_inf', 'noise_inf', 'Q'])
#print(df)

###### read data #######
'''''
create df with columns nodes, contagion_inf, noise_inf, initial_inf, Q, identifier
'''
with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()
        identifier = str.split(line, "!")[0] 
        mypath = os.path.join("C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/5_results/surrogate_results_erdos_bins20_maxdose0.5_halftime/Q_values", identifier, "Q_"+ identifier + ".txt"
            )
        if exists(mypath):
            #print(mypath)
            with open(mypath
            ) as f:
                Q = f.read()
            metadata = pd.read_csv(os.path.join(
                "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos", identifier, "infectiondata_" + identifier + ".csv"
                )
            )
            metadata['Q'] = Q
            metadata['identifier'] = identifier
            metadata['method'] = str.split(identifier, "_")[0]

            mylist.append(metadata)
        
print(mylist)
df = pd.concat(mylist, ignore_index= False)
df["method_codes"] = pd.Categorical(df["method"]).codes
output_file = "C:/Users/isivf/Desktop/df.csv"
df.to_csv(output_file,index=False)
print(df.info())
print(df)
df['Q'] = df['Q'].astype("float")
######## subset df #######
#by network size
df_n500 = df[df["nodes"] == 500]
#print(f"df_n500 is {df_n500}")
df_n1000 = df[df["nodes"] == 1000]
#print(f"df_n1000 is {df_n1000}")

#by contagion method
df_n500_SI = df_n500[df_n500["method_codes"] == 0]
print(f"##### filtered dataframe is {df_n500_SI.shape, df_n500_SI}")
df_n500_generalized = df_n500[df_n500["method_codes"] == 1]
df_n1000_SI = df_n1000[df_n1000["method_codes"] == 0]
df_n1000_generalized = df_n1000[df_n1000["method_codes"] == 1]

###### assign values #####
signaltonoise = df['contagion_inf']/df['noise_inf']
inffraction = (df['contagion_inf']+df['noise_inf'])/df['nodes']
absoluteinf = df['contagion_inf']+df['noise_inf']

##### create subset for unsuccessful detections #####
df_highQ = df[df['Q'] >= 0.05]    
signaltonoise_high = df_highQ['contagion_inf']/df_highQ['noise_inf']
inffraction_high = (df_highQ['contagion_inf']+df_highQ['noise_inf'])/df_highQ['nodes']
absoluteinf_high = df_highQ['contagion_inf']+df_highQ['noise_inf']

df_highQ_n500 = df_n500[df_n500['Q'] >= 0.05]
signaltonoise_high_n500 = df_highQ_n500['contagion_inf']/df_highQ_n500['noise_inf']
inffraction_high_n500 = (df_highQ_n500['contagion_inf']+df_highQ_n500['noise_inf'])/df_highQ_n500['nodes']
absoluteinf_high_n500 = df_highQ_n500['contagion_inf']+df_highQ_n500['noise_inf']

df_highQ_n500_SI = df_n500_SI[df_n500_SI['Q'] >= 0.05]

df_highQ_n500_generalized = df_n500_generalized[df_n500_generalized['Q'] >= 0.05]

df_highQ_n1000 = df_n1000[df_n1000['Q'] >= 0.05]   
signaltonoise_high_n1000 = df_highQ_n1000['contagion_inf']/df_highQ_n1000['noise_inf']
inffraction_high_n1000 = (df_highQ_n1000['contagion_inf']+df_highQ_n1000['noise_inf'])/df_highQ_n1000['nodes']
absoluteinf_high_n1000 = df_highQ_n1000['contagion_inf']+df_highQ_n1000['noise_inf']

df_highQ_n1000_SI = df_n1000_SI[df_n1000_SI['Q'] >= 0.05]

df_highQ_n1000_generalized = df_n1000_generalized[df_n1000_generalized['Q'] >= 0.05]

df_lowQ_n500_SI = df_n500_SI[df_n500_SI['Q'] < 0.05]

df_lowQ_n500_generalized = df_n500_generalized[df_n500_generalized['Q'] < 0.05]

df_lowQ_n1000_SI = df_n1000_SI[df_n1000_SI['Q'] < 0.05]

df_lowQ_n1000_generalized = df_n1000_generalized[df_n1000_generalized['Q'] < 0.05]

###### create first scatter plot #######
print(f"Q ist {df['Q']}")
plt.scatter(signaltonoise, inffraction, c= df['Q'], cmap = 'viridis', s = 40, alpha = 0.7)
cbar = plt.colorbar(label = 'Q value')
plt.scatter(signaltonoise_high, inffraction_high, marker = '|', c = 'darkorange', alpha = 0.7)
plt.xlabel("signal to noise")
plt.xlim(-0.01, 1)
plt.ylabel("infected fraction")
plt.title("Erdős-Rényi model")
plt.show()
###### create second scatter plot #######
plt.scatter(signaltonoise, absoluteinf, c= df['Q'], cmap = 'viridis', alpha = 0.7)
cbar = plt.colorbar(label = 'Q value')
plt.scatter(signaltonoise_high, absoluteinf_high, marker = '|', c = 'darkorange', alpha = 0.7)
plt.xlabel("signal to noise")
plt.xlim(-0.01, 1)
plt.ylabel("Number of infections")
plt.title("Erdős-Rényi model")
plt.show()
###### get infection process data #####
DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
print(INFECTION_FILE)
inf_df = pd.read_csv(INFECTION_FILE)


plt.figure(1, figsize=(5, 20))
ax = plt.subplot(211)
for idx, row in df_highQ_n500_SI.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "blue", alpha = 0.2)
for idx, row in df_highQ_n500_generalized.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "red", alpha = 0.2)
plt.xlim(0, 50)
plt.ylim(0, 500)
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')   
plt.title('Unsuccessful detections, n = 500') 
ax.legend(['Red: Generalized contagion', 'Blue: SI contagion'])
plt.subplot(212)
for idx, row in df_highQ_n1000_SI.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "blue", alpha = 0.2)
for idx, row in df_highQ_n1000_generalized.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "red", alpha = 0.2)
plt.xlim(0, 50)
plt.ylim(0, 1000)
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')   
plt.title('Unsuccessful detections, n = 1000') 
ax.legend(['Blue: SI contagion', 'Red: Generalized contagion'])
plt.show()

plt.figure(1, figsize=(5, 20))
plt.subplot(211)
for idx, row in df_lowQ_n500_SI.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "blue", alpha = 0.2)
for idx, row in df_lowQ_n500_generalized.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "red", alpha = 0.2)
plt.xlim(0, 50)
plt.ylim(0, 500)
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')   
plt.title('Successful detections, n = 500') 
plt.subplot(212)
for idx, row in df_lowQ_n1000_SI.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "blue", alpha = 0.2)
for idx, row in df_lowQ_n1000_generalized.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "red", alpha = 0.2)
plt.xlim(0, 50)
plt.ylim(0, 1000)
ax.legend(['Blue: SI contagion', 'Red: Generalized contagion'])
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')   
plt.title('Successful detections, n = 1000') 
plt.show()



###### create infection timeline plot with unsuccessful detection
for idx, row in df_highQ.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "black", alpha = 0.2)
plt.xlim(0, 50)
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')   
plt.title('Simulated infection processes with Q >= 0.05') 
plt.show()
###### create infection timeline plot with successful detection
df_lowQ = df[df['Q'] < 0.05]


for idx, row in df_lowQ.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data_erdos/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    plt.plot(count, c = "black", alpha = 0.1)
plt.xlim(0, 50)    
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')
plt.title('Simulated infection processes with Q < 0.05')
plt.show()
