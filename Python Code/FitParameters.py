#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%




import math
import numpy
from TextFile import *
from Data import *

class FitParameters:

    def __init__(self,fitResults,filenames):
        self.filenames=filenames
        self.pguess=fitResults


    def writeToFile(self,params,filename):
        ParamTxtFile=open(filename,'w')
        ParamTxtFile.write(str(self.pguess[1:3*params.NumberofPeaks:3]).strip('[]') + "\n"+ "\n")
        ParamTxtFile.write(str(self.pguess[2:3*params.NumberofPeaks:3]).strip('[]') + "\n"+ "\n")
        ParamTxtFile.write(self.filenames[0]+"\n")
        AmplitudeForFirstFile=self.pguess[0:3*params.NumberofPeaks:3]
        ParamTxtFile.write(str(AmplitudeForFirstFile).strip('[]') + "\n"+ "\n")
        for i in range (1,len(self.filenames)):
             ParamTxtFile.write(self.filenames[i] + "\n")
#             ParamTxtFile.write(str(self.pguess[(2+i)*self.NumberofPeaks:((3+i)*self.NumberofPeaks-1)]).strip('[]')) + "\n" + "\n")
             ParamTxtFile.write((str(self.pguess[(2+i)*params.NumberofPeaks:((3+i)*self.NumberofPeaks-1)]).strip('[]')) + "\n" + "\n")
        ParamTxtFile.close()

    def readFromFile(self,locationForOutputParam):
        self.locationForOutputParam=locationForOutputParam
#        print(self.locationForOutputParam+self.filenames[0])
        with open(self.locationForOutputParam+self.filenames[0]) as f:
            parameters = f.read().splitlines()
        lineIndex, self.p = self.ReadExtendedLine(0,parameters)

        self.NumberofPeaks=len(self.p)
        lineIndex, self.w= self.ReadExtendedLine(lineIndex+1,parameters)
#        self.Q=[[0,0,0],[0,0,0]]
        lineIndex=lineIndex+1
        Data=DataSmall_q(" "," ")
        dataFileName=parameters[lineIndex]
        self.Q=[Data.ExtractQfromFileName(dataFileName)]
        self.dataFileNames=[dataFileName]
        lineIndex, Amp = self.ReadExtendedLine(lineIndex+1,parameters)
        self.Amp=[[float(i) for i in Amp]]
        self.NumberofDatasets=0
        try:
#        if 1==1:
            for indx in range (0,1000):
                lineIndex=lineIndex+1
                dataFileName=parameters[lineIndex]
                self.Q=numpy.append(self.Q,[Data.ExtractQfromFileName(dataFileName)],axis=0)
                self.dataFileNames=numpy.append(self.dataFileNames,[dataFileName])
                lineIndex, Amp = self.ReadExtendedLine(lineIndex+1,parameters)
                self.Amp=numpy.append(self.Amp,[[float(i) for i in Amp]], axis=0)
                self.NumberofDatasets=self.NumberofDatasets+1
        except:
                f.close()
        #read file and splitline
        #read positions
        #read widths
        #read Wavevectors
        #read amplitudes
        return

    def ReadExtendedLine(self,paramFileLineIndex,parameters):
        array=str.split(parameters[paramFileLineIndex])
        #print array
        while len(str.split(parameters[paramFileLineIndex]))>0:
            paramFileLineIndex=paramFileLineIndex+1
            arr=parameters[paramFileLineIndex].split()
            array.extend(arr)
        return paramFileLineIndex, array
    
class InitialGuesses(FitParameters):

    def __init__(self,params,data):
#        print(params.fileWithGuesses)
        #FitParameters.__init__(self,data,fitResults)
        self.filenames=data.filenames
        self.NumberofPeaks=params.NumberofPeaks
        self.NumberofDatasets=data.NumberofDatasets
        self.widths=numpy.zeros(self.NumberofPeaks)+params.InitWidthsFinal
        self.amplitudes=numpy.zeros(self.NumberofPeaks*self.NumberofDatasets)+params.InitAmplitudes
        self.positions=numpy.zeros(self.NumberofPeaks)+params.positionGuesses
        self.pguess=numpy.zeros(3*self.NumberofPeaks+self.NumberofPeaks*(self.NumberofDatasets-1))
        self.buildInitArray(self.NumberofPeaks,self.NumberofDatasets,self.positions)

 
    def buildInitArray(self,NumberofPeaks,NumberofDatasets,positions):
        
        for i in range (0,self.NumberofPeaks):
            self.pguess[3*i]=self.amplitudes[i]
            self.pguess[3*i+1]=self.positions[i]
            self.pguess[3*i+2]= self.widths[i]
        for i in range (3*self.NumberofPeaks,3*self.NumberofPeaks+self.NumberofPeaks*(self.NumberofDatasets-1)):
            self.pguess[i]=self.amplitudes[i-2*self.NumberofPeaks]
        #return

