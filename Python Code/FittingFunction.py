#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


from TextFile import *
from FitParameters import *

class FittingFunction:

    def __init__(self,InitialGuesses):
        self.NumberofPeaks=InitialGuesses.NumberofPeaks
        self.NumberofDatasets=InitialGuesses.NumberofDatasets
        self.buildfittingFunction()
        self.buildfittingFunctionDeclaration()
        
    def buildfittingFunction(self):
        self.char_funct='' 
        add=''
        for m in range (1, self.NumberofPeaks+1):      
            delimiter=''
            if m > 1:
               delimiter='+'
            AmplitudeIndex=str(3*(m-1)+1)
            PositionIndex=str(3*(m-1)+2)
            WidthIndex=str(3*(m-1)+3) #Amplitude is actually Integrated Intensity
            self.char_funct=self.char_funct+delimiter+'(p'+AmplitudeIndex+'/p'+WidthIndex+')*numpy.exp(-(numpy.power(((Energy-p'+PositionIndex+')/p'+WidthIndex+'),2)))'
        
        i=0        
        for n in range(1,self.NumberofDatasets):
            shift=100*(n) 
            s_shift=str(shift)
            for m in range(0,self.NumberofPeaks):
                i=i+1
                AmplitudeIndex=str(3*self.NumberofPeaks+i)
                PositionIndex=str(3*(m)+2)
                WidthIndex=str(3*(m)+3)
                self.char_funct=self.char_funct + '+ p'+AmplitudeIndex+'*numpy.exp(-(numpy.power(((Energy-p'+PositionIndex+'-'+s_shift+')/p'+WidthIndex+'),2)))'
      
    def buildfittingFunctionDeclaration(self):
        i=0 
        self.fittingFunctionDeclaration='self,Energy'
        for m in range (1,self.NumberofPeaks+1):      
            AmplitudeIndex=str(3*(m-1)+1)
            PositionIndex=str(3*(m-1)+2)
            WidthIndex=str(3*(m-1)+3)
            self.fittingFunctionDeclaration=self.fittingFunctionDeclaration+',p'+AmplitudeIndex+',p'+PositionIndex+',p'+WidthIndex
            
        for n in range(1,self.NumberofDatasets):
            for m in range (0, self.NumberofPeaks):
                i=i+1
                self.fittingFunctionDeclaration=self.fittingFunctionDeclaration+',p'+str(3*self.NumberofPeaks+i)
        #self.fittingFunctionDeclaration=self.fittingFunctionDeclaration+'):'

        
