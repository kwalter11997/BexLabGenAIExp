# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:59:34 2024

@author: bexlab
"""
import json
import getpass
import pandas as pd
import statistics
import numpy as np
import scipy.stats as stats

user = getpass.getuser()

#subjs = ['BP','Claire','JM2','KW','MK','PB','SN','SS','ncr']
subjs = ['bb']

clutterHigh_rt = []
clutterLow_rt = []
targetPresent_rt = []
targetAbsent_rt = []

clutterHigh_fix = []
clutterLow_fix = []
targetPresent_fix = []
targetAbsent_fix = []

all_subjects_data = []

for s in subjs:
    
    file_path = f'C:\\Users\\{user}\\Dropbox\\Kerri_Walter\\BexLabGenAI\\{s}_gaze_data.json'
   # Open gaze file
    with open(file_path, 'r') as json_file:
        gaze_data = json.load(json_file)
    
    file_path = f'C:\\Users\\{user}\\Dropbox\\Kerri_Walter\\BexLabGenAI\\{s}_data.xlsx'
    # Open data file
    data = pd.read_excel(file_path)
    target_present = data['Target Present']
    
    file_path = f'C:\\Users\\{user}\\Dropbox\\Kerri_Walter\\BexLabGenAI\\{s}_prompt_info.xlsx'
    # Open prompt info file
    prompt_info = pd.read_excel(file_path)
    clutter = np.repeat(prompt_info['Clutter'].values, 4)
    
    ### Reaction Time ###
    
    #Clutter
    clutterHigh_rt_subj = data[clutter == 'High']['Reaction Time']
    clutterLow_rt_subj = data[clutter == 'Low']['Reaction Time']
    
    clutterHigh_rt.append(statistics.mean(clutterHigh_rt_subj))
    clutterLow_rt.append(statistics.mean(clutterLow_rt_subj))
    
    #Target Present/Absent
    targetPresent_rt_subj = data[target_present == 'y']['Reaction Time']
    targetAbsent_rt_subj = data[target_present == 'n']['Reaction Time']
    
    targetPresent_rt.append(statistics.mean(targetPresent_rt_subj))
    targetAbsent_rt.append(statistics.mean(targetAbsent_rt_subj))

    
   ### Fixations ###
   
    nFix = []
    for f in range(0,len(gaze_data)):
        #size 29=fixStart, 35=gazeEvent, 65=fixEnd
        sizes = [len(element) for element in gaze_data[f]] 
        fixations = sizes.count(29)
        nFix.append(fixations)
     
    #Clutter
    clutterHigh_fix_subj = [nFix[i] for i in range(len(clutter)) if clutter[i] == 'High']
    clutterLow_fix_subj = [nFix[i] for i in range(len(clutter)) if clutter[i] == 'Low']
    
    clutterHigh_fix.append(statistics.mean(clutterHigh_fix_subj))
    clutterLow_fix.append(statistics.mean(clutterLow_fix_subj))
    
    #Target Present/Absent
    targetPresent_fix_subj = [nFix[i] for i in range(len(target_present)) if target_present[i] == 'y']
    targetAbsent_fix_subj = [nFix[i] for i in range(len(target_present)) if target_present[i] == 'n']
    
    targetPresent_fix.append(statistics.mean(targetPresent_fix_subj))
    targetAbsent_fix.append(statistics.mean(targetAbsent_fix_subj))    
    
    
    ### Long Form Data ###
    
    data_long = {"Subject": [s] * len(data),
                "Clutter": clutter,
                "Target": target_present,  
                "RT": data['Reaction Time'],
                "Fixations": nFix                 
        }
    subject_df = pd.DataFrame(data_long)
    
    all_subjects_data.append(subject_df)

# Concatenate all subject DataFrames into a single DataFrame
final_df = pd.concat(all_subjects_data, ignore_index=True)

### STATS ###
from statsmodels.formula.api import mixedlm
import matplotlib.pyplot as plt

# Mixed-effects model for Reaction Time
model_rt = mixedlm("RT ~ Clutter * Target", final_df, groups="Subject")
result_rt = model_rt.fit()
print(result_rt.summary())

# Mixed-effects model for Fixations
model_fix = mixedlm("Fixations ~ Clutter * Target", final_df, groups="Subject")
result_fix = model_fix.fit()
print(result_fix.summary())

### Plot ###

### Reaction Time ###

# Aggregate the data
summary_df = final_df.groupby(['Clutter', 'Target']).agg(
    mean_RT=('RT', 'mean'),
    sem_RT=('RT', 'sem')  # Standard error of the mean
).reset_index()

# Check the aggregated data
print(summary_df)

# Set figure size
plt.figure(figsize=(8, 6))

# Bar positions
x = np.arange(len(summary_df['Clutter'].unique()))
width = 0.35

# Separate data by Target Presence
target_present = summary_df[summary_df['Target'] == 'y']
target_absent = summary_df[summary_df['Target'] == 'n']

# Plot bars with error bars
plt.bar(x - width/2, target_present['mean_RT'], width, yerr=target_present['sem_RT'], label='Target Present', color='skyblue', capsize=5)
plt.bar(x + width/2, target_absent['mean_RT'], width, yerr=target_absent['sem_RT'], label='Target Absent', color='orange', capsize=5)

# Add labels and title
plt.xticks(x, summary_df['Clutter'].unique())
plt.xlabel('Clutter Condition')
plt.ylabel('Mean Reaction Time (ms)')
plt.title('Reaction Time by Clutter and Target Presence')
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

### Fixations ###

# Aggregate the data
summary_df = final_df.groupby(['Clutter', 'Target']).agg(
    mean_Fix=('Fixations', 'mean'),
    sem_Fix=('Fixations', 'sem')  # Standard error of the mean
).reset_index()

# Check the aggregated data
print(summary_df)

# Set figure size
plt.figure(figsize=(8, 6))

# Bar positions
x = np.arange(len(summary_df['Clutter'].unique()))
width = 0.35

# Separate data by Target Presence
target_present = summary_df[summary_df['Target'] == 'y']
target_absent = summary_df[summary_df['Target'] == 'n']

# Plot bars with error bars
plt.bar(x - width/2, target_present['mean_Fix'], width, yerr=target_present['sem_Fix'], label='Target Present', color='skyblue', capsize=5)
plt.bar(x + width/2, target_absent['mean_Fix'], width, yerr=target_absent['sem_Fix'], label='Target Absent', color='orange', capsize=5)

# Add labels and title
plt.xticks(x, summary_df['Clutter'].unique())
plt.xlabel('Clutter Condition')
plt.ylabel('Mean Number of Fixations')
plt.title('Number of Fixations by Clutter and Target Presence')
plt.legend()

# Show plot
plt.tight_layout()
plt.show()
