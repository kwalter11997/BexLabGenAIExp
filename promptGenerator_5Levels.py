# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:58:59 2025

@author: Kerri
"""

import random
import os
import argparse
import pandas as pd
from pandas import DataFrame

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--participant", required=True, help="Participant name")
parser.add_argument("--user", required=True, help="User name")
args = parser.parse_args()

participant = args.participant
user = args.user

# Ensure the output directory exists
output_dir = f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels'
os.makedirs(output_dir, exist_ok=True)

### Lists for prompts ###
places = ['kitchen', 'bathroom', 'bedroom', 'laundry room', 'garage']
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

kitchen_things = ['spatula', 'bowl', 'pot', 'kettle']
bathroom_things = ['soap', 'towel', 'toothbrush', 'robe']
bedroom_things = ['lamp', 'nightstand', 'blanket', 'pillow']
#office_things = ['stapler', 'clock', 'pen', 'calculator']
laundry_things = ['detergent', 'hanger', 'ironing board', 'laundry basket']
garage_things = ['hose', 'ladder', 'toolbox', 'watering can']

def create_prompt(trial):
    random_place = shuffle_list[trial-1]
    global place
    if random_place == 0:
        place = 'kitchen'
        things = kitchen_things
    elif random_place == 1:
        place = 'bathroom'
        things = bathroom_things
    elif random_place == 2:
        place = 'bedroom'
        things = bedroom_things
    elif random_place == 3:
        place = 'laundryroom'
        things = laundry_things
    elif random_place == 4:
        place = 'garage'
        things = garage_things

   
    global clutter
    if clutter_shuffle_list[trial-1] == 0:
        prompt_clutter = ' minimalist'
        clutter = 'Low'
    elif clutter_shuffle_list[trial-1] == 1:
        prompt_clutter = ' simple'
        clutter = 'MediumLow'
    elif clutter_shuffle_list[trial-1] == 2:
        prompt_clutter = ''
        clutter = 'Medium'
    elif clutter_shuffle_list[trial-1] == 3:
        prompt_clutter = ' busy'
        clutter = 'MediumHigh'
    elif clutter_shuffle_list[trial-1] == 4:
        prompt_clutter = ' heavily cluttered'
        clutter = 'High'
        
    random_things = random.sample(range(len(things)), 4) #random things (no duplicates)
    random_colors = random.sample(range(len(colors)), 4) #random colors (no duplicates)

    global prompt
    prompt = f'a photorealistic{prompt_clutter} {places[random_place]} with {colors[random_colors[0]]} {things[random_things[0]]}, {colors[random_colors[1]]} {things[random_things[1]]}, {colors[random_colors[2]]} {things[random_things[2]]}, and {colors[random_colors[3]]} {things[random_things[3]]}'

    global targets
    targets = {
        1: f"{colors[random_colors[0]]} {things[random_things[0]]}",
        2: f"{colors[random_colors[1]]} {things[random_things[1]]}",
        3: f"{colors[random_colors[2]]} {things[random_things[2]]}",
        4: f"{colors[random_colors[3]]} {things[random_things[3]]}"
        }
    
def create_incongruent_prompt(trial):
    random_place = shuffle_list[trial-1]
    global incongruent_place
    if random_place == 0:
        incongruent_place = 'kitchen'
    elif random_place == 1:
        incongruent_place = 'bathroom'
    elif random_place == 2:
        incongruent_place = 'bedroom'
    elif random_place == 3:
        incongruent_place = 'laundryroom'
    elif random_place == 4:
        incongruent_place = 'livingroom'

    random_things = incon_shuffle_list[trial-1]
    if random_things == 0:
        things = kitchen_things
    elif random_things == 1:
        things = bathroom_things
    elif random_things == 2:
        things = bedroom_things
    elif random_things == 3:
        things = laundry_things
    elif random_things == 4:
        things = garage_things
        
    random_things = random.sample(range(len(things)), 4) #random things (no duplicates)
    random_colors = random.sample(range(len(colors)), 4) #random colors (no duplicates)

    global incongruent_prompt
    incongruent_prompt = f'a photorealistic heavily cluttered {places[random_place]} with {colors[random_colors[0]]} {things[random_things[0]]}, {colors[random_colors[1]]} {things[random_things[1]]}, {colors[random_colors[2]]} {things[random_things[2]]}, and {colors[random_colors[3]]} {things[random_things[3]]}'

    global incongruent_targets
    incongruent_targets = {
        1: f"{colors[random_colors[0]]} {things[random_things[0]]}",
        2: f"{colors[random_colors[1]]} {things[random_things[1]]}",
        3: f"{colors[random_colors[2]]} {things[random_things[2]]}",
        4: f"{colors[random_colors[3]]} {things[random_things[3]]}"
        }
    
def shuffle_lists_no_match(list1, list2):
    while True:
        # Shuffle both lists
        random.shuffle(list1)
        random.shuffle(list2)
        
        # Check if there are any matching values at the same index
        if all(a != b for a, b in zip(list1, list2)):
            return list1, list2
        
### Set up randomization order for participant ###
shuffle_list = [0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4] #random order
#random.shuffle(shuffle_list)
clutter_shuffle_list = [0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4] 
#random.shuffle(clutter_shuffle_list)
paired_lists = list(zip(shuffle_list, clutter_shuffle_list)) #pair the lists so always one clutter condition for each room
random.shuffle(paired_lists)
shuffle_list, clutter_shuffle_list = zip(*paired_lists) # Unzip the shuffled pairs back into two separate lists
shuffle_list = list(shuffle_list) # Convert back to lists (since zip returns tuples)
clutter_shuffle_list = list(clutter_shuffle_list)

# scene = 1

prompt_list = []
place_list =[]
target_list=[]
clutter_list=[]
congruency_list=[]
incongruent_prompt_list = []
incongruent_place_list = []
incongruent_target_list = []
incongruent_clutter_list = []
incongruent_congruency_list = []

### Create scenes ###
for trial in list(range(1,26)): #25 trials (5 scenes shown 5 times, 4 images per prompt, 100 total images)
    
    create_prompt(trial)
    prompt_list.append(prompt)
    

    place_list.append(place)
    target_list.append(targets)
    clutter_list.append(clutter)
    congruency_list.append('Congruent')


### Create incongruent scenes ###
shuffle_list = [0,1,2,3,4] 
incon_shuffle_list = [0,1,2,3,4]
random.shuffle(shuffle_list)

# Shuffle the lists such that no value is in the same position in both lists
shuffle_list, incon_shuffle_list = shuffle_lists_no_match(shuffle_list, incon_shuffle_list)

for trial in list(range(1,6)): #5 trials (5 scenes shown 1 time, 4 images per prompt, 20 total images)
    
    create_incongruent_prompt(trial)
    incongruent_prompt_list.append(incongruent_prompt)
    
    incongruent_place_list.append(incongruent_place)
    incongruent_target_list.append(incongruent_targets)
    incongruent_clutter_list.append('High')
    incongruent_congruency_list.append('Incongruent') 
    
    
### Create congruent dataframe ###
con_df = DataFrame({'Scene': place_list, 
                'Target': target_list, 
                'Clutter': clutter_list,
                'Congruency': congruency_list})    

### Create incongruent dataframe ###
incon_df = DataFrame({'Scene': incongruent_place_list, 
                'Target': incongruent_target_list, 
                'Clutter': incongruent_clutter_list,
                'Congruency': incongruent_congruency_list})    

    
### randomly insert incongruent trials ###    
# Generate 5 unique random values between 1 and 25 (inclusive)
random_values = random.sample(range(1, 26), 5)
random_values.sort()    

# Insert the rows into df1 at the random indices
df1=con_df
df2=incon_df
for i, idx in enumerate(random_values):
    # Insert row from df2 into df1 at the specified index
    df1 = pd.concat([df1.iloc[:idx + i], df2.iloc[i:i+1], df1.iloc[idx + i:]]).reset_index(drop=True)
    prompt_list.insert(idx + i, incongruent_prompt_list[i])
    
### save data to file ###    
df1.to_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/{participant}_prompt_info.xlsx', sheet_name='sheet1', index=False)
  
df = DataFrame(prompt_list, columns=['Prompt'])
df.to_csv(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/{participant}_prompt_list.csv', index=False) 
    
