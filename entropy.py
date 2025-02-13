# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:29:47 2025

@author: bexlab
"""

import pandas as pd
from skimage.io import imread
from skimage.measure import shannon_entropy
import matplotlib.pyplot as plt

entropy = []

subjpth = 'C:/Users/bexlab/Dropbox/Kerri_Walter/generativeAI/5Levels/test'

for im in range(1,26):
    for sim in range(1,5):
        imgpth = f'{subjpth}/{im}.{sim}.jpg'
        
        # Read the image
        image = imread(imgpth, as_gray=True)
        
        # Calculate entropy
        entropy_value = shannon_entropy(image)
        entropy.append(entropy_value)
        
        #print("Entropy:", entropy_value)
        
        # Optionally, display the image and its entropy
        #plt.imshow(image, cmap='gray')
        #plt.title(f'Entropy: {entropy_value:.2f}')
        #plt.show()

testinfo = pd.read_excel('C:/Users/bexlab/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/test_prompt_info.xlsx')
clutter = [item for item in testinfo.Clutter for _ in range(4)]

# Create a DataFrame with data points and their respective categories
df = pd.DataFrame({
    'Clutter': clutter,
    'Entropy': entropy
})

order = ['Low', 'MediumLow', 'Medium', 'MediumHigh', 'High']
# Convert the 'Category' column to a categorical type with the defined order
df['Clutter'] = pd.Categorical(df['Clutter'], categories=order, ordered=True)

for clutter in order:
    category_data = df[df['Clutter'] == clutter]['Entropy']
    plt.scatter([clutter] * len(category_data), category_data, label=clutter)
    

# Add labels and title
plt.xlabel('Clutter')
plt.ylabel('Entropy')

plt.scatter(clutter,entropy)

### Reaction Time ###

subjdata = pd.read_excel('C:/Users/bexlab/Dropbox/Kerri_Walter/BexLabGenAI/5Levels/test_data.xlsx')
subjdata['Reaction Time']

plt.scatter(entropy,subjdata['Reaction Time'])

# Add labels and title
plt.xlabel('Entropy')
plt.ylabel('Reaction Time')