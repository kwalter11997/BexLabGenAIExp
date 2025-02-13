# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:17:26 2024

@author: Kerri
"""
import random
import os
import argparse
from pandas import DataFrame

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--participant", required=True, help="Participant name")
parser.add_argument("--user", required=True, help="User name")
args = parser.parse_args()

participant = args.participant
user = args.user

# Ensure the output directory exists
output_dir = f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI'
os.makedirs(output_dir, exist_ok=True)

### Lists for prompts ###
places = ['kitchen', 'bathroom', 'bedroom', 'office', 'living room']
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

kitchen_things = ['knife', 'bowl', 'pot', 'kettle']
bathroom_things = ['soap', 'towel', 'toothbrush', 'mirror']
bedroom_things = ['lamp', 'nightstand', 'book', 'pillow']
office_things = ['stapler', 'clock', 'pen', 'calculator']
livingroom_things = ['mug', 'blanket', 'table', 'rug']

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
        place = 'office'
        things = office_things
    elif random_place == 4:
        place = 'livingroom'
        things = livingroom_things

   
    global clutter
    if clutter_shuffle_list[trial-1] == 0:
        prompt_clutter = ''
        clutter = 'Low'
    else:
        prompt_clutter = ' high clutter'
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

### Set up randomization order for participant ###
shuffle_list = [0,0,1,1,2,2,3,3,4,4] #random order
#random.shuffle(shuffle_list)
clutter_shuffle_list = [0,1,0,1,0,1,0,1,0,1] 
#random.shuffle(clutter_shuffle_list)
paired_lists = list(zip(shuffle_list, clutter_shuffle_list)) #pair the lists so always one high clutter and one low clutter of each room
random.shuffle(paired_lists)
shuffle_list, clutter_shuffle_list = zip(*paired_lists) # Unzip the shuffled pairs back into two separate lists
shuffle_list = list(shuffle_list) # Convert back to lists (since zip returns tuples)
clutter_shuffle_list = list(clutter_shuffle_list)

scene = 1

prompt_list = []
place_list =[]
target_list=[]
clutter_list=[]

### Create scenes ###
for trial in list(range(1,11)): #10 trials (5 scenes shown twice, 4 images per prompt, 40 total images)
    
    create_prompt(trial)
    prompt_list.append(prompt)
    

    place_list.append(place)
    target_list.append(targets)
    clutter_list.append(clutter)
      
### save data to file ###    
df = DataFrame({'Scene': place_list, 
                'Target': target_list, 
                'Clutter': clutter_list})
df.to_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/{participant}_prompt_info.xlsx', sheet_name='sheet1', index=False)
  
df = DataFrame(prompt_list, columns=['Prompt'])
df.to_csv(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/{participant}_prompt_list.csv', index=False) 
    
