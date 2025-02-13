# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:00:39 2025

@author: Kerri
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import json

# Function to load the image and extract RGB values
def generate_rgb_map(image_path):
    # Open the image using Pillow
    img = Image.open(image_path)
    
    # Convert the image to RGB (in case it's not in RGB mode)
    img_rgb = img.convert('RGB')
    
    # Convert the image into a numpy array of RGB values
    global rgb_array
    rgb_array = np.array(img_rgb)
    
    # Print out the RGB values of each pixel
    print("RGB Map:")
    for row in rgb_array:
        print(row)
    
    # # Visualize the image RGB map (optional)
    # plt.imshow(rgb_array)
    # plt.title("RGB Map of Image")
    # plt.axis('off')  # Turn off axis for better view
    # plt.show()

image_path = 'C:/Users/Kerri/Dropbox/Kerri_Walter/generativeAI/BP/1.1.jpg'
generate_rgb_map(image_path)

#Gaze Data
gaze_path = f'C:\\Users\\Kerri\\Dropbox\\Kerri_Walter\\BexLabGenAI\\BP_gaze_data.json'
# Open gaze file
with open(gaze_path, 'r') as json_file:
    gaze_data = json.load(json_file)

#Grab fixations (using fixation end,  size: 29=fixStart, 35=gazeEvent, 65=fixEnd)
trial1 = gaze_data[0]
fixEnds = [i for i, x in enumerate(trial1) if len(x) == 65]
xycoords = [(trial1[i][45], trial1[i][46]) for i in fixEnds]
# Remove duplicates while preserving order
unique_xycoords = []
seen = set()
for coord in xycoords:
    if coord not in seen:
        unique_xycoords.append(coord)
        seen.add(coord)

xycoords = unique_xycoords
x_values, y_values = zip(*xycoords)

# total screen size is 3840x2160
# image size is 1024x1024
def get_rgb_value(image_array, x, y):
    # Adjust the coordinates based on the center origin (0, 0)
    x_index = int(x + 512) #1024/2
    y_index = int(y + 512)
    
    # # Ensure the indices are within bounds (0 to 1023)
    # x_index = max(0, min(1023, x_index))
    # y_index = max(0, min(1023, y_index))
    
    # Return the RGB value at the calculated indices
    return image_array[y_index, x_index]

#rgbVal = get_rgb_value(rgb_array, xycoords)

#def display_image_with_point(image_array, x, y):
def display_image_with_point(image_array, coordinates):
    
    # Create a figure with two subplots (one for the image, one for the swatch)
    fig, axs = plt.subplots(1, 2, figsize=(14, 8))

    # Display the image
    axs[0].imshow(image_array)
    
    #store RGB values for swatches
    rgb_values = []
    
    for i, (x, y) in enumerate(coordinates):
            # Get RGB value at this point
            rgb_value = get_rgb_value(image_array, x, y)
            rgb_values.append(rgb_value)
            
            # Plot the point on the image
            axs[0].scatter(x + 512, y + 512, color='red', s=100)  # Red point
            axs[0].text(x + 512, y + 512, str(i + 1), color='white', fontsize=12, ha='center', va='center')
        
    
    # # Plot the point on the image
    # # We reverse the y-axis for image coordinates (y increases downward)
    # axs[0].scatter(x + 512, y + 512, color='red', s=50, label=f"Point ({x}, {y})")  # Red point
    
    # # Add labels and title
    # axs[0].title("Fixations")
    # axs[0].xlabel("X Coordinate")
    # axs[0].ylabel("Y Coordinate")
    
   # Display the RGB swatches on the right subplot, vertically arranged
    num_swatches = len(rgb_values)
    axs[1].axis('off')  # Hide the axis for the swatches
    
    # Adjust the height for the swatches (space them vertically)
    axs[1].set_ylim(0, num_swatches * 0.1)  # Set a limit for vertical space

    # Loop over the RGB values and plot each swatch
    for i, rgb_value in enumerate(rgb_values):
        # Plot each RGB swatch as a 1x1 block of color
        axs[1].imshow([[rgb_value]], extent=[0, 1, i * 0.1, (i + 1) * 0.1])  # Adjust vertical positioning
        axs[1].text(1.05, (i + 0.5) * 0.1, f"{i + 1}: {rgb_value}", ha='left', va='center', fontsize=10, color='black')

    # # Plot the RGB swatches on the right subplot
    # for i, rgb_value in enumerate(rgb_values):
    #         axs[1].imshow([[rgb_value]])  # A 1x1 image with the RGB color
    #         axs[1].axis('off')  # Hide the axes for the swatch
            
    #         # Add a label to each RGB swatch with the corresponding number
    #         axs[1].text(0.5, 0.5, f"{i + 1}: {rgb_value}", ha='center', va='center', fontsize=10, color='black')
    #         axs[1].set_title("RGB Swatches")
        
    # # Display the color swatch in the second subplot
    # axs[1].imshow([[rgbVal]])  # A 1x1 image with the RGB color
    # axs[1].axis('off')  # Hide the axes for the swatch
    
    # # Set the title for the swatch
    # axs[1].set_title(f"RGB Value: {rgbVal}")
    
    # Show the plots
    plt.tight_layout()
    plt.show()

# # Display the image with the plotted point
# display_image_with_point(rgb_array, x_values[4], y_values[4])
display_image_with_point(rgb_array, xycoords)
