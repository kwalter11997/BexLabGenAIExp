# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 17:17:32 2024

@author: Kerri
"""

#### TO AVOID COMPATIBILITY ISSUES USE PYTHON 3.8 AND PSYCHOPY 2022.2.5 ####

import pandas as pd
import psychopy
import tkinter
from psychopy.iohub import launchHubServer
from psychopy.core import getTime, wait
from pandas import DataFrame

iohub_config = {'eyetracker.hw.gazepoint.gp3.EyeTracker':
    {'name': 'tracker', 'device_timer': {'interval': 0.005}}}
    
io = launchHubServer(**iohub_config)

# Get the eye tracker device.
tracker = io.devices.tracker

# run eyetracker calibration
r = tracker.runSetupProcedure()

# Check for and print any eye tracker events received...
tracker.setRecordingState(True)

# root = tkinter.Tk()
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# tracker.setDisplaySize(screen_width, screen_height)

stime = getTime()
while getTime()-stime < 2.0:
    for e in tracker.getEvents():
        print(e)
        
  
# Check for and print current eye position every 100 msec.
stime = getTime()
while getTime()-stime < 5.0:
    print(tracker.getPosition())
    wait(0.1)

events = tracker.getEvents()
for event in events:
    print("Raw X:", event['right_raw_x'], "Gaze X:", event['right_gaze_x'])

tracker.setRecordingState(False)

# Stop the ioHub Server
io.quit()


print(io.devices.__dict__)

event_names = ['experiment_id','session_id','device_id','event_id','type','device_time','logged_time','time','confidence_interval','delay','filter_id',
 'left_gaze_x','left_gaze_y','left_raw_x','left_raw_y','left_pupil_measure1','left_pupil_measure1_type','left_pupil_measure2','left_pupil_measure2_type',
 'right_gaze_x','right_gaze_y','right_raw_x','right_raw_y','right_pupil_measure1','right_pupil_measure1_type','right_pupil_measure2','right_pupil_measure2_type',
 'dial','dialv','gsr','gsrv','hr','hrv','hrp','status']

df = pd.DataFrame({
    "Name": event_names,
    "Value": event
})

# # If a connection already exists, close it. 
# try:    
#     tracker.setRecordingState(False)   
#     tracker.setConnectionState(False)    
#     io.quit() # Stop the ioHub Server
# except:    
#     pass
# io, tracker = SetUpEyeTracker(fixation_win)
# ResetET = False 
# RunningETCalibration = True

# while RunningETCalibration:     
#     # Run the gazepoint calibration    
#     ETCalibrationMode, FixationGazeRegion_radius, FixationRegion, ResetET, AveragingWindowDuration =     
#     RunGazePointCalibration(fixation_win, FixationGazeRegion_radius, ETCalibrationMode, 
#     FixReg_CalibratedDegree_X, FixReg_CalibratedDegree_Y, FixReg_Cal_X, FixReg_Cal_Y, ResetET, 
#     AveragingWindowDuration)    
#     if ResetET:     
#         # Stop and restart connection to prevent problems in cases when gaze point app needed restarting.                  
#         print("Restarting connection to Gazepoint...")        
#         # Stop eye data recording and connection        
#         try:           
#             tracker.setRecordingState(False)          
#             tracker.setConnectionState(False) 
#             io.quit() # Stop the ioHub Server        
#         except:           
#             pass       
#         # Then restart connection  
#         io, tracker = SetUpEyeTracker(fixation_win)        
#         ResetET = False   
#     elif not ResetET:        
#         RunningETCalibration = False  