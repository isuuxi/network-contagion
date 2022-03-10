import os
import json
#load identifier
#get Q values from identifieres
#get metadata from identifiers
#extract infected fraction and noise infections frmo metadata
#merge into one dataframe
Q_DIRECTORY = "C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion\Q_values"
 
file = "C:\Users\isivf\Desktop\Masterarbeit\repos\network-contagion\data\identifiers.txt"
num_lines = sum(1 for line in open(file))

with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()


with open(os.path.join(
            Q_DIRECTORY,
            f'Q_' + identifier + '.json'
        ) as f:
        data = json.load(f)