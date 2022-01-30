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
#import matlab.engine
from RSE_Constants import *
from plotDataWithFit import *
from Display import *
import os

params=Parameters(RSE_Constants.INPUTS_PATH, RSE_Constants.INPUTS_FILENAME)
#print(params);

if params.QMode==0:
    dd=1
    testData=DataSmall_q(params, params.path_data)
if params.QMode==1:
    testData=CollectionOfQs(params)
print(params.path_data)
testData.Generate()
if params.BkgMode==0:
    plot=Plot(params)
    plot.Plot()
    Disp=Display()
    Disp.MakePlotSummary(params.path_data,params.ProcessedDataName)

print("line 21, explore")
if params.BkgMode==1:
    RSE_Constants.FLAG=0
    BackgroundFiles=DataBackgroundQs(params)
    print("line 23, explore")
    BackgroundFiles.GenerateAllFiles()
    print("line 25, explore")



