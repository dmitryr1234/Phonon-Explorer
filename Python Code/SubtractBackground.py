#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !                                                                         !
# !         This file was added by Tyler Sterling on 08.04.2021             !
# !                                                                         !
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# system modules
import numpy as np
import matplotlib.pyplot as plt
import os

# custom modules. using import * might clash with namespace of system modules ...
from TextFile import *
from Data import *
from FittingFunction import *
from FittingData import *
from Display import *
from plotDataWithFit import *
from FitParameters import *
from GaussianSmooth import SmoothedBackground
from RSE_Constants import *

# -----------------------------------------------------------------------------------------------

# read the input file
params=Parameters(RSE_Constants.INPUTS_PATH,RSE_Constants.INPUTS_FILENAME)
params.ReadBackgroundParams()

# -----------------------------------------------------------------------------------------------

# get the background folders
folderForBkgSubtractedFiles=[subdir for subdir in os.listdir(params.path_data) if \
        subdir.startswith(RSE_Constants.GEN_FOLDER)]

Disp=Display() # initialize class to make the plots

# loop over the background folders
for i in range(0,len(folderForBkgSubtractedFiles)):

    folder=params.path_data+folderForBkgSubtractedFiles[i]+'/' # path of the folder to do in this iter.
    print('now in folder',folder)

    # get the files in this background folder
    files=[file for file in os.listdir(folder) if file.startswith(RSE_Constants.STARTS_WITH) \
            and not file.endswith(RSE_Constants.ENDS_WITH)] 

    # load the raw data
    rawFileName=folder[folder.index('_' + RSE_Constants.STARTS_WITH)+1:-1] # the Q point file
    
    # -------------------------------------------------------------------------------------------
    # load the bg files, smooth the data, find the background, and save everything

    # this class uses gaussian smoothing and interpolation to determine background
    smooth_bg = SmoothedBackground(folder)
    smooth_bg.smooth_cuts_for_this_Q(params,rawFileName) # get the smoothed bg, write the files, etc.

    # read the files, subtract the bg, and write the subtracted file to subtr_background
    smooth_bg.subtract_background(params,rawFileName)

    # -------------------------------------------------------------------------------------------
    # now go back and plot all the files

    # plot each file with its background 
    plot_with_smooth = PlotDataWithGaussianSmoothedBG(params,folder,files)

    # plot the bg cuts and the smoothed bg all in one plot. same as Background.DisplayAllFiles 
    smooth_bg.plot_all_in_one(params,rawFileName)

    # plot the raw file and the background
    smooth_bg.plot_raw_cut(params,rawFileName)

    # plot the subtracted background
    smooth_bg.plot_subtr_cut(params,rawFileName)

    # make a single file of all plots in the bg determination folder
    Disp.MakePlotSummary(folder,RSE_Constants.BACKGR_PREFIX+rawFileName)

# -----------------------------------------------------------------------------------------------
# now go and make the combined files for the raw Q and subtracted Q

# do it for raw Q in good_slices
Disp.MakePlotSummary(params.path_data,params.ProcessedDataName)

# do it for subtracted Q in subtr_background
Disp.MakePlotSummary(params.folderForBkgSubtractedFiles,params.ProcessedDataName)

# -----------------------------------------------------------------------------------------------

print('\n\tall done with the background determination!\n')









