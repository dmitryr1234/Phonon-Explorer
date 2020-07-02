#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%




from TextFile import *
from Data import *
from FittingFunction import *
from FittingData import *
from Display import *
import re
import os
import math
import time
from numpy import *
from plotDataWithFit import *
from FitParameters import *
from Background import *
import matplotlib.pyplot as plt
from RSE_Constants import *

params=Parameters(RSE_Constants.INPUTS_PATH,RSE_Constants.INPUTS_FILENAME)
params.ReadBackgroundParams()

folderForBkgSubtractedFiles=[subdir for subdir in os.listdir(params.path_data) if subdir.startswith(RSE_Constants.BACKGROUND_SUBTRACTED_FOLDER)]
#print(folderForBkgSubtractedFiles)
#print(os.listdir(params.path_data))
#print(len(folderForBkgSubtractedFiles))
#print(params.path_data)
Disp=Display()
for i in range (0,len(folderForBkgSubtractedFiles)):
    folder=params.path_data+folderForBkgSubtractedFiles[i]+'/'
    print(folder)
    files=[file for file in os.listdir(folder) if file.startswith(RSE_Constants.STARTS_WITH) and not file.endswith(RSE_Constants.ENDS_WITH)] 
    rawFileName=folder[folder.index('_' + RSE_Constants.STARTS_WITH)+1:-1]
#    print(rawFileName)
    rawData=Dataset(params.path_data,[rawFileName])
#    print(rawData.Intensity)
    for j in range (0,len(files)):
        try:
#        if 1==1: 
            Fitting=FittingBackgroundData(params,folder,files[j])
            popt, pcov=Fitting.doFitting()
            data=Dataset(folder,[files[j]])
#            WriteToText=WriteFinalParamToFile(params,data)
#            WriteToText.writeToFile(folder,files[j],popt)
            WriteToText=FitParameters(popt,data.filenames)
            WriteToText.writeToFile(params,folder+'_'+files[j]+'.txt')
        except Exception as e:
            print("fit failed:"+folder+" "+files[j])
            print(e)
#            time.sleep(5)
 
    PlotDataWithFitting=PlotDataWithFitParamCustomFolder(params,folder,folder,folder)
    Backgr=Background(params,folder,rawData)
    Backgr.DisplayAllFiles(folder,folder,rawFileName)
    Backgr.DisplayOrigFile(params.path_data,params.location_ForPlots,rawFileName)
    Disp.MakePlotSummary(folder,RSE_Constants.BACKGR_PREFIX+rawFileName) #Make single PDF of all plots in the background folder
Disp.MakePlotSummary(params.path_data,params.ProcessedDataName)
#Backgr.Adjust(rawFileName,params.folderForBkgSubtractedFiles)
Disp.MakePlotSummary(params.folderForBkgSubtractedFiles,params.ProcessedDataName)




