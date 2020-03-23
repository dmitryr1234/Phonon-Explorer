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
from WriteFinalParamToFile import *
from plotDataWithFit import *
import datetime
from RSE_Constants import *
from Display import *
print(datetime.datetime.now())

print("Parameters")
params=Parameters(RSE_Constants.INPUTS_PATH_MAIN,RSE_Constants.INPUTS_FILENAME_MAIN)
params.ReadMultizoneFitParams()
params.locationForOutputParam=params.folderForBkgSubtractedFiles
print("DataSmall_q")
data=DataSmall_q(params,params.folderForBkgSubtractedFiles)

data.Read()
print("InitialGuesses")

InitialGuesses=InitialGuesses(params,data)

print("Fitting")
Fitting=FittingData(params,InitialGuesses,data)

popt, pcov=Fitting.doFitting()


WriteToText=WriteFinalParamToFile(params,data)

WriteToText.writeToFile(params.locationForOutputParam+RSE_Constants.FITTING_PARAM_FILE,popt)
WriteToText.writeToFile(params.locationForOutputParam+"err"+RSE_Constants.FITTING_PARAM_FILE,numpy.sqrt(numpy.diag(pcov)))
folder=params.locationForOutputParam
PlotDataWithFitting=PlotDataWithFitParamCustomFolder(params,folder,folder,folder)
Disp=Display()
Disp.MakePlotSummary(params.folderForBkgSubtractedFiles,params.ProcessedDataName)

print(datetime.datetime.now())

