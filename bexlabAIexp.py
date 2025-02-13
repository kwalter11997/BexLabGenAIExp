# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:59:31 2024

@author: Kerri
"""

#### TO AVOID COMPATIBILITY ISSUES USE PYTHON 3.8 AND PSYCHOPY 2022.2.5 ####

#pip install selenium
#pip install requests
#pip install psychopy

#import selenium
import psychopy
#import requests
#import random
import pandas
import os
import getpass
import argparse
import ast

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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
output_dir = f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI'
os.makedirs(output_dir, exist_ok=True)

# # Define the directory where the participant data will be stored
# user = getpass.getuser()
# directory = fr'C:\Users\{user}\Dropbox\Kerri_Walter\BexLabGenAI'

# #lists for prompts
# places = ['kitchen', 'bathroom', 'bedroom', 'office', 'living room']
# colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

# kitchen_things = ['knife', 'bowl', 'stove', 'kettle', 'fridge']
# bathroom_things = ['sink', 'toilet', 'towel', 'toothbrush', 'shower']
# bedroom_things = ['bed', 'chair', 'nightstand', 'book', 'pillow']
# office_things = ['computer', 'desk', 'file cabinet', 'pens', 'printer']
# livingroom_things = ['couch', 'tv', 'table', 'painting', 'rug']

target_list = pandas.read_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/{participant}_prompt_info.xlsx')
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
                            'status'],

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


# # Function to check if a participant name already exists and increment if necessary
# def get_unique_participant_name(participant_name, directory):
#     base_name = participant_name
#     c = 1
#     # Check if the base_name exists and increment if it does
#     while os.path.exists(os.path.join(directory, base_name + (f"{c}" if c > 1 else "") + ".xlsx")):
#         c += 1
#     # Return the name with the counter appended
#     return base_name + (f"{c}" if c > 1 else "")

# def setup():
#     #open webpage
#     driver = webdriver.Chrome()
#     url = 'https://www.bing.com/images/create'
#     driver.get(url)
#     elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "q"))) #wait for page to load
#     #login
#     #assert "Bing" in driver.title
#     elem = driver.find_element(By.NAME, "q")
#     elem.send_keys(prompt)
#     elem.send_keys(Keys.RETURN)
#     #enter username
#     elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "i0116"))) #wait for page to load
#     elem = driver.find_element(By.ID, "i0116")
#     elem.send_keys('bexlabAIexp@outlook.com')
#     elem.send_keys(Keys.RETURN)
#     #enter password
#     elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "i0118"))) #wait for page to load
#     elem = driver.find_element(By.ID, "i0118")
#     elem.send_keys('BexLabAI')
#     elem.send_keys(Keys.RETURN)
#     #continue
#     elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "acceptButton"))) #wait for page to load
#     button = driver.find_element(By.ID, "acceptButton")
#     button.click()
#     return driver
  
# def save_scenes():   
  
#     button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "mimg"))) #wait for page to load
#     button = driver.find_element(By.CLASS_NAME, "mimg")
#     button.click()
    
#     iframe = driver.find_element(By.TAG_NAME, "iframe") #switch to iframe
#     driver.switch_to.frame(iframe)
#     driver.implicitly_wait(1) #wait for page to load

#     for i in list(range(1,5)):
#         # Locate the image    
#         if i==1:
#             image = driver.find_element(By.XPATH, "//*[@id='mainImageWindow']/div[1]/div/div/div/img")
#         else:
#             nextimg = driver.find_element(By.ID, "navr") #click next
#             nextimg.click()
#             image = driver.find_element(By.XPATH, "//*[@id='mainImageWindow']/div[2]/div/div/div/img")
        
#         # Extract the image URL from the 'src' attribute
#         image_url = image.get_attribute('src')
#         #save in 1024x1024
#         image_url = image_url.replace('270','1024')
        
#         #save images to computer
#         img_data = requests.get(image_url).content
#         with open(f"/Users/{user}/Dropbox/Kerri_Walter/generativeAI/{expInfo['Participant']}/{scene}.{i}.jpg", 'wb') as handler:
#             handler.write(img_data)
#     #exit
#     webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#     driver.switch_to.default_content()
    
# def create_prompt(trial):
#     random_place = shuffle_list[trial-1]
#     global place
#     if random_place == 0:
#         place = 'kitchen'
#         things = kitchen_things
#     elif random_place == 1:
#         place = 'bathroom'
#         things = bathroom_things
#     elif random_place == 2:
#         place = 'bedroom'
#         things = bedroom_things
#     elif random_place == 3:
#         place = 'office'
#         things = office_things
#         place = 'livingroom'
#     elif random_place == 4:
#         things = livingroom_things
   
#     global clutter
#     if clutter_shuffle_list[trial-1] == 0:
#         prompt_clutter = ''
#         clutter = 'Low'
#     else:
#         prompt_clutter = ' high clutter'
#         clutter = 'High'
        
#     random_things = random.sample(range(len(things)-1), 4) #random things (no duplicates)
#     random_colors = random.sample(range(len(colors)-1), 4) #random colors (no duplicates)

#     global prompt
#     prompt = f'a photorealistic{prompt_clutter} {places[random_place]} with {colors[random_colors[0]]} {things[random_things[0]]}, {colors[random_colors[1]]} {things[random_things[1]]}, {colors[random_colors[2]]} {things[random_things[2]]}, and {colors[random_colors[3]]} {things[random_things[3]]}'

#     global targets
#     targets = {
#         1: f"{colors[random_colors[0]]} {things[random_things[0]]}",
#         2: f"{colors[random_colors[1]]} {things[random_things[1]]}",
#         3: f"{colors[random_colors[2]]} {things[random_things[2]]}",
#         4: f"{colors[random_colors[3]]} {things[random_things[3]]}"
#     }
        
################## RUN EXPERIMENT ##################
# shuffle_list = [0,0,1,1,2,2,3,3,4,4] #random order
# random.shuffle(shuffle_list)
# clutter_shuffle_list = [0,0,0,0,0,1,1,1,1,1] 
# random.shuffle(clutter_shuffle_list)
# scene = 1

# #Get participant info
# expName = 'BexLab Gen AI Experiment'
# expInfo = {'Participant':''}
# #expInfo = {'Participant':'', 'session':'w2020'}
# dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False,title=expName)
# if dlg.OK == False:
#     core.quit()
# expInfo['Date'] = data.getDateStr()
# # Check if the participant name is empty, and if so, prompt for input
# if not expInfo['Participant']:
#     core.quit()  # Quit if no participant name is provided
# # Ensure participant name is unique
# expInfo['Participant'] = get_unique_participant_name(expInfo['Participant'], directory)
# os.makedirs(f'C:/Users/{user}/Dropbox/Kerri_Walter/generativeAI/{expInfo["Participant"]}') #create a folder for this participants images

# place_list =[]
# target_list=[]
# clutter_list=[]
reaction_time_list = []
start_time_list = []
end_time_list = []
event_list = []
   
# run eyetracker calibration
r = tracker.runSetupProcedure()
     
#for trial in list(range(1,11)): #10 trials (5 scenes shown twice, 4 images per prompt, 40 total images)
for trial in list(range(1,3)):
    
    # create_prompt(trial)
    
    # ### Save scenes ###
    # if trial == 1:         
    #      #open the webpage and login
    #      driver = setup() 
    #      elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "q"))) #wait for page to load
    #      save_scenes()
    #      scene += 1
    # else:
    #     #Clear old prompt and input new one
    #     elem = driver.find_element(By.NAME, "q")
    #     elem.clear()
    #     elem.send_keys(prompt)
    #     elem.send_keys(Keys.RETURN)
    #     elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "mimg"))) #wait for page to load
    #     save_scenes()
    #     scene += 1

    ### Show Exp Window ###
    win = visual.Window(
        (900, 900),
        screen=0,
        units="pix",
        #allowGUI=True,
        fullscr=False,
        #checkTiming=False
    )

    targets = target_list[trial-1]
    # Convert target string back to a dictionary
    targets = ast.literal_eval(targets)
    
    for subtrial in list(range(1,5)):
        
        path_to_image_file = f'C:/Users/{user}/Dropbox/Kerri_Walter/generativeAI/{participant}/{trial}.{subtrial}.jpg'        
        # pass the image path to ImageStim to load and display:
        image_stim = visual.ImageStim(win, image=path_to_image_file)
        text_stim = visual.TextStim(
            win,
            text=targets[subtrial],
            pos=(0.0, 0.8),
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
        event.waitKeys(keyList=['space'])  # press space to continue
        events = tracker.getEvents() #events that happened this trial
        tracker.setRecordingState(False) #stop tracking
        end_time = core.getTime() # Record the ending time
        reaction_time = end_time - start_time # Record reaction time
        
               
        for e in events:
            event_list.append(e)
       
            
        # place_list.append(place)
        # target_list.append(targets[subtrial])
        # clutter_list.append(clutter)
        reaction_time_list.append(reaction_time)
        start_time_list.append(start_time)
        end_time_list.append(end_time)
        
    win.close()
    #core.quit()

# Stop the ioHub Server
io.quit()

### save data to file ###    
# df = DataFrame({'Scene': place_list, 
#                 'Target': target_list, 
#                 'Clutter': clutter_list, 
#                 'Reaction Time': reaction_time_list, 
#                 'Start Time': start_time_list, 
#                 'End Time': end_time_list})
# df.to_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/{expInfo["Participant"]}.xlsx', sheet_name='sheet1', index=False)

df = DataFrame({'Reaction Time': reaction_time_list, 
                'Start Time': start_time_list, 
                'End Time': end_time_list})
df.to_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/{participant}_time_data.xlsx', sheet_name='sheet1', index=False)

# #eyetracker data
# eyetracker_df = DataFrame({
#     'Name': GazepointSampleEvent_names,
#     'Value': e})
# eyetracker_df.to_excel(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/{participant}_gazeData.xlsx', sheet_name='sheet1', index=False)

## TODO - optomize create_scenes to run in background during trials
## TODO - get eyetracking data

