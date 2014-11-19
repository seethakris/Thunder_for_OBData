# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 08:50:59 2014
Plot PCA components and maps for OB data 
@author: seetha
"""

#Import python libraries
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns #For creating nice plots


def plot_pca_maps_for_stacks(pca, maps, pts, clrs, recon, unique_clrs, matched_pixels, matched_signals, num_z_planes,\
        Exp_Folder, filename_save_prefix, Stimulus_Name, stim_start, stim_end):
        
    filesep = os.path.sep
     
    # To save as pdf create file
    Figure_PDFDirectory = Exp_Folder+filesep+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory)           
    pp = PdfPages(Figure_PDFDirectory+filename_save_prefix+'_PCA_Stacks.pdf')
                
    sns.set_context("poster") 
    
    if num_z_planes!=0:
        Filenames_stim = [ii + ' Z='+ str(jj)  for jj in num_z_planes for ii in Stimulus_Name]
    else:
        Filenames_stim = [ii + ' Z='+ str(jj+1) for jj in range(0,np.size(maps,2)) for ii in Stimulus_Name]
    
    ############ Plot Colormaps of scores ############    
    for ii in range(0,np.size(Filenames_stim)):
        with sns.axes_style("white"):
            fig2 = plt.imshow(maps[:,:,ii,:].transpose((1,0,2)))
            plt.title((Filenames_stim[ii]))
            plt.axis('off')                   
            fig2 = plt.gcf()
            pp.savefig(fig2)
            plt.close()    
            
    
    ########### Plot components ##################
    fig2 = plt.figure()
    sns.set_context("talk", font_scale=1.25)
    with sns.axes_style("darkgrid"):
        ax1 = plt.subplot(221)
        plt.plot(pca.comps.T);
        plt.locator_params(axis = 'y', nbins = 4)
        sns.axlabel("Time (seconds)","a.u")
        A = []
        for ii in xrange(0,np.size(pca.comps.T, 0)):
            A = np.append(A, [str(ii+1)])
            
        ax1.legend(A, loc=4)
        plt.axhline(y=0, linestyle='-', color='k', linewidth=1)
        plot_vertical_lines(stim_start,stim_end)
        
    
    #Plot mean signals according to color and boxplot of number of pixels in each plane
    with sns.axes_style("darkgrid"):
        for ii in range(0,np.size(unique_clrs,0)):       
            fig2 = plt.subplot(223)
            sns.tsplot(np.array(matched_signals[ii].clr_grped_signal), linewidth=3, ci=95, err_style="ci_band", color=unique_clrs[ii])
            plt.locator_params(axis = 'y', nbins = 4)            
            sns.axlabel("Time (seconds)","a.u")            
        plot_vertical_lines(stim_start,stim_end)
        plt.axhline(y=0, linestyle='-', color='k', linewidth=1)

    
    with sns.axes_style("white"):
        fig2 = plt.subplot(222)
        fig2 = sns.boxplot(np.transpose(matched_pixels),linewidth=3, widths=.5, color=unique_clrs)
        for ii in range(0,np.size(unique_clrs,0)):
            fig2 = plt.plot(np.repeat(ii+1,np.size(matched_pixels,1)), np.transpose(matched_pixels[ii,:]),'s', \
            color=unique_clrs[ii], markersize=5, markeredgecolor='k', markeredgewidth=2) 
            plt.locator_params(axis = 'y', nbins = 4)
        sns.axlabel("Colors", "Number of Pixels")
        sns.despine(offset=10, trim=True);  
        
    
    plt.tight_layout()
    fig2 = plt.gcf()
    pp.savefig(fig2)
    plt.close()
   
    for stim in xrange(0,np.size(Stimulus_Name)):
       with sns.axes_style("white"):
           same_stim_folders = [Filenames_stim.index(ii) for ii in Filenames_stim if ii.find(Stimulus_Name[stim])==0]
           fig2 = plt.subplot(221)
           matched_pixels_stim = matched_pixels[:,same_stim_folders]
           fig2 = sns.boxplot(np.transpose(matched_pixels_stim),linewidth=3, widths=.5, color=unique_clrs)
           
           for ii in range(0,np.size(unique_clrs,0)):
               fig2 = plt.plot(np.repeat(ii+1,np.size(matched_pixels_stim,1)), np.transpose(matched_pixels_stim[ii,:]),'s', \
               color=unique_clrs[ii], markersize=5, markeredgecolor='k', markeredgewidth=2) 
               plt.locator_params(axis = 'y', nbins = 4)
               
           sns.axlabel("Colors", "Number of Pixels")
           sns.despine(offset=10, trim=True)  
           
           
           for ii in range(0,np.size(unique_clrs,0)):       
                fig2 = plt.subplot(223)
                sns.tsplot(np.array(matched_signals[ii].clr_grped_signal), linewidth=3, ci=95, err_style="ci_band", color=unique_clrs[ii])
                plt.locator_params(axis = 'y', nbins = 4)            
                sns.axlabel("Time (seconds)","a.u")            
                plot_vertical_lines(stim_start,stim_end)
           plt.axhline(y=0, linestyle='-', color='k', linewidth=1)
           
           fig2 = plt.subplot(222)
           temp = (np.mean(maps[:,:,same_stim_folders,:], axis=2))
           plt.imshow(temp.astype(np.float16))
           plt.axis('off')
           plt.title('Mean projection' + Stimulus_Name[stim])
           plt.tight_layout()
           
           fig2 = plt.gcf()
           pp.savefig(fig2)
           plt.close()
    
    pp.close()
        
        
def plot_vertical_lines(stim_start,stim_end):
    plt.axvline(x=stim_start, linestyle='-', color='k', linewidth=1)
    plt.axvline(x=stim_end, linestyle='--', color='k', linewidth=1)
    
    

    
