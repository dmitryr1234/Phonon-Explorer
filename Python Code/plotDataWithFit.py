#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%




import numpy
from TextFile import *
from Data import *
from FitParameters import *
import matplotlib.pyplot as plt

class Plot:
    def __init__(self,maxY,directory):
        self.location_ForPlots=directory
        self.dataDirectory=directory
        self.maxY=maxY
        
    def Plot(self):
        dataFileNames=[file for file in os.listdir(self.dataDirectory) if file.startswith("H") and not file.endswith("pdf")]
        for i in range (0,len(dataFileNames)):
            data=Dataset(self.dataDirectory,[dataFileNames[i]])
            plt.errorbar(data.Energy, data.Intensity, data.Error,fmt='o')
            plt.xlabel('Energy')
            plt.ylabel('Intensity')
            plt.title(dataFileNames[i])#+" dh="+str(params.Deltah))
            plt.ylim((-0.1*self.maxY,self.maxY)) 
            plt.grid() 
            plt.savefig(self.dataDirectory+dataFileNames[i]+'.pdf')
                #plt.show()
            plt.close()    

class PlotDataWithFitParam:
    def __init__(self,params):
        self.location_ForPlots=params.location_ForPlots
        self.locationForOutputParam=params.locationForOutputParam
        self.dataDirectory=params.path_data
        self.ParamFileNames=['_FittingParam.txt']
        self.InitCommon(params)


    def InitCommon(self,params):
        self.NumberofPeaks=params.NumberofPeaks
#        self.DataFileNames = [file for file in os.listdir(self.dataDirectory) if file.startswith("H")]
#        self.NumberofDatasets = len(self.DataFileNames)
        #self.fittingFunctionForplot()
        #self.ReadExtendedLine(firstLine,parameters)
        self.maxY=params.maxY
        self.params=params
        self.ReadAndPlot()  

    def ReadAndPlot(self):

        for iParamFile in range(0,len(self.ParamFileNames)):
            filename=self.ParamFileNames[iParamFile]
            fitResults=FitParameters(0,[filename])
            fitResults.readFromFile(self.locationForOutputParam)
            for indx in range (0,len(fitResults.dataFileNames)):
                try:
                    data=Dataset(self.dataDirectory,[fitResults.dataFileNames[indx]])  
                    self.func=numpy.zeros(len(data.Energy))
                    FitResultsArray=[]
                    FitResultsArray.append(data.Energy)
                    for i in range (0,fitResults.NumberofPeaks):
                        peak=float(fitResults.Amp[indx][i])/float(fitResults.w[i])*numpy.exp(-(numpy.power(((data.Energy-float(fitResults.p[i]))/float(fitResults.w[i])),2)))
                        self.func=self.func+peak
                        plt.plot(data.Energy, peak, 'b-', label='fit')
                        FitResultsArray.append(peak)
                    FitResultsArray.append(self.func)
                    numpy.savetxt(self.dataDirectory+"fit"+fitResults.dataFileNames[indx],numpy.transpose(FitResultsArray), fmt="%5.2e")
                    plt.errorbar(data.Energy, data.Intensity, data.Error, fmt='o')
                    plt.plot(data.Energy, self.func, 'r-', label='fit')
                    plt.xlabel('Energy')
                    plt.ylabel('Intensity')
                    plt.title(fitResults.dataFileNames[indx]+" dH="+str(self.params.Deltah)+ " dK="+str(self.params.Deltak)+" dL="+str(self.params.Deltal))
                    plt.ylim((-0.1*self.maxY,self.maxY)) 
                    plt.grid() 
                    plt.savefig(self.location_ForPlots+fitResults.dataFileNames[indx]+'.pdf')
                    #plt.show()
                    plt.close()
                except:
                    d=0   #dummy


class PlotDataWithFitParamCustomFolder(PlotDataWithFitParam):  
    def __init__(self,params,location_ForPlots,locationForOutputParam,dataDirectory):
        self.location_ForPlots=location_ForPlots
        self.locationForOutputParam=locationForOutputParam
        self.dataDirectory=dataDirectory
#        self.paramFileName=paramFileName
#        self.DataFileNames=[file for file in os.listdir(self.dataDirectory) if file.startswith("H") and not file.endswith("pdf")]
        self.ParamFileNames=[file for file in os.listdir(self.dataDirectory) if file.startswith("_") and not file.endswith("pdf")]
        self.InitCommon(params)
#        self.ReadAndPlot()  

           
