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
from WriteFinalParamToFile import *
from plotDataWithFit import *
from Background import *
import matplotlib.pyplot as plt
from RSE_Constants import *

params=Parameters(RSE_Constants.INPUTS_PATH,RSE_Constants.INPUTS_FILENAME)
params.ReadBackgroundParams()

folderForBkgSubtractedFiles=[subdir for subdir in os.listdir(params.path_data) if subdir.startswith(RSE_Constants.BACKGROUND_SUBTRACTED_FOLDER)]
#print(folderForBkgSubtractedFiles)
#print(os.listdir(params.path_data))
#print(len(folderForBkgSubtractedFiles))
plt.figure(figsize=(8.27,11.69,))

plt.xlabel(RSE_Constants.X_LABEL)
plt.ylabel(RSE_Constants.Y_LABEL)
plt.ylim((0,0.0005)) 
plt.grid()
#print(params.path_data)
Disp=Display()
for i in range (0,len(folderForBkgSubtractedFiles)):
    folder=params.path_data+folderForBkgSubtractedFiles[i]+'/'
    print(folder)
    files=[file for file in os.listdir(folder) if file.startswith(RSE_Constants.STARTS_WITH) and not file.endswith(RSE_Constants.ENDS_WITH)] 
    rawFileName=folder[folder.index('_' + RSE_Constants.STARTS_WITH)+1:-1]
#    print(rawFileName)
    rawData=Dataset(params.path_data,[rawFileName])
    for j in range (0,len(files)):
        try:
#        if 1==1:
            Fitting=FittingBackgroundData(params,folder,files[j])
            popt, pcov=Fitting.doFitting()
            data=Dataset(folder,[files[j]])
            WriteToText=WriteFinalParamToFile(params,data)
            WriteToText.writeToFile(folder+'_'+files[j]+'.txt',popt)
        except Exception as e:
            print("fit failed:"+folder+" "+files[j])
            print(e)
#            time.sleep(5)

    PlotDataWithFitting=PlotDataWithFitParamCustomFolder(params,folder,folder,folder)
    Backgr=Background(params,folder)
    Backgr.DisplayAllFiles(folder,params.location_ForPlots,rawFileName)
    Backgr.Save(params.path_data,RSE_Constants.BACKGR_PREFIX+rawFileName)
    Backgr.DisplayOrigFile(params.path_data,params.location_ForPlots,rawFileName)
    Backgr.Subtract(params,rawData,rawFileName)

    Disp.MakePlotSummary(folder,RSE_Constants.BACKGR_PREFIX+rawFileName) #Make single PDF of all plots in the background folder
Disp.MakePlotSummary(params.path_data,params.ProcessedDataName)
#Backgr.Adjust(params.folderForBkgSubtractedFiles)
Disp.MakePlotSummary(params.folderForBkgSubtractedFiles,params.ProcessedDataName)

files=[file for file in os.listdir(params.path_data) if file.startswith("B_") and not file.endswith("pdf")]
colors=['red', 'black', 'blue', 'brown', 'green', 'orange']
for j in range (0,len(files)):
    try:
        data=np.genfromtxt(params.path_data+files[j])
        energy=data[:,][:,0]
        intensity=data[:,][:,1] 
        plt.plot(energy, intensity, colors[j], label='fit',linewidth=1.0)
    except:
        d=0 #dummy
#plt.title(rawFileName)
#plt.errorbar(rawData.Energy, rawData.Intensity, rawData.Error, fmt='o')
#plt.savefig(params.path_data+'_B_'+rawFileName+'.pdf')
#plt.close()



