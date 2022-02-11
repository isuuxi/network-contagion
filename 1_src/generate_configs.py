import json
import numpy as np
from run_model import *

##parameters to change##
#dose level to control contagion spread: 0.001 to 1 in steps of
#noise: 0 to 0.1 in steps of 
#time to control contagion development: 200 to 1000
#size ? 500, 1000, 1500

DOSES = np.arange(0.1, 1, 0.1)
DOSE_LIMITED = [0.001, 0.1, 0.2, 0.5, 0.7, 1]
NOISES = np.arange(0, 0.05, 0.01)
TIMES = np.arange(200, 1000, 100)
SIZES = [500, 1000, 1500]
EXPERIMENTS = 5
p = 0.01

for sizes in SIZES:
    for times in TIMES:
        for noises in NOISES:
            for doses in DOSE_LIMITED:
                for experiment in range(EXPERIMENTS):
                    run_model(times, sizes, p, noises, doses, experiment)
                





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