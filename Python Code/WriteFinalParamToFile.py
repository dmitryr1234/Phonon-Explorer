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

class WriteFinalParamToFile:

    def __init__(self,params,data):
        self.files=data.filenames
        self.NumberofPeaks=params.NumberofPeaks

        
    def writeToFile(self,filename,fitParams):
        ParamTxtFile=open(filename,'w')
        ParamTxtFile.write(str(fitParams[1:3*self.NumberofPeaks:3]).strip('[]') + "\n"+ "\n")
        ParamTxtFile.write(str(fitParams[2:3*self.NumberofPeaks:3]).strip('[]') + "\n"+ "\n")
        ParamTxtFile.write(self.files[0] + "\n")
        ParamTxtFile.write(str(fitParams[0:3*self.NumberofPeaks-1:3]).strip('[]') + "\n"+ "\n")
        #ParamTxtFile.write(self.filenames[0]+ "\n")

        for i in range (1,len(self.files)):
            ParamTxtFile.write(self.files[i] + "\n")
            ParamTxtFile.write((str(fitParams[((2+i)*self.NumberofPeaks):((3+i)*self.NumberofPeaks):1]).strip('[]')) + "\n" + "\n")
        
        ParamTxtFile.close() 

