
import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np
from scipy.ndimage import gaussian_filter1d

file = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/noise0/data_watts/identifiers_watts.txt"
num_lines = sum(1 for line in open(file))
output_folder = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/5_results/spreading_visualization/noise0/networks/watts/"

df_th05 = pd.DataFrame(0, [1], columns=['col'])
df_th1 = pd.DataFrame()
df_th15 = pd.DataFrame()
added_th05 = 0
added_th1 = 0
added_th15 = 0
myarray_th05 = np.zeros(1600)
myarray_th1 = np.zeros(1600)
myarray_th15 = np.zeros(1600)

na_sum_th05 = []
print(type(na_sum_th05))
na_sum_th1 = []
na_sum_th15 = []


df_SI05 = pd.DataFrame(np.nan, index=range(5000), columns=['observations'])
df_SI1 = pd.DataFrame(np.nan, index=range(5000), columns=['observations'])
df_SI15 = pd.DataFrame(np.nan, index=range(5000), columns=['observations'])

count_th05 = 0
count_th1 = 0
count_th15 = 0

'''''
with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()
        identifier = str.split(line, "!")[0]
        #print(f"+++++identifier is {identifier}+++++++")
        method = str.split(identifier, "_")[0]
        #print(method)
        if method == "generalized":
            DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/noise0/data_watts/data_watts/" + identifier  
            x = str.split(identifier, "_")
            threshold = str.split(x[8], "d")[1]
            #print(threshold)
            if threshold == "0.5":
                print("++++++++++threshold 0.5++++++++++")
                INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
                inf_df = pd.read_csv(INFECTION_FILE)
                print(type(na_sum_th05))
                na_sum_th05.append(inf_df['timestep'].isna().sum())
                inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
                count = np.squeeze(np.asarray(inf_df))
                myarray_th05 = np.column_stack((myarray_th05, count))
                count_th05 = count_th05 +1
            elif threshold == "1":
                print("++++++++++threshold 1.0++++++++++")
                INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
                inf_df = pd.read_csv(INFECTION_FILE)
                na_sum_th1.append(inf_df['timestep'].isna().sum())
                inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
                count = np.squeeze(np.asarray(inf_df))
                myarray_th1 = np.column_stack((myarray_th1, count))     
                count_th1 = count_th1 +1     
            elif threshold == "1.5":
                print("++++++++++threshold 1.5++++++++++")
                INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
                inf_df = pd.read_csv(INFECTION_FILE)
                na_sum_th15.append(inf_df['timestep'].isna().sum())
                inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
                print(f"inf data frame is without na {inf_df.dropna()}")
                count = np.squeeze(np.asarray(inf_df))
                print(f"inf_df as numpy has shape {count.shape}")
                myarray_th15 = np.column_stack((myarray_th15, count)) 
                count_th15 = count_th15 +1
                print(f"my array is {myarray_th15}")      


print(f"na_sum_th05 is {na_sum_th05}")
print(f"na_sum_th1 is {na_sum_th1}")
print(f"na_sum_th15 is {na_sum_th15}")

print(f"count_th05 is {count_th05}")
print(f"count_th1 is {count_th1}")
print(f"count_th15 is {count_th15}")


average_th05 = np.nansum(myarray_th05, axis = 1)/(myarray_th05.shape[1]-1)
average_th05 = np.round_(average_th05)
average_th05 = pd.DataFrame(average_th05)
averageth05_grouped = average_th05.groupby(by=[0]).size()
#print(f"threshold 0.5 is {averageth05_grouped}")

average_th1 = np.nansum(myarray_th1, axis = 1)/(myarray_th1.shape[1]-1)
average_th1 = np.round_(average_th1)
#print(f"np average for 1 is {average_th1}")
average_th1 = pd.DataFrame(average_th1)
#print(f"pandas average for 1 is {average_th1}")
averageth1_grouped = average_th1.groupby(by=[0]).size()
#print(f"threshold 1 is {averageth1_grouped}")


average_th15 = (np.nansum(myarray_th15, axis = 1)/(myarray_th15.shape[1]-1))
average_th15 = np.round_(average_th15)
print(f"np average for 1.5 is {average_th15}")
average_th15 = pd.DataFrame(average_th15)
print(f"pandas array for 1.5 is {average_th15}")
averageth15_grouped = average_th15.groupby(by=[0]).size()
print(f"threshold 1.5 is {averageth15_grouped}")


fig, ax = plt.subplots()
ax.set_xlabel('Time step')
ax.set_ylabel('Number of infected nodes')   
ax.set_title(f'{identifier}', fontsize=7) 
ax.legend(["infections cumulative", "infections"])           

#y_smoothed = gaussian_filter1d(count, sigma=5)
ax.hist(average_th05, label = "infections", bins = 50, color ="blue", alpha = 0.4)
ax.hist(average_th1, label = "infections", bins = 50, color ="red", alpha = 0.4)
ax.hist(average_th15, label = "infections", bins = 50, color ="green", alpha = 0.4)


#ax.plot(y_smoothed, label = "infections")

#fig.savefig(os.path.join(output_folder, "infections" + identifier + ".png"))
ax.legend()
plt.show()
plt.clf()
plt.close()

fig, ax = plt.subplots()
ax.set_xlabel('Time step')
ax.set_ylabel('Number of infected nodes')   
ax.set_title(f'{identifier}', fontsize=7) 
ax.legend(["infections cumulative", "infections"])           

#y_smoothed = gaussian_filter1d(count, sigma=5)
ax.plot(averageth05_grouped, c = "green", label = "infections")
ax.plot(averageth1_grouped, c = "black", label = "infections")
ax.plot(averageth15_grouped, c = "red", label = "infections")
#ax.plot(y_smoothed, label = "infections")

#fig.savefig(os.path.join(output_folder, "infections" + identifier + ".png"))
ax.legend()
plt.show()
plt.clf()
plt.close()
#print(count)
'''''
    
