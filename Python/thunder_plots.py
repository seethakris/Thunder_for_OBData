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


def plot_pca_maps(pca, maps, pts, clrs, recon, unique_clrs, matched_pixels, \
    matched_signals,  num_z_planes, Exp_Folder, filename_save_prefix, Stimulus_Name,\
    stim_start, stim_end):
     
    filesep = os.path.sep
     
    # To save as pdf create file
    Figure_PDFDirectory = Exp_Folder+filesep+'Figures'+filesep
    if not os.path.exists(Figure_PDFDirectory):
        os.makedirs(Figure_PDFDirectory)           
    pp = PdfPages(Figure_PDFDirectory+filename_save_prefix+'_PCA.pdf')
    
    sns.set_context("poster")  
    
    ############ Plot Colormaps of scores ############    
    #If there is only one stack, else plot each stack
    if len(maps.shape)==3:
        #Plot colored maps for each stack
        with sns.axes_style("white"):
            fig2 = plt.imshow(maps[:,:,:].transpose((1,0,2)))
            plt.title((Stimulus_Name + ' Z=' + str(num_z_planes[0])))
            plt.axis('off')
            fig2 = plt.gcf()
            pp.savefig(fig2)
            plt.close()

    else:
        for ii in range(0,np.size(maps,2)):
            with sns.axes_style("white"):
                fig2 = plt.imshow(maps[:,:,ii,:].transpose((1,0,2)))
                if num_z_planes ==0:
                    plt.title((Stimulus_Name + ' Z=' + str(ii+1)))
                else:
                    plt.title((Stimulus_Name + ' Z=' + str(num_z_planes[ii])))
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
            A = np.append(A, ['comp' + str(ii+1)])
        ax1.legend(A, loc=4)
        plot_vertical_lines(stim_start,stim_end)
        plt.axhline(y=0, linestyle='-', color='k', linewidth=1)
        
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
    
    #Plot mean projection    
    with sns.axes_style("white"):  
        temp = (np.mean(maps, axis=2))
        fig2 = plt.subplot(224)
        plt.imshow(temp.astype(np.float16))
        plt.axis('off')
        plt.title('Mean projection')
    
    plt.tight_layout()
    fig2 = plt.gcf()
    pp.savefig(fig2)
    plt.close()
    pp.close()
    
        
    
def plot_vertical_lines(stim_start,stim_end):
    plt.axvline(x=stim_start, linestyle='-', color='k', linewidth=1)
    plt.axvline(x=stim_end, linestyle='--', color='k', linewidth=1)
    
    

