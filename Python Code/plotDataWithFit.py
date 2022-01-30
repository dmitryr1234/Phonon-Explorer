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
from RSE_Constants import *
from FitParameters import *
import matplotlib.pyplot as plt

class Plot:
    def __init__(self,params):
        self.location_ForPlots=params.path_data
        self.dataDirectory=params.path_data
        self.params=params
        
    def Plot(self):
        dataFileNames=[file for file in sorted(os.listdir(self.dataDirectory)) if file.startswith("H") and not file.endswith("pdf")]
        for i in range (0,len(dataFileNames)):
            data=Dataset(self.dataDirectory,[dataFileNames[i]])
            self.plotDataset(data,0)
    def plotDataset(self,data,indx,fitResults=0):
        if fitResults==0:
            self.plotSingle(self.dataDirectory,self.dataDirectory,[data.filenames[indx]])        
        else:
            FitResultsArray=self.getFitResultsArray(fitResults,data.Energy,indx)
            numpy.savetxt(self.dataDirectory+'fit'+data.filenames[0],FitResultsArray)
            self.plotSingle(self.dataDirectory,self.dataDirectory,data.filenames,FitResultsArray)
        return

    def plotSingle(self,folder,plotsFolder,filenames,FitResultsArray=0,title=0):
        for i in range(0,len(filenames)):
            try:
                data=Dataset(folder,[filenames[i]])
            except:
                data=Dataset(folder,filenames[i])
            plt.errorbar(data.Energy, data.Intensity, data.Error,fmt=RSE_Constants.SYMBOL[i])
#        print(len(FitResultsArray))
        if FitResultsArray!=0:
            lineColor='b-'
            for i in range(1,len(FitResultsArray)-1):
                plt.plot(FitResultsArray[0], FitResultsArray[i], 'b-', label='fit')
                lineColor='r-'
            plt.plot(FitResultsArray[0], FitResultsArray[len(FitResultsArray)-1], lineColor, label='fit',linewidth=4.0)
        plt.xlabel(RSE_Constants.X_LABEL)
        plt.ylabel(RSE_Constants.Y_LABEL)
        self.titleApend=" dH="+str(self.params.Deltah)+ " dK="+str(self.params.Deltak)+" dL="+str(self.params.Deltal)
        plt.ylim((-0.1*self.params.maxY,self.params.maxY)) 
        plt.grid()
        if title==0:
            title=filenames[0]
        plt.title(title+self.titleApend)
        plt.savefig(plotsFolder+title+'.pdf')
        plt.close()

    def getFitResultsArray(self,fitResults, Energy,indx):
        self.func=numpy.zeros(len(Energy))
        FitResultsArray=[]
        FitResultsArray.append(Energy)
        for i in range (0,fitResults.NumberofPeaks):
            peak=float(fitResults.Amp[indx][i])/float(fitResults.w[i])*numpy.exp(-(numpy.power(((Energy-float(fitResults.p[i]))/float(fitResults.w[i])),2)))
            self.func=self.func+peak
            FitResultsArray.append(peak)
        FitResultsArray.append(self.func)
  
        return FitResultsArray
    
class PlotDataWithFitParam(Plot):
    def __init__(self,params):
        self.location_ForPlots=params.location_ForPlots
        self.locationForOutputParam=params.locationForOutputParam
        self.dataDirectory=params.path_data
        self.ParamFileNames=['_FittingParam.txt']
        self.ParamErrFileNames=['err_FittingParam.txt']
        self.InitCommon(params)
        Plot.__init__(params.maxY,self.dataDirectory)

    def InitCommon(self,params):
        self.NumberofPeaks=params.NumberofPeaks
#        self.DataFileNames = [file for file in os.listdir(self.dataDirectory) if file.startswith("H")]
#        self.NumberofDatasets = len(self.DataFileNames)
        #self.fittingFunctionForplot()
        #self.ReadExtendedLine(firstLine,parameters)
        self.maxY=params.maxY
        self.params=params
        self.ReadAndPlot()
        
#Also save all positions and all widths to the same files for all q
        
    def ReadAndPlot(self):
        p=open(os.path.join(self.locationForOutputParam,"Positions.txt"),'w')
        w=open(os.path.join(self.locationForOutputParam,"Widths.txt"),'w')
        for iParamFile in range(0,len(self.ParamFileNames)):
            #if 1==1:

            filename=self.ParamFileNames[iParamFile]
            fitResults=FitParameters(0,[filename])
            fitResults.readFromFile(self.locationForOutputParam)
#            print(fitResults.p)
            try:
                err_filename=self.ParamErrFileNames[iParamFile]
                err_fitResults=FitParameters(0,[err_filename])
                err_fitResults.readFromFile(self.locationForOutputParam)
                p.write(filename+',')
                w.write(filename+',')
                pString=''
                wString=''
                for i in range(0,len(fitResults.p)):
                    pString=pString+str(fitResults.p[i])+','+str(err_fitResults.p[i])+','
                    wString=wString+str(fitResults.w[i])+','+str(err_fitResults.w[i])+','
                p.write(pString+'\n')
                w.write(wString+'\n')
            except:
                dd=1   #dummy statement
            
            for indx in range (0,len(fitResults.dataFileNames)):
                if 1==1:
#                try:
                    data=Dataset(self.dataDirectory,[fitResults.dataFileNames[indx]])
#                    print(fitResults.dataFileNames[indx])
                    self.plotDataset(data,indx,fitResults)
#                except:
#                    d=0   #dummy


class PlotDataWithFitParamCustomFolder(PlotDataWithFitParam):  
    def __init__(self,params,location_ForPlots,locationForOutputParam,dataDirectory):
        self.location_ForPlots=location_ForPlots
        self.locationForOutputParam=locationForOutputParam
        self.dataDirectory=dataDirectory
#        self.paramFileName=paramFileName
#        self.DataFileNames=[file for file in os.listdir(self.dataDirectory) if file.startswith("H") and not file.endswith("pdf")]
        self.ParamFileNames=[file for file in sorted(os.listdir(self.dataDirectory)) if file.startswith("_") and not file.endswith("pdf")]
        self.ParamErrFileNames=[file for file in sorted(os.listdir(self.dataDirectory)) if file.startswith("err_") and not file.endswith("pdf")]
        self.InitCommon(params)
#        self.ReadAndPlot()  

# -----------------------------------------------------------------------------------------

class PlotDataWithGaussianSmoothedBG(Plot):

    """
    this class was added by Tyler Sterling on 08.04.2021
    """

    def __init__(self,params,bg_folder,bg_files):

        """
        read the smoothed bg for a given file and plot it + its background.
        """

        self.params = params

        for bg_file in bg_files:

            smooth_file = os.path.join(bg_folder,RSE_Constants.SMOOTHED_STARTS_WITH+bg_file)
            smooth_data = np.loadtxt(smooth_file)
            smooth_array = []
            smooth_array.append(smooth_data[:,0]) # bg energy grid
            smooth_array.append(smooth_data[:,1]) # bg intensity values

            self.plotSingle(bg_folder,bg_folder,[bg_file],smooth_array,bg_file)

# -----------------------------------------------------------------------------------------

