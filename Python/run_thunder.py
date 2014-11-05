# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 12:23:07 2014
Main script to run thunder - caters mainly to Michelle's Olfactory Bulb Data 
with Thunder updated on Nov 1 2014
@author: seetha
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~ Required User Input ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Enter Main Folder containing stimulus folders. Ensure the data in the stimulus folders are registered 
## and are multitiffs in Z
Exp_Folder = '/Users/seetha/Desktop/Michelle_OB_Thunder/Data/141010 Fish2 Deconvolved/' 

#Prefix using which all text files, figures, matfiles and numpy array for this run of thunder will be saved. 
#If text file with prefixed name already exists, the script will go straight to running PCA 
filename_save_prefix = 'Allfiles' 

#Experiment parameters
img_size_x = 128 #X and Y resolution - if there are images that dont have this resolution, they will be resized
img_size_y = 256
num_time = 121  #Total Number of time points in experiment
num_z_planes = [1,4,5] #Mention z-planes to be used for analysis. If all planes to be used, say num_z_planes=0

#Only time points specified in these two variables will be used 
#for creating text files and further analysis
time_start = 20 #Starting time point 
time_end = 120 #Ending time point

#Set if you want to use raw images or delta f/f. If delta f/f is needed, specify baseline time points
f_f_flag = 0 #0-raw data, 1-delta f/f
dff_start = 1
dff_end = 10

#Stimulus Parameters
combine = 0 #1 - Combine timepoints from all stimulus folders in Exp_Folder, 0-Run PCA on each seperately

#PCA parameters
pca_components = 3 #Number of pca components to detect from files
num_pca_colors = 150 #Number of colors on the pca maps
num_samples = 10000 #number of random samples to select to do PCA reconstruction
thresh_pca = 0.0001 #Threshold above which to plot the pca components
color_map = 'polar' #Colormap for plotting principle components

######################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~ Importing Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Import some python libraries
import os
import numpy as np
import time

#Import thunder libraries
from thunder import ThunderContext

######################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Script ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

############### STEP 1 ######################
#Create text file 

#Check if text file already exists, else create it
txt_file = [f for f in os.listdir(Exp_Folder) if (f.endswith('.txt') and f.find(filename_save_prefix+'.txt')==0)]

#Create Stimulus folder
Stimulus_Folders = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f))]




