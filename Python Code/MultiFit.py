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
import re
import os
import math
from numpy import *
from FitParameters import *
from plotDataWithFit import *
import datetime
from RSE_Constants import *
from Display import *
print(datetime.datetime.now())

print("Parameters")
params=Parameters(RSE_Constants.INPUTS_PATH_MAIN,RSE_Constants.INPUTS_FILENAME_MAIN)
params.ReadMultizoneFitParams()
params.locationForOutputParam=params.folderForBkgSubtractedFiles

for i in range (0,len(params.positionGuessesList[:])):
    print("DataSmall_q")
    print(params.reducedQlist[i:i+1])
    if len(params.reducedQlist[i:i+1])==0:
        data=DataSmall_q(params,params.folderForBkgSubtractedFiles)
#        params.qh=1000  #1000 means that reduced q is not specified
#        params.qk=1000
#        params.ql=1000
        paramFileName='_'+RSE_Constants.FITTING_PARAM_FILE

    else:
#        print(params.SmallqAlgorithm)
        data=DataSmall_q(params,params.folderForBkgSubtractedFiles,params.reducedQlist[i:i+1][0])
        params.qh=params.reducedQlist[i:i+1][0][0]
        params.qk=params.reducedQlist[i:i+1][0][1]
        params.ql=params.reducedQlist[i:i+1][0][2]
        paramFileName='_'+RSE_Constants.FITTING_PARAM_FILE+'_'+str(params.qh)+'_'+str(params.qk)+'_'+str(params.ql)+'.txt'

    data.Read()
    print("InitialGuesses")
    params.positionGuesses=params.positionGuessesList[i]
    params.NumberofPeaks=len(params.positionGuesses)
    InitialGuesses=InitialGuesses(params,data)

    print("Fitting")
    Fitting=FittingData(params,InitialGuesses,data)

    popt, pcov=Fitting.doFitting()

    WriteToText=FitParameters(popt,data.filenames)
    WriteToText.writeToFile(params,params.locationForOutputParam+paramFileName+'.txt')
    
    WriteToText=FitParameters(numpy.sqrt(numpy.diag(pcov)),data.filenames)
    WriteToText.writeToFile(params,params.locationForOutputParam+'err'+paramFileName+'.txt')

#    WriteToText=WriteFinalParamToFile(params,data)

 #   WriteToText.writeToFile(params.locationForOutputParam,paramFileName,popt)
 #   WriteToText.writeToFile(params.locationForOutputParam,"err"+paramFileName,numpy.sqrt(numpy.diag(pcov)))
    folder=params.locationForOutputParam
    PlotDataWithFitting=PlotDataWithFitParamCustomFolder(params,folder,folder,folder)
    Disp=Display()
    from FitParameters import *
Disp.MakePlotSummary(params.folderForBkgSubtractedFiles,params.ProcessedDataName)

print(datetime.datetime.now())

