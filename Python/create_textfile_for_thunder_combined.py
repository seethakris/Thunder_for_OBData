# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 17:25:01 2014
Convert data to text from multi tiffs from all stimulus folders in the experiment folder
and concatenate their time points for PCA
@author: seetha
"""

#Import relevant libraries
import numpy as np #for numerical operations on arrays
import PIL as pil # for image resizing
import os  

import matplotlib.pyplot as plt #for plotting
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

from libtiff import TIFF #for reading multiTiffs

#Custom libraries
from smooth import smooth

smooth_window = 5

def create_textfile_combined(Exp_Folder, Stimulus_Folders, filename_save_prefix, img_size_x, img_size_y,\
            img_size_crop_x, img_size_crop_y, num_time, time_start, time_end, num_z_planes, stim_start, stim_end,\
            f_f_flag, dff_start, dff_end):
    filesep = os.path.sep #Get fileseperator according to operating system
    
    # To plot as PDF create directory
    Figure_PDFDirectory = Exp_Folder+filesep+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory) 
    pp = PdfPages(Figure_PDFDirectory+filename_save_prefix+'_PreprossData_Combined.pdf')
    
    zz = 0 #each multitiff file is considered as one stack
    Matfile_for_Thunder_Combined = None
    
    #Get data from multitiffs. - Conditions to check while loading data - num_z_planes and time_start and time_end
    if num_z_planes!=0: # Get only planes specified in the array num_z_planess
        for stim in Stimulus_Folders:
            Matfile_for_Thunder = None
            
            for lst in xrange(0,np.size(num_z_planes, axis=0)): 
                tif = TIFF.open(os.path.join(Exp_Folder,stim,'Registered',('Registered_Z='+str(num_z_planes[lst])+'.tif')), mode='r') #Open multitiff 
                
                zz = zz+1  #Update the number of current z plane to add to text file
            
                # Get image data as a matrix. Also Plot average image for validation
                data = get_data_from_tiff(tif, stim, img_size_x, img_size_y, num_time, num_z_planes[lst], pp) #get data in matrix form from multitiff
                
                #Get data in thunder format [xx,yy,zz,time]
                temp_matfile_for_thunder = get_matrix_for_textfile(data,img_size_crop_x, img_size_crop_y,\
                stim, zz, time_start, time_end,f_f_flag, dff_start, dff_end, stim_start,stim_end, num_z_planes[lst], pp)
                
                #Append each tiff files data to a bigger matrix - for each stimulus first
                if Matfile_for_Thunder is None:
                    Matfile_for_Thunder = temp_matfile_for_thunder
                else:
                    Matfile_for_Thunder = np.append(Matfile_for_Thunder,temp_matfile_for_thunder, axis=0)
            
            #Append each tiff files from all stimulus folders to a bigger file
            if Matfile_for_Thunder_Combined is None:
                Matfile_for_Thunder_Combined = Matfile_for_Thunder
            else:
                Matfile_for_Thunder_Combined = np.append(Matfile_for_Thunder_Combined,Matfile_for_Thunder[:,3:], axis=1)
    
    elif num_z_planes==0: #Get all files
        for stim in Stimulus_Folders:
            Matfile_for_Thunder = None
            
            #Find tiff files in given experiment folder 
            onlyfiles = [ f for f in os.listdir(os.path.join(Exp_Folder, stim, 'Registered'))\
            if (os.path.isfile(os.path.join(Exp_Folder, stim, 'Registered',f)) and f.find('.tif')>0 and f.find('Registered_Z=')==0)]
    
            for lst in xrange(1,np.size(onlyfiles, axis=0)+1): 
                tif = TIFF.open(os.path.join(Exp_Folder,stim,'Registered',('Registered_Z='+str(lst)+'.tif')), mode='r') #Open multitiff 
                
                zz = zz+1  #Update the number of current z plane to add to text file
            
                # Get image data as a matrix. Also Plot average image for validation
                data = get_data_from_tiff(tif, stim, img_size_x, img_size_y, num_time, lst, pp) #get data in matrix form from multitiff
                
                #Get data in thunder format [xx,yy,zz,time]
                temp_matfile_for_thunder = get_matrix_for_textfile(data, img_size_crop_x, img_size_crop_y, 
                stim, zz, time_start, time_end,f_f_flag, dff_start, dff_end, stim_start,stim_end, lst, pp)
                
                #Append each tiff files data to a bigger matrix - for each stimulus first
                if Matfile_for_Thunder is None:
                    Matfile_for_Thunder = temp_matfile_for_thunder
                else:
                    Matfile_for_Thunder = np.append(Matfile_for_Thunder,temp_matfile_for_thunder, axis=0)
            
            #Append each tiff files from all stimulus folders to a bigger file
            if Matfile_for_Thunder_Combined is None:
                Matfile_for_Thunder_Combined = Matfile_for_Thunder
            else:
                Matfile_for_Thunder_Combined = np.append(Matfile_for_Thunder_Combined,Matfile_for_Thunder[:,3:], axis=1)               
    
    #Smoothen the t series
    Matfile_for_Thunder_Combined_smooth = np.zeros([np.size(Matfile_for_Thunder_Combined,0), np.size(Matfile_for_Thunder_Combined,1)+smooth_window-1])
    Matfile_for_Thunder_Combined_smooth[:,0:3] = Matfile_for_Thunder_Combined[:,0:3]    
    for ii in range(0, np.size(Matfile_for_Thunder_Combined,0)):
        Matfile_for_Thunder_Combined_smooth[ii,3:] = smooth(Matfile_for_Thunder_Combined[ii,3:],smooth_window,'hanning')
    
    
    
    pp.close()        
    print 'Saving all the data in the text file '            
    np.savetxt(Exp_Folder+filesep+filename_save_prefix+'_combine.txt', Matfile_for_Thunder_Combined_smooth, fmt='%i')#Save as text file
    
    return Matfile_for_Thunder_Combined_smooth


def get_data_from_tiff(tif, stim, img_size_x, img_size_y, num_time, filename, pp):
    data = np.zeros((img_size_x,img_size_y,num_time), dtype=np.uint8)
    ii = 0
    for image in tif.iter_images():
        #Check if image is of the xy resolution specified, else resize
        if np.size(image,1)!=img_size_y or np.size(image,0)!=img_size_x:
            if ii == 0: #Print that there is a size mismatch
                print 'Size mismatch..Resizing Stim ' + stim + ' Z='+ str(filename)
            temp_image = pil.Image.fromarray(image)    
            data[:,:,ii] = np.array(temp_image.resize((img_size_y, img_size_x), pil.Image.NEAREST))            
            ii = ii+1
        else:
            data[:,:,ii] = image
            ii = ii+1   
    #Plot average data over time for reviewingin grayscale      
    with sns.axes_style("white"):
        fig1 = plt.imshow(np.mean(data[:,:,:], axis=2), cmap='gray')
        plt.title('Stim ' + stim + ' Z='+str(filename))
        plt.axis('off')
        fig1 = plt.gcf()
        pp.savefig(fig1)
        plt.close()
        
    return data
    
       
def get_matrix_for_textfile(data, img_size_crop_x, img_size_crop_y, stim, zz, time_start, time_end,\
    f_f_flag, dff_start, dff_end,stim_start,stim_end,filename, pp):
    
    #Cropping unwanted pixels as specified by user
    if img_size_crop_x!= 0 and img_size_crop_y!=0:
        print "Cropping x and y pixels.."
        data1 = data[img_size_crop_y:-img_size_crop_y, img_size_crop_x:-img_size_crop_x]
    elif img_size_crop_x==0 and img_size_crop_y!=0:
        print "Cropping only y pixels.."
        data1 = data[img_size_crop_y:-img_size_crop_y, :]
    elif img_size_crop_x!=0 and img_size_crop_y==0:
        print "Cropping only x pixels.."
        data1 = data[:, img_size_crop_x:-img_size_crop_x]
    else:
        data1 = data
   
    print 'Creating array from stack for Stim ' + stim + ' Z='+ str(filename)
    temp_matfile_for_thunder = np.zeros([np.size(data1, axis=0)*np.size(data1, axis=1),3+(time_end-time_start)], dtype=np.int)
    count = 0    
    for yy in xrange(0,np.size(data1, axis=1)):
        for xx in xrange(0,np.size(data1, axis=0)): 
            temp_matfile_for_thunder[count,0] = xx+1;
            temp_matfile_for_thunder[count,1] = yy+1;
            temp_matfile_for_thunder[count,2] = zz;
            # Create delta f/f values if necessary
            if f_f_flag==0:
                temp_matfile_for_thunder[count,3:] = data1[xx,yy,time_start:time_end]
            else:
                temp_matfile_for_thunder[count,3:] = (data1[xx,yy,time_start:time_end]-np.mean(data1[xx,yy,dff_start:dff_end]))/np.std(data1[xx,yy,dff_start:dff_end])
            count = count+1 
    
    #Plot heatmap for validation    
    with sns.axes_style("white"):
        A = temp_matfile_for_thunder[:,3:]    
        B = np.argsort(np.mean(A, axis=1))  
        C = A[B,:]
        if f_f_flag == 1: #Plot with correct climif dff is true
            fig2 = plt.imshow(C[-1000:,:],aspect='auto', cmap='jet',vmin=-5, vmax=5)
        else:
            fig2 = plt.imshow(C[-1000:,:],aspect='auto', cmap='jet')
        plot_vertical_lines(stim_start-time_start,stim_end-time_start)
        labels, locs = plt.xticks()
        labels1 = [int(item) for item in labels]
        labels2 = [str(int(item)+time_start) for item in labels]
        plt.xticks((labels1),(labels2))
        plt.xlim(0,(time_end-time_start))
        plt.title('Sorted Heatmap Z='+str(filename))
        plt.colorbar()
        fig2 = plt.gcf()
        pp.savefig(fig2)
        plt.close()
        A = None    

    return temp_matfile_for_thunder

def plot_vertical_lines(stim_start,stim_end):
    plt.axvline(x=stim_start, linestyle='-', color='k', linewidth=1)
    plt.axvline(x=stim_end, linestyle='--', color='k', linewidth=1)