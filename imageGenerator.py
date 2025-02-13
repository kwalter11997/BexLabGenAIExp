# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:42:30 2024

@author: Kerri
"""
import selenium
import requests
import random
import pandas
import os
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from psychopy import core, event, visual, gui, data

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--participant", required=True, help="Participant name")
parser.add_argument("--user", required=True, help="User name")
args = parser.parse_args()

participant = args.participant
user = args.user

prompt_list = pandas.read_csv(f'C:/Users/{user}/Dropbox/Kerri_Walter/BexLabGenAI/{participant}_prompt_list.csv')

def setup():
    #open webpage
    driver = webdriver.Chrome()
    url = 'https://www.bing.com/images/create'
    driver.get(url)
    elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "q"))) #wait for page to load
    #login
    #assert "Bing" in driver.title
    elem = driver.find_element(By.NAME, "q")
    elem.send_keys(prompt)
    elem.send_keys(Keys.RETURN)
    #enter username
    elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "i0116"))) #wait for page to load
    elem = driver.find_element(By.ID, "i0116")
    elem.send_keys('bexlabAIexp@outlook.com')
    elem.send_keys(Keys.RETURN)
    #enter password
    elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "i0118"))) #wait for page to load
    elem = driver.find_element(By.ID, "i0118")
    elem.send_keys('BexLabAI')
    elem.send_keys(Keys.RETURN)
    #continue
    elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "acceptButton"))) #wait for page to load
    button = driver.find_element(By.ID, "acceptButton")
    button.click()
    return driver
  
def save_scenes():   
  
    button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "mimg"))) #wait for page to load
    button = driver.find_element(By.CLASS_NAME, "mimg")
    button.click()
    
    iframe = driver.find_element(By.TAG_NAME, "iframe") #switch to iframe
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(1) #wait for page to load

    for i in list(range(1,5)):
        # Locate the image    
        if i==1:
            image = driver.find_element(By.XPATH, "//*[@id='mainImageWindow']/div[1]/div/div/div/img")
        else:
            nextimg = driver.find_element(By.ID, "navr") #click next
            nextimg.click()
            image = driver.find_element(By.XPATH, "//*[@id='mainImageWindow']/div[2]/div/div/div/img")
        
        # Extract the image URL from the 'src' attribute
        image_url = image.get_attribute('src')
        #save in 1024x1024
        image_url = image_url.replace('270','1024')
        
        #save images to computer
        img_data = requests.get(image_url).content
        with open(f"/Users/{user}/Dropbox/Kerri_Walter/generativeAI/{participant}/{scene}.{i}.jpg", 'wb') as handler:
            handler.write(img_data)
    #exit
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    driver.switch_to.default_content()

### Set up randomization order for participant ###
shuffle_list = [0,0,1,1,2,2,3,3,4,4] #random order
random.shuffle(shuffle_list)
clutter_shuffle_list = [0,0,0,0,0,1,1,1,1,1] 
random.shuffle(clutter_shuffle_list)
scene = 1
    
### Create scenes ###
for imagetrial in list(range(1,11)): #10 trials (5 scenes shown twice, 4 images per prompt, 40 total images)
#for imagetrial in list(range(1,3)):
    
    prompt = prompt_list.Prompt[imagetrial-1]
    
    ### Save scenes ###
    if imagetrial == 1:         
         #open the webpage and login
         driver = setup() 
         elem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "q"))) #wait for page to load
         save_scenes()
         os.system("nircmd.exe win min class Chrome_WidgetWin_1") #minimize window
         scene += 1
    else:
        #Clear old prompt and input new one
        elem = driver.find_element(By.NAME, "q")
        elem.clear()
        elem.send_keys(prompt)
        elem.send_keys(Keys.RETURN)
        elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "mimg"))) #wait for page to load
        save_scenes()
        scene += 1
        
