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
from plotDataWithFit import *
from RSE_Constants import *
from FitParameters import *

class Background():
    def __init__(self,params,folder,rawData):
               
        self.params=params
        self.backgroundEnergy=rawData.Energy
#        print(folder)
#        os.listdir(folder)
        self.FitFileNames=[file for file in os.listdir(folder) if file.startswith("fit")]

        if len(self.FitFileNames)==1:
            self.backgroundIntensity=[0]*len(rawData.Energy)
            intensityAfterSubtractedBackground=[0]*len(rawData.Energy)
        else:

            self.backgroundIntensity=[10000000000]*len(rawData.Energy)
            intensityAfterSubtractedBackground=[0]*len(rawData.Energy)

            FitEnergy=[]
            FitIntensity=[]
            for iFile in range(0,len(self.FitFileNames)):
                FitData=genfromtxt(folder+self.FitFileNames[iFile])
                FitEnergy.append(FitData[0])
                FitIntensity.append(FitData[len(FitData)-1])

            for iFile in range(0,len(self.FitFileNames)):
                intens=FitIntensity[iFile]
                energy=FitEnergy[iFile]
                for iEng in range(0,len(self.backgroundEnergy)):            
                    try:
                        newInt=intens[list(energy).index(self.backgroundEnergy[iEng])]
                        self.backgroundIntensity[iEng]=min(self.backgroundIntensity[iEng],newInt)
                    except:
                        dd=0  #dummy

        self.Save(params.path_data,RSE_Constants.BACKGR_PREFIX+rawData.filenames[0])

        if not os.path.exists(params.folderForBkgSubtractedFiles):
            os.makedirs(params.folderForBkgSubtractedFiles)

        offset=self.AutomaticAdjustForConst(params,folder,rawData)
        for iEng in range(0,len(self.backgroundEnergy)):
            intensityAfterSubtractedBackground[iEng]=rawData.Intensity[iEng]-self.backgroundIntensity[iEng]-1.3*offset
#            print(rawData.Intensity[iEng],intensityAfterSubtractedBackground[iEng])
        
        FileafterBckgrdSubtr=open(params.folderForBkgSubtractedFiles+rawData.filenames[0],'w')

        for i in range (0,len(rawData.Energy)):
            FileafterBckgrdSubtr.write(str(rawData.Energy[i])+'  '+ str(intensityAfterSubtractedBackground[i])+ '  '+str(rawData.Error[i])+'\n')
        
        FileafterBckgrdSubtr.close()  
        
        dataWithFit=Plot(self.params)
        dataWithFit.plotSingle(params.folderForBkgSubtractedFiles,params.folderForBkgSubtractedFiles,rawData.filenames)

#        print(self.backgroundIntensity)
        return

        
    def CompareDataWithFit(self, data, funcEnergy, fit): #bug here. Not using
        diff=0
        sumData=0
        for i in range(0,len(funcEnergy)):
            if not numpy.isnan(data.Intensity[i]):
                diff=diff+self.func[i]-data.Intensity[i]
                sumData=sumData+data.Intensity[i]
#        print(diff/sumData)
    def CompareDataWithBackground(self):
            
        return
    def DisplayAllFiles(self,folder,plotsFolder,fileName):
#        plt.figure(figsize=(8.27,11.69,))
        dataWithFit=Plot(self.params)
        backgroundArray=[]
        backgroundArray.append(self.backgroundEnergy)
        backgroundArray.append(self.backgroundIntensity)
        files=[file for file in os.listdir(folder) if file.startswith("H") and not file.endswith("pdf")]
        dataWithFit.plotSingle(folder,plotsFolder,files,backgroundArray,fileName+'_all')
        return
    
    def Save(self,folder,filename):
#        print(folder,filename)
        if self.backgroundEnergy[0]==numpy.nan:
            print("No background for " + filename)
            return
        bkgTxtFile=FitTextFile(folder,filename)
        backgroundArray=[]
        backgroundArray.append(self.backgroundEnergy)
        backgroundArray.append(self.backgroundIntensity)

        bkgTxtFile.Write(backgroundArray)
        
    def DisplayOrigFile(self,folder,plotsFolder,fileName):
        dataWithFit=Plot(self.params)
        backgroundArray=[]
        backgroundArray.append(self.backgroundEnergy)
        backgroundArray.append(self.backgroundIntensity)
        dataWithFit.plotSingle(folder,folder,[fileName],backgroundArray)
        return


    def AutomaticAdjustForConst(self,params,folder,rawData):
        
#        print(rawData.dataDirectory,'  here')
#        print(folder)
        smoothedData=np.genfromtxt(folder+'fit'+rawData.filenames[0])
        smoothedDataEnergy=smoothedData[0]
        smoothedDataIntensity=smoothedData[len(smoothedData)-1]
        bkgData=np.genfromtxt(rawData.dataDirectory+'B_'+rawData.filenames[0])
        bkgDataEnergy=bkgData[0]
        bkgDataIntensity=bkgData[1]
        diff = []
        for j in range(0,len(smoothedDataEnergy)):
#            if 1==1:
            try:
                diff.append(smoothedDataIntensity[j]-bkgDataIntensity[list(bkgDataEnergy).index(smoothedDataEnergy[j])])
            except:
                dd=0
        offset=min(diff)
        print(offset)
        plt.plot(smoothedDataEnergy, smoothedDataIntensity, 'b-', label='fit',linewidth=1.0)
        plt.plot(bkgDataEnergy, bkgDataIntensity, 'r-', label='fit',linewidth=1.0)
        plt.xlabel(RSE_Constants.X_LABEL)
        plt.ylabel(RSE_Constants.Y_LABEL)
        plt.ylim((0,self.params.maxY)) 
        plt.grid()
        plt.title(rawData.filenames[0]+' offset '+str(offset))
        plt.savefig(folder+rawData.filenames[0]+'_test.pdf')
        plt.close()

        return offset
        
