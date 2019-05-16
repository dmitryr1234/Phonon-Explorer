#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


import sys
from TextFile import *
from Data import *
from FittingFunction import *
from FitParameters import *
from scipy.optimize import curve_fit
import scipy.optimize as optimization
import matplotlib.pyplot as plt
from numpy import *
from RSE_Constants import *

class FittingData():
   
    def __init__(self,params,InitialGuesses,data):

        self.NumberofIter=params.NumberofFitIter
        self.tempFileDir=params.path_InputFiles
        self.InitialGuesses=InitialGuesses.pguess  
        self.NumberofPeaks=InitialGuesses.NumberofPeaks
        self.NumberofDatasets=InitialGuesses.NumberofDatasets
        self.FittingFunction=FittingFunction(InitialGuesses)
        self.Energy=data.Energy
        self.Intensity=data.Intensity
        self.Error=data.Error
        self.positionGuesses=params.positionGuesses
        self.WidthLowerBound=params.WidthLowerBound
        self.e_step=params.e_step
        self.NumberofParam=self.NumberofPeaks*3+self.NumberofPeaks*(self.NumberofDatasets-1)
             
    def doFitting(self):
#        print(self.positionGuesses)
#        tempFile=self.tempFileDir+RSE_Constants.TEMP_FILE
        tempFile=self.tempFileDir+"guru99.py"
        f= open(tempFile,"w+")
        f.write("import numpy" + "\n")
        f.write("class FitFuncTemp:" + "\n")
        f.write("    def func1("+self.FittingFunction.fittingFunctionDeclaration+"):"+ "\n")
        f.write("        return "+self.FittingFunction.char_funct)
        f.close()

        sys.path.append(self.tempFileDir)
        from guru99 import FitFuncTemp
        ff=FitFuncTemp()

        LB=numpy.zeros(self.NumberofParam)
        UB=numpy.zeros(self.NumberofParam)
        PositionDelta=0.1*self.positionGuesses[self.NumberofPeaks-1]
        
        for i in range (0,self.NumberofParam):
            LB[i]=0
            UB[i]=numpy.inf   
        
        for ii in range (0,self.NumberofPeaks):
            LB[3*ii+2]=self.WidthLowerBound #Low bound of the widths must change with each experiment
            UB[3*ii+2]=self.WidthLowerBound*7
            LB[3*ii+1]=self.InitialGuesses[3*ii+1]-PositionDelta
            UB[3*ii+1]=self.InitialGuesses[3*ii+1]+PositionDelta

        
#        UB[0]=0.023
            
#        UB[1]=self.InitialGuesses[1]+0.1
#        LB[1]=self.InitialGuesses[1]-0.1
        param_bounds=(LB,UB)
        for ind in range (1,self.NumberofIter):             
#            popt, pcov = curve_fit(ff.func1, self.Energy, self.Intensity, p0=self.InitialGuesses,bounds=param_bounds,maxfev=100000)
            popt, pcov = curve_fit(ff.func1, self.Energy, self.Intensity,sigma=self.Error, p0=self.InitialGuesses,bounds=param_bounds,xtol=5e-8,maxfev=2000)
        del sys.modules['guru99']
        return popt, pcov

class FittingDataFromFile(FittingData):
    def __init__(self,params,InitialGuesses,folder,datafile):
        FittingData(params,InitialGuesses,DataTextFile(folder,datafile))

class FittingBackgroundData(FittingData):
    def __init__(self,params,folder,datafile):
        data=Dataset(folder,[datafile])
        firstEnergyIndex=0
        lastEnergyIndex=len(data.Energy)-1
#        print(params.Resolution, params.e_step,0.8*params.Resolution/params.e_step)
#        print(data.Energy[firstEnergyIndex:lastEnergyIndex:int(0.8*params.Resolution/params.e_step)])
        positions=data.Energy[firstEnergyIndex:lastEnergyIndex:int(params.Resolution/params.e_step)]
#        print(positions)
#        print([data.Energy[lastEnergyIndex]])
        if positions[len(positions)-1]<data.Energy[lastEnergyIndex]:
            positions=numpy.append(positions,[data.Energy[lastEnergyIndex]])
#        print(positions)
        params.positionGuesses=positions
        params.NumberofPeaks=len(positions)
        params.InitWidthsFinal=params.MinPeakWidthForSmoothing
        params.WidthLowerBound=params.MinPeakWidthForSmoothing
        InitGuess=InitialGuesses(params,data)
                
        FittingData.__init__(self,params,InitGuess,data)

