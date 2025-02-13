# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 15:00:37 2024

@author: Kerri
"""

#### TO AVOID COMPATIBILITY ISSUES USE PYTHON 3.8 AND PSYCHOPY 2022.2.5 ####

#pip install psychopy==2022.2.5
#pip install selenium

import subprocess
import getpass
import os
from psychopy import core, gui, data

# Define the directory where the participant data will be stored
user = getpass.getuser()
directory = fr'C:\Users\{user}\Dropbox\Kerri_Walter\BexLabGenAI'

def get_unique_participant_name(participant_name, directory):
    base_name = participant_name
    c = 1
    # Check if the base_name exists and increment if it does
    while os.path.exists(os.path.join(directory, base_name + (f"{c}" if c > 1 else "") + ".xlsx")):
        c += 1
    # Return the name with the counter appended
    return base_name + (f"{c}" if c > 1 else "")

### Get participant info ###
expName = 'BexLab Gen AI Experiment'
expInfo = {'Participant':''}
#expInfo = {'Participant':'', 'session':'w2020'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False,title=expName)
if dlg.OK == False:
    core.quit()
expInfo['Date'] = data.getDateStr()
# Check if the participant name is empty, and if so, prompt for input
if not expInfo['Participant']:
    core.quit()  # Quit if no participant name is provided
# Ensure participant name is unique
expInfo['Participant'] = get_unique_participant_name(expInfo['Participant'], directory)
os.makedirs(f'C:/Users/{user}/Dropbox/Kerri_Walter/generativeAI/{expInfo["Participant"]}') #create a folder for this participants images
participant = expInfo['Participant']

### Run prompt generator ###
generate_prompts = subprocess.Popen(["python", f"C:\\Users\{user}\\Dropbox\\Kerri_Walter\\promptGenerator.py", "--participant", participant, "--user", user], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
generate_prompts.wait()

### Run experiment and image generation scripts concurrently ###
generate_images = subprocess.Popen(["python", f"C:\\Users\{user}\\Dropbox\\Kerri_Walter\\imageGenerator.py", "--participant", participant, "--user", user], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
run_experiment = subprocess.Popen(["python", f"C:\\Users\{user}\\Dropbox\\Kerri_Walter\\runExperiment.py", "--participant", participant, "--user", user], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for both processes to finish
generate_images.wait()
run_experiment.wait()


#out, err = generate_prompts.communicate()

