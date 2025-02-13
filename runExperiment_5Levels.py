# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 2025

@author: Kerri
"""

import psychopy
import pandas
import os
import argparse
import ast
import time
import json

from psychopy import core, event, visual, gui, data
from pandas import DataFrame
from psychopy.iohub import launchHubServer

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

target_list = pandas.read_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/{participant}_prompt_info.xlsx')
target_list = target_list.Target
 
### Eyetracker Things ###
GazepointSampleEvent_names = ['experiment_id','session_id','device_id','event_id','type',
                              'device_time','logged_time','time','confidence_interval','delay','filter_id',
                              'left_gaze_x','left_gaze_y','left_raw_x','left_raw_y',
                              'left_pupil_measure1','left_pupil_measure1_type','left_pupil_measure2','left_pupil_measure2_type',
                              'right_gaze_x','right_gaze_y','right_raw_x','right_raw_y',
                              'right_pupil_measure1','right_pupil_measure1_type','right_pupil_measure2','right_pupil_measure2_type',
                              'dial','dialv','gsr','gsrv','hr','hrv','hrp','status']

FixationStartEvent_names = ['experiment_id','session_id','device_id','event_id','type',
                            'device_time','logged_time','time','confidence_interval','delay','filter_id','eye',
                            'gaze_x','gaze_y','gaze_z',
                            'angle_x','angle_y',
                            'raw_x','raw_y',
                            'pupil_measure1','pupil_measure1_type','pupil_measure2','pupil_measure2_type',
                            'ppd_x','ppd_y',
                            'velocity_x','velocity_y','velocity_xy',
                            'status']

FixationEndEvent_names = ['experiment_id','session_id','device_id','event_id','type',
                       'device_time','logged_time','time','confidence_interval','delay','filter_id','eye','duration',
                       'start_gaze_x','start_gaze_y','start_gaze_z',
                       'start_angle_x','start_angle_y',
                       'start_raw_x','start_raw_y',
                       'start_pupil_measure1','start_pupil_measure1_type','start_pupil_measure2','start_pupil_measure2_type',
                       'start_ppd_x','start_ppd_y',
                       'start_velocity_x','start_velocity_y','start_velocity_xy',
                       'end_gaze_x','end_gaze_y','end_gaze_z',
                       'end_angle_x','end_angle_y',
                       'end_raw_x','end_raw_y',
                       'end_pupil_measure1','end_pupil_measure1_type','end_pupil_measure2','end_pupil_measure2_type',
                       'end_ppd_x','end_ppd_y',
                       'end_velocity_x','end_velocity_y','end_velocity_xy',
                       'average_gaze_x','average_gaze_y','average_gaze_z',
                       'average_angle_x','average_angle_y',
                       'average_raw_x','average_raw_y',
                       'average_pupil_measure1','average_pupil_measure1_type','average_pupil_measure2','average_pupil_measure2_type',
                       'average_ppd_x','average_ppd_y',
                       'average_velocity_x','average_velocity_y','average_velocity_xy','peak_velocity_x','peak_velocity_y','peak_velocity_xy',
                       'status']
    
# Define the ioHub configuration
iohub_config = {
    "eyetracker.hw.gazepoint.gp3.EyeTracker": {
        "name": "tracker",
        "device_timer": {"interval": 0.005},
        #"monitor_event_types": [ "BinocularEyeSampleEvent", "FixationStartEvent", "FixationEndEvent"]
    }
}

#set up a temporary fullscreen window so the tracker has the correct screen dimensions on setup
tracker_win = visual.Window(
    screen=0,
    units='pix',
    fullscr=True)
tracker_win.close()

# Launch the ioHub server
io = launchHubServer(window=tracker_win, **iohub_config)

# Access the eyetracker instance
tracker = io.devices.tracker

def save_data():
    df = DataFrame({'Reaction Time': reaction_time_list, 
                    'Start Time': start_time_list, 
                    'End Time': end_time_list,
                    'Mouse Position': click_list})
    df.to_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/{participant}_data.xlsx', sheet_name='sheet1', index=False)

    #eyetracker data
    with open(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/{participant}_gaze_data.json', 'w') as f:
        json.dump(event_list, f)   
        
################## RUN EXPERIMENT ##################
reaction_time_list = []
start_time_list = []
end_time_list = []
event_list = [[] for _ in range(120)]  # Create a list containing 120 (total trials) empty lists
click_list = []
   
# run eyetracker calibration
r = tracker.runSetupProcedure()

c = 0 #dummy counter
 
### Show Exp Window ###
win = visual.Window(
    #(900, 900),
    screen=0,
    units="pix",
    #allowGUI=True,
    fullscr=True,
    #checkTiming=False
)
    
mouse = event.Mouse(win=win)
    
for trial in list(range(1,31)): #30 trials (congruent: 5 scenes shown 5 times/incongruent: 5 scenes shown 1 time. 4 images per prompt. 100 congruent images, 20 incongruent images. 120 total images)

    targets = target_list[trial-1]
    # Convert target string back to a dictionary
    targets = ast.literal_eval(targets)
    
    for subtrial in list(range(1,5)):
        
        c += 1
        
        path_to_image_file = f'C:/Users/{user}/Dropbox/Kerri_Walter/generativeAI/5Levels/{participant}/{trial}.{subtrial}.jpg'        
        
        #wait until images have been generated/saved
        while not os.path.exists(path_to_image_file):
            text_stim = visual.TextStim(
                win,
                text="Loading...",
                pos=(0.0, 0.0),
                units="norm",
                height=0.05,
                wrapWidth=0.8,
            )
            text_stim.draw()
            win.flip()
            time.sleep(1)  # Wait before checking again
       
        # pass the image path to ImageStim to load and display:
        image_stim = visual.ImageStim(win, image=path_to_image_file)
        text_stim = visual.TextStim(
            win,
            text=targets[subtrial],
            pos=(0.0, 0.0),
            units="norm",
            height=0.05,
            wrapWidth=0.8,
        )
            
        text_stim.draw()
        win.flip()
        core.wait(2)
        image_stim.draw()
        win.flip()
        
        tracker.setRecordingState(True) #start tracking
        start_time = core.getTime() # Record the starting time
        
        #event.waitKeys(keyList=['space'])  # press space to continue
        # Wait for a left mouse click and record the position
        while True:
            # Check for quit key ('q') or mouse click
            keys = event.getKeys()
            if 'q' in keys:  # If 'q' key is pressed, quit the experiment
                print("Quit key pressed. Exiting the experiment.")
                win.close()
                core.quit()
                io.quit()
            if mouse.getPressed()[0]:  # Check if the left mouse button is clicked
                click_position = mouse.getPos()  # Get the position of the mouse click
                break  # Exit the loop once the click is detected
            
        events = tracker.getEvents() #events that happened this trial
        tracker.setRecordingState(False) #stop tracking
        end_time = core.getTime() # Record the ending time
        reaction_time = end_time - start_time # Record reaction time
                            
        reaction_time_list.append(reaction_time)
        start_time_list.append(start_time)
        end_time_list.append(end_time)
        event_list[c-1] = events #populate event_list for each trial 
        click_list.append(click_position)
        
        save_data()
        
win.close()
#core.quit()

# Stop the ioHub Server
io.quit()

# df = DataFrame({'Reaction Time': reaction_time_list, 
#                 'Start Time': start_time_list, 
#                 'End Time': end_time_list,
#                 'Mouse Position': click_list})
# df.to_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/{participant}_data.xlsx', sheet_name='sheet1', index=False)

# #eyetracker data
# with open(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/{participant}_gaze_data.json', 'w') as f:
#     json.dump(event_list, f)
