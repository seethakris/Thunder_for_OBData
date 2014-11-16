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
filename_save_prefix = 'test9' 

#Experiment parameters
img_size_x = 20 #X and Y resolution - if there are images that dont have this resolution, they will be resized
img_size_y = 20 
img_size_crop_x = 3 #How many pixels to crop on x and y axis. If none say 0
img_size_crop_y = 3

num_time = 121  #Total Number of time points in experiment
num_z_planes = [1,3] #Mention z-planes to be used for analysis. eg [1,3,8] If all planes to be used, say num_z_planes=0

#Only time points specified in these two variables will be used 
#for creating text files and further analysis
time_start = 1 #Starting time point 
time_end = 121 #Ending time point

#Stimulus on and off time
stim_start = 50 #Stimulus Starting time point 
stim_end = 60 #Stimulus Ending time point

#Set if you want to use raw images or delta f/f. If delta f/f is needed, specify baseline time points
f_f_flag =  0 #0-raw data, 1-delta f/f
dff_start = 10
dff_end = 20

#Stimulus Parameters
combine = 0 #1 - Combine time points from all stimulus planes in Exp_Folder, 0-Run PCA on each seperately

#PCA parameters
pca_components = 4 #Number of pca components to detect from files
num_pca_colors = 150 #Number of colors on the pca maps
num_samples = 3000 #number of random samples to select to do PCA reconstruction
thresh_pca = 0.0001 #Threshold above which to plot the pca components
color_map = 'polar' #Colormap for plotting principle components

######################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~ Importing Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Import some python libraries
import os
filesep = os.path.sep
import time

#Import thunder libraries
from thunder import ThunderContext


#Import user defined libraries
from create_textfile_for_thunder import create_textfile
from create_textfile_for_thunder_combined import create_textfile_combined
from thunder_analysis import run_pca
from thunder_analysis import make_pca_maps
from thunder_plots import plot_pca_maps
######################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~ Main Script ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

############### STEP 1 ######################
#Create text file 

#Check appropriate folders if combine = 0 or 1
#Find Stimulus folder
Stimulus_Folders = [f for f in os.listdir(Exp_Folder) if os.path.isdir(os.path.join(Exp_Folder, f)) and f.find('Figures')<0] 

if combine == 0: #check for text file in individual folders   
    #Check if text file already exists in each stimulus folder, else create it
    for ii in range(0, len(Stimulus_Folders)):
        txt_file = [f for f in os.listdir(os.path.join(Exp_Folder, Stimulus_Folders[ii], 'Registered')) \
        if (f.find(filename_save_prefix+'.txt')==0)]
            
        if len(txt_file)==0: 
            start_time = time.time() 
            print 'Saving images individually to text on '+Stimulus_Folders[ii]
            Working_Directory = os.path.join(Exp_Folder, Stimulus_Folders[ii], 'Registered')
            Matfile_for_thunder = create_textfile(Working_Directory, filename_save_prefix, img_size_x, img_size_y,\
            img_size_crop_x, img_size_crop_y,num_time, time_start, time_end, num_z_planes,\
            stim_start, stim_end, f_f_flag, dff_start, dff_end) #Create text file
            print 'Saving to text file took '+ str(int(time.time()-start_time)) +' seconds'

else:#check for text file in top folder
    
    txt_file = [f for f in os.listdir(Exp_Folder) if (f.find(filename_save_prefix+'.txt')==0)]

    if len(txt_file)==0: 
        start_time = time.time() 
        print 'Saving images to text for all files in '+ Exp_Folder
        Matfile_for_thunder = create_textfile_combined(Exp_Folder, Stimulus_Folders, filename_save_prefix, img_size_x, img_size_y,\
        img_size_crop_x, img_size_crop_y, num_time, time_start, time_end, num_z_planes, \
        stim_start, stim_end, f_f_flag, dff_start, dff_end) #Create text file
        print 'Saving to text file took '+ str(int(time.time()-start_time)) +' seconds'
        

################ STEP 2 ######################
#Start Thunder Context.
print 'Starting Thunder Now. Check console for details'
tsc = ThunderContext.start(appName="thunderpca")
time.sleep(2)

############## STEP 3 ######################  
#Load data and run pca from the text file using thunder context. 
#Work on each stimulus folder individually if combine = 0, together if combine =1

if combine == 0:    
    for ii in range(0, len(Stimulus_Folders)):
        Working_Directory = os.path.join(Exp_Folder, Stimulus_Folders[ii], 'Registered')
        #Load data        
        data = tsc.loadSeries(Working_Directory+filesep+filename_save_prefix+'.txt', inputformat='text', nkeys=3)
        data = data.cache()

        #Run PCA
        start_time = time.time()   
        print 'Running pca individually...on '+Stimulus_Folders[ii]
        pca, imgs_pca = run_pca(data,pca_components)                
        print 'Running PCA took '+ str(int(time.time()-start_time)) +' seconds'  
        
        #Create polar maps
        start_time = time.time()   
        print 'Creating polar maps...on '+ Stimulus_Folders[ii]
        maps, pts, clrs, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal = make_pca_maps(pca, imgs_pca, img_size_x,\
        img_size_y, num_pca_colors, num_samples, thresh_pca, color_map)
        print 'Creating polar maps took '+ str(int(time.time()-start_time)) +' seconds'
        
        #Plot PCA components and maps
        start_time = time.time()   
        print 'Plotting PCA figures...on '+ Stimulus_Folders[ii]
        plot_pca_maps(pca, maps, pts, clrs, recon, unique_clrs, matched_pixels, matched_signals, num_z_planes,\
        Working_Directory, filename_save_prefix, Stimulus_Folders[ii], stim_start, stim_end)        
        print 'Plotting PCA figures took '+ str(int(time.time()-start_time)) +' seconds'
       
else:
    
        Working_Directory = Exp_Folder
        #Load data        
        data = tsc.loadSeries(Working_Directory+filesep+filename_save_prefix+'.txt', inputformat='text', nkeys=3)
        data.center()        
        data = data.cache()

        #Run PCA
        start_time = time.time()   
        print 'Running pca for all files...in '+ Exp_Folder
        pca, imgs_pca = run_pca(data,pca_components)                
        print 'Running PCA took '+ str(int(time.time()-start_time)) +' seconds'  
        
        #Create polar maps
        start_time = time.time()   
        print 'Creating polar maps for all files...in '+ Exp_Folder
        maps, pts, clrs, recon, unique_clrs, matched_pixels, matched_signals, mean_signal, sem_signal = make_pca_maps(pca, imgs_pca, img_size_x,\
        img_size_y, num_pca_colors, num_samples, thresh_pca, color_map)
        print 'Creating polar maps took '+ str(int(time.time()-start_time)) +' seconds'
        
        #Plot PCA components and maps
        start_time = time.time()   
        print 'Plotting PCA figure sfor all files...in '+Exp_Folder
        Exp_Folder_Name = Exp_Folder[Exp_Folder[:-1].rfind('/')+1:-1]        
        plot_pca_maps(pca, maps, pts, clrs, recon, unique_clrs, matched_pixels, matched_signals, num_z_planes,\
        Working_Directory, filename_save_prefix, Exp_Folder_Name, stim_start, stim_end)        
        print 'Plotting PCA figures took '+ str(int(time.time()-start_time)) +' seconds'