with open(file) as fp:
    for cnt in range(0, num_lines):
        line = fp.readline()
        identifier = str.split(line, "!")[0]
        #print(f"+++++identifier is {identifier}+++++++")
        method = str.split(identifier, "_")[0]
        if method == "SI":
            DATA_DIRECTORY = "C:/Users/isivf/Desktop/Masterarbeit/repos/network-contagion/data/noise0/data_watts/data_watts/" + identifier
            x = str.split(identifier, "_")
            infprobindiv = str.split(x[8], "v")[1]
            print(infprobindiv)
            if infprobindiv == "0.02":
                print("++++++++++threshold 0.5++++++++++")
                INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
                inf_df = pd.read_csv(INFECTION_FILE)
                print(type(na_sum_th05))
                na_sum_th05.append(inf_df['timestep'].isna().sum())
                inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
                count = np.squeeze(np.asarray(inf_df))
                myarray_th05 = np.column_stack((myarray_th05, count))
                count_th05 = count_th05 +1
            elif infprobindiv == "0.04":
                print("++++++++++threshold 1.0++++++++++")
                INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
                inf_df = pd.read_csv(INFECTION_FILE)
                na_sum_th1.append(inf_df['timestep'].isna().sum())
                inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
                count = np.squeeze(np.asarray(inf_df))
                myarray_th1 = np.column_stack((myarray_th1, count))     
                count_th1 = count_th1 +1     
            elif infprobindiv == "0.08":
                print("++++++++++threshold 1.5++++++++++")
                INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
                inf_df = pd.read_csv(INFECTION_FILE)
                na_sum_th15.append(inf_df['timestep'].isna().sum())
                inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
                print(f"inf data frame is without na {inf_df.dropna()}")
                count = np.squeeze(np.asarray(inf_df))
                print(f"inf_df as numpy has shape {count.shape}")
                myarray_th15 = np.column_stack((myarray_th15, count)) 
                count_th15 = count_th15 +1
                print(f"my array is {myarray_th15}")      



preunique_05 = np.delete(myarray_th05, 0 , 1) 
print(f"######size is {preunique_05.shape}preuniques is {preunique_05} and NAs are {np.count_nonzero(np.isnan(preunique_05))} ###########")
uniques05, uniques_counts05 = np.unique(preunique_05, return_counts=True)
uniques_counts05 = uniques_counts05/count_th05
print(f"######uniques05 is {uniques05} and their counts are {uniques_counts05}###########")

preunique1 = np.delete(myarray_th1, 0 , 1) 
print(f"######size is {preunique1.shape}preuniques is {preunique1} and NAs are {np.count_nonzero(np.isnan(preunique1))} ###########")
uniques1, uniques_counts1 = np.unique(preunique1, return_counts=True)
uniques_counts1 = uniques_counts1/count_th1
print(f"######uniques1 is {uniques1} and their counts are {uniques_counts1}###########")

preunique15 = np.delete(myarray_th15, 0 , 1) 
print(f"######size is {preunique15.shape}preuniques is {preunique15} and NAs are {np.count_nonzero(np.isnan(preunique15))} ###########")
uniques15, uniques_counts15 = np.unique(preunique15, return_counts=True)
uniques_counts15 = uniques_counts15/count_th15
print(f"######uniques15 is {uniques15} and their counts are {uniques_counts15}###########")

fig, ax = plt.subplots()
ax.plot(uniques05, uniques_counts05, c = "green", label = "Threshold = 0.5")
ax.plot(uniques1, uniques_counts1, c = "blue", label = "Threshold = 1")
ax.plot(uniques15, uniques_counts15, c = "red", label = "Threshold = 1.5")
ax.set_xlabel('Time step')
ax.set_ylabel('Average number of infected nodes')   
ax.set_title("Average number of infected nodes per time step", fontsize=11) 
ax.legend()
plt.show()
plt.close()



print(f"na_sum_th05 is {na_sum_th05}")
print(f"na_sum_th1 is {na_sum_th1}")
print(f"na_sum_th15 is {na_sum_th15}")

print(f"count_th05 is {count_th05}")
print(f"count_th1 is {count_th1}")
print(f"count_th15 is {count_th15}")


average_th05 = np.nansum(myarray_th05, axis = 1)/(myarray_th05.shape[1]-1)
average_th05 = np.round_(average_th05)
average_th05 = pd.DataFrame(average_th05)
averageth05_grouped = average_th05.groupby(by=[0]).size()
#print(f"threshold 0.5 is {averageth05_grouped}")

average_th1 = np.nansum(myarray_th1, axis = 1)/(myarray_th1.shape[1]-1)
average_th1 = np.round_(average_th1)
#print(f"np average for 1 is {average_th1}")
average_th1 = pd.DataFrame(average_th1)
#print(f"pandas average for 1 is {average_th1}")
averageth1_grouped = average_th1.groupby(by=[0]).size()
#print(f"threshold 1 is {averageth1_grouped}")


average_th15 = (np.nansum(myarray_th15, axis = 1)/(myarray_th15.shape[1]-1))
average_th15 = np.round_(average_th15)
print(f"np average for 1.5 is {average_th15}")
average_th15 = pd.DataFrame(average_th15)
print(f"pandas array for 1.5 is {average_th15}")
averageth15_grouped = average_th15.groupby(by=[0]).size()
print(f"threshold 1.5 is {averageth15_grouped}")


fig, ax = plt.subplots()
ax.set_xlabel('Time step')
ax.set_ylabel('Number of infected nodes')   
ax.set_title(f'{identifier}', fontsize=7) 
ax.legend(["infections cumulative", "infections"])           

#y_smoothed = gaussian_filter1d(count, sigma=5)
ax.hist(average_th05, label = "infections", bins = 50, color ="blue", alpha = 0.4)
ax.hist(average_th1, label = "infections", bins = 50, color ="red", alpha = 0.4)
ax.hist(average_th15, label = "infections", bins = 50, color ="green", alpha = 0.4)


#ax.plot(y_smoothed, label = "infections")

#fig.savefig(os.path.join(output_folder, "infections" + identifier + ".png"))
ax.legend()
plt.show()
plt.clf()
plt.close()

fig, ax = plt.subplots()
ax.set_xlabel('Time step')
ax.set_ylabel('Number of infected nodes')   
ax.set_title(f'{identifier}', fontsize=7) 
ax.legend(["infections cumulative", "infections"])           

#y_smoothed = gaussian_filter1d(count, sigma=5)
ax.plot(averageth05_grouped, c = "green", label = "infections")
ax.plot(averageth1_grouped, c = "black", label = "infections")
ax.plot(averageth15_grouped, c = "red", label = "infections")
#ax.plot(y_smoothed, label = "infections")

#fig.savefig(os.path.join(output_folder, "infections" + identifier + ".png"))
ax.legend()
plt.show()
plt.clf()
plt.close()
#print(count)         




'''''

                inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
    count = inf_df.groupby(['timestep']).size()
    count = np.asarray(count)
elif threshold == "1":
    INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
    print(f"+++++++++++inf df is {inf_df}")
    count = inf_df.groupby(['timestep']).size()
    count = pd.DataFrame(count)
    df_th1 = pd.concat([count, df_th1], axis=0)
    added_th1 = added_th1 + 1
elif threshold == "1.5":
    INFECTION_FILE = DATA_DIRECTORY + "/spreading_" + identifier + ".csv"
    inf_df = pd.read_csv(INFECTION_FILE)
    inf_df['timestep'] = inf_df['timestep'].replace(to_replace= 0, value= float("NaN"))
    count = inf_df.groupby(['timestep']).size()
    count = pd.DataFrame(count)
    df_th15 = pd.concat([count, df_th15], axis=0)
    added_th15 = added_th15 + 1
df_th05 = df_th05.dropna()
df_th1 = df_th1.dropna()
df_th15 = df_th15.dropna()
print(df_th05)
print(df_th1)
print(df_th15)
           
            fig, ax = plt.subplots()
            ax.set_xlabel('Time step')
            ax.set_ylabel('Number of infected nodes')   
            ax.set_title(f'{identifier}', fontsize=7) 
            ax.legend(["infections cumulative", "infections"])           
            
            y_smoothed = gaussian_filter1d(count, sigma=5)
            ax.plot(y_smoothed, label = "infections")
            ax.plot(y_smoothed, label = "infections")

            fig.savefig(os.path.join(output_folder, "infections" + identifier + ".png"))
            ax.legend()
            plt.clf()
            plt.close()

        elif method == "SI":
            x = str.split(identifier, "_")
            infprobindiv = str.split(x[8], "v")
            
'''