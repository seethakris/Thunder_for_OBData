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
filename_save_prefix = 'test1' 

#Experiment parameters
img_size_x = 384 #X and Y resolution - if there are images that dont have this resolution, they will be resized
img_size_y = 502
num_time = 121  #Total Number of time points in experiment
num_z_planes = [1,4,5] #Mention z-planes to be used for analysis. If all planes to be used, say num_z_planes=0

#Only time points specified in these two variables will be used 
#for creating text files and further analysis
time_start = 0 #Starting time point 
time_end = 121 #Ending time point

#Stimulus on and off time
stim_start = 50 #Stimulus Starting time point 
stim_end = 60 #Stimulus Ending time point

#Set if you want to use raw images or delta f/f. If delta f/f is needed, specify baseline time points
f_f_flag =  0#0-raw data, 1-delta f/f
dff_start = 1
dff_end = 20

#Stimulus Parameters
combine = 0 #1 - Combine planes from all stimulus folders in Exp_Folder, 0-Run PCA on each seperately

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


#Import user defined libraries
from create_textfile_for_thunder import create_textfile
from create_textfile_for_thunder import create_textfile_combined

######################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Script ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

############### STEP 1 ######################
#Create text file 

#Check appropriate folders if combine = 0 or 1
#Find Stimulus folder
Stimulus_Folders = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f))] 

if combine == 0: #check for text file in individual folders   
    #Check if text file already exists in each stimulus folder, else create it
    for ii in range(0, len(Stimulus_Folders)):
        txt_file = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Folders[ii], 'Registered')) \
        if (f.find(filename_save_prefix+'.txt')==0)]
            
        if len(txt_file)==0: 
            start_time = time.time() 
            print 'Saving images to text on '+Stimulus_Folders[ii]
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Folders[ii], 'Registered')
            Matfile_for_thunder = create_textfile(Working_Directory, filename_save_prefix, img_size_x, img_size_y,\
            num_time, time_start, time_end, num_z_planes, stim_start, stim_end, f_f_flag, dff_start, dff_end) #Create text file
            print 'Saving to text file took '+ str(int(time.time()-start_time)) +' seconds'

else:#check for text file in top folder
    
    txt_file = [f for f in os.listdir(Exp_Folder) if (f.find(filename_save_prefix+'.txt')==0)]

    if len(txt_file)==0: 
        start_time = time.time() 
        print 'Saving images to text on all files in '+ Exp_Folder
        Matfile_for_thunder = create_textfile_combined(Exp_Folder, filename_save_prefix, img_size_x, img_size_y,\
        num_time, time_start, time_end, num_z_planes, stim_start, stim_end, f_f_flag, dff_start, dff_end) #Create text file
        print 'Saving to text file took '+ str(int(time.time()-start_time)) +' seconds'



