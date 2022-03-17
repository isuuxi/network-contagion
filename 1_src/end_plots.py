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
 
file = 'C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/identifiers.txt'
num_lines = sum(1 for line in open(file))
mylist = []

#df = pd.DataFrame(columns = ['nodes', 'contagion_inf', 'noise_inf', 'Q'])
#print(df)

with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()
        identifier = str.split(line, "!")[0] 
        mypath = os.path.join("C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/5_results/surrogate_results/Q_values", identifier, "Q_"+ identifier + ".txt"
            )
        if exists(mypath):
            #print(mypath)
            with open(mypath
            ) as f:
                Q = f.read()
            metadata = pd.read_csv(os.path.join(
                "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data", identifier, "infectiondata_" + identifier + ".csv"
                )
            )
            metadata['Q'] = Q
            metadata['identifier'] = identifier
            mylist.append(metadata)
        
print(mylist)
df = pd.concat(mylist, ignore_index= False)
print(df.info())
print(df)
'''''
n, bins, patches = plt.hist(df['Q'], 10, density=1, facecolor='g', alpha=0.75)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
plt.grid(True)
#plt.show()
'''

#df['Q'].hist(bins = 10)
#plt.show()
signaltonoise = df['noise_inf']/df['contagion_inf']
print(f"signaltonoise is {signaltonoise}")
inffraction = (df['contagion_inf']+df['noise_inf'])/df['nodes']
print(f" inffraction is {inffraction}")
absoluteinf = df['contagion_inf']+df['noise_inf']
#plt.hist2d(signaltonoise, df['Q'], bins=(10, 50), cmap=plt.cm.jet)
#plt.show()

#signal to noise ratio
#infected fraction (Systemgrößeparameter)
#total number infected zu signal to noise ratio 
#2D Scatterplot mit Punkten, die Farbe entsprechend der Q Werte

df['Q'] = df['Q'].astype("float")
df_highQ = df[df['Q'] >= 0.05]    
signaltonoise_high = df_highQ['noise_inf']/df_highQ['contagion_inf']
inffraction_high = (df_highQ['contagion_inf']+df_highQ['noise_inf'])/df_highQ['nodes']
absoluteinf_high = df_highQ['contagion_inf']+df_highQ['noise_inf']

print(f"Q ist {df['Q']}")
plt.scatter(signaltonoise, inffraction, c= df['Q'], cmap = 'viridis', s = 40, alpha = 0.7)
cbar = plt.colorbar(label = 'Q value')
plt.scatter(signaltonoise_high, inffraction_high, marker = '|', c = 'darkorange', alpha = 0.7)
plt.xlabel("noise over signal")
plt.ylabel("infected fraction")
plt.show()

plt.scatter(signaltonoise, absoluteinf, c= df['Q'], cmap = 'viridis', alpha = 0.7)
cbar = plt.colorbar(label = 'Q value')
plt.scatter(signaltonoise_high, absoluteinf_high, marker = '|', c = 'darkorange', alpha = 0.7)
plt.xlabel("noise over signal")
plt.ylabel("Number of infections")
plt.show()


DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/" 
INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
print(INFECTION_FILE)
inf_df = pd.read_csv(INFECTION_FILE)
print(inf_df, type(inf_df))

for idx, row in df_highQ.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
#print(INFECTION_FILE)
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    #print(count)
    plt.plot(count, c = "black", alpha = 0.2)
plt.xlim(0, 50)
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')   
plt.title('Simulated infection processes with Q >= 0.05') 
plt.show()

df_lowQ = df[df['Q'] < 0.05]
print(f"for Q under threshold is {df_lowQ}")

for idx, row in df_lowQ.iterrows():
    identifier = row['identifier']
    DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/" 
    INFECTION_FILE = DATA_DIRECTORY + identifier + "/" + "spreading_"+ identifier + ".csv"
#print(INFECTION_FILE)
    inf_df = pd.read_csv(INFECTION_FILE)
    count = inf_df.groupby(['timestep']).size()
    count = count.cumsum()
    #print(count)
    plt.plot(count, c = "black", alpha = 0.1)
plt.xlim(0, 50)    
plt.xlabel('Time step')
plt.ylabel('Number of infected nodes')
plt.title('Simulated infection processes with Q < 0.05')
plt.show()

#print(inf_df, type(inf_df))


