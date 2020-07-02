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
    def __init__(self,params,folder):
               
        self.params=params
        self.func=numpy.zeros(1000)
#        print(folder)
#        os.listdir(folder)
        self.ParamFileNames=[file for file in os.listdir(folder) if file.startswith("_")]
        self.DataFileNames=[file for file in os.listdir(folder) if file.startswith("H") and not file.endswith("pdf") ]
        self.backgroundIntensity=[numpy.nan]
        self.backgroundEnergy=[numpy.nan]
        self.maxY=params.maxY
        print ('HERE')
        print(self.ParamFileNames)
        PlotDataWithFit=PlotDataWithFitParamCustomFolder(params,folder,folder,folder)
        for iParamFile in range (0,len(self.ParamFileNames)):            
            filename=self.ParamFileNames[iParamFile]
            fitResults=FitParameters(0,[filename])
            fitResults.readFromFile(folder)
            NumberofPeaks=len(fitResults.p)
            Offset=0#floor(params.Resolution/self.params.e_step)
#            print(folder+self.DataFileNames[iParamFile])
            data=Dataset(folder,[self.DataFileNames[iParamFile]])
            funcEnergyLength=int((data.Energy[len(data.Energy)-1]-data.Energy[0])/params.e_step-2*Offset+1)
            funcEnergy=numpy.zeros(funcEnergyLength)
            for i in range (0, funcEnergyLength):
                funcEnergy[i]=data.Energy[0]+Offset*params.e_step+i*params.e_step
            self.func=numpy.zeros(len(funcEnergy))
            for i in range (0,NumberofPeaks):
                peak=float(fitResults.Amp[0][i])/float(fitResults.w[i])*numpy.exp(-(numpy.power(((numpy.asarray(funcEnergy)-float(fitResults.p[i]))/float(fitResults.w[i])),2)))
                self.func=self.func+peak
#            self.CompareDataWithFit(data,funcEnergy,self.func)

            for i in range(0,len(funcEnergy)):
                j=numpy.argwhere(data.Energy==funcEnergy[i])
                if len(j)==0:
                    self.func[i]=99999
            
            self.Recalculate(funcEnergy)
          
# Truncate the background arrays to the right length, (max(ii))
        try:
            ii = [ii for ii, value in enumerate(self.backgroundIntensity) if value<90000]
            self.backgroundIntensity=self.backgroundIntensity[:max(ii)+1]
        except:
            print('No background files in ' + folder)
            return
        self.backgroundEnergy1=numpy.zeros(max(ii)+1)
        for i in range(0,max(ii)+1):
            if self.backgroundIntensity[i]>99000:
                self.backgroundIntensity[i]=numpy.nan                   
            self.backgroundEnergy1[i]=self.backgroundEnergy[0]+i*(self.params.e_step)
        self.backgroundEnergy=self.backgroundEnergy1
        
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
    
    def Recalculate(self,funcEnergy):

        i_shift=0
        if numpy.isnan(self.backgroundEnergy[0]):
             self.backgroundEnergy=funcEnergy
             self.backgroundIntensity=self.func
             return
# ajust Background array size on the low energy side if the new array starts at lower energy than the current background
        if funcEnergy[0]<self.backgroundEnergy[0]:
            for i in range(0,len(funcEnergy)):
                if funcEnergy[i]==self.backgroundEnergy[0]:
                    i_shift=i
            self.backgroundEnergy=numpy.lib.pad(self.backgroundEnergy,(0,i_shift+1),'minimum') #doesn't matter what values to pad with
            self.backgroundIntensity=numpy.lib.pad(self.backgroundIntensity,(i_shift+1,0),'constant',constant_values=(99000,0))

# Now repopulate self.backgroundEnergy
            for i in range(0,len(self.backgroundEnergy)):
                self.backgroundEnergy[i]=funcEnergy[0]+i*self.params.e_step
# Adjust the high energy end
        if funcEnergy[len(funcEnergy)-1]>self.backgroundEnergy[len(self.backgroundEnergy)-1]:
            j_shift=int((-self.backgroundEnergy[len(self.backgroundEnergy)-1]+funcEnergy[len(funcEnergy)-1])/self.params.e_step)
            self.backgroundEnergy=numpy.lib.pad(self.backgroundEnergy,(0,j_shift),'minimum') #doesn't matter what values to pad with
            self.backgroundIntensity=numpy.lib.pad(self.backgroundIntensity,(0,j_shift),'constant',constant_values=(0,99000))
            for i in range(0,len(self.backgroundEnergy)):
                self.backgroundEnergy[i]=self.backgroundEnergy[0]+i*self.params.e_step

# line up the new background array with the existing background 
        i_offset=0
        if funcEnergy[0]>self.backgroundEnergy[0]:
            i_offset=numpy.argwhere(self.backgroundEnergy==funcEnergy[0])
                    
# recalculate background intensity        
        for j in range (0,len(funcEnergy)):
            if self.backgroundIntensity[j+i_offset]>self.func[j]:
                self.backgroundIntensity[j+i_offset]=self.func[j]

                
    def DisplayAllFiles(self,folder,plotsFolder,fileName):
#        plt.figure(figsize=(8.27,11.69,))
        dataWithFit=Plot(self.params)
        backgroundArray=[]
        backgroundArray.append(self.backgroundEnergy)
        backgroundArray.append(self.backgroundIntensity)
        files=[file for file in os.listdir(folder) if file.startswith("H") and not file.endswith("pdf")]
        dataWithFit.plotSingle(folder,folder,files,backgroundArray,fileName)
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

    def Subtract(self,params,rawData,rawFileName,offset):

#find index in background data where raw data starts
        intensityAfterSubtractedBackground=numpy.zeros(len(rawData.Energy))
#        print(IndexOffset)
#        print(len(rawData.Energy),len(self.backgroundIntensity),len(rawData.Error))
#        print(rawData.Energy)
#        print(self.backgroundEnergy)
        try:
#        if (1==1):
            Qs=numpy.genfromtxt(params.folderForBkgSubtractedFiles+"BackgroundAdjustment.txt")
            QHlist=Qs[:,][:,0]
            QKlist=Qs[:,][:,1]
            QLlist=Qs[:,][:,2]
            Adjustments=Qs[:,][:,3]
            Q=rawData.ExtractQfromFileName(rawData.filenames[0])
            self.backgAdjustment=0
            for i in range(0,len(QHlist)):
                if (Q[0]==QHlist[i] and Q[1]==QKlist[i] and Q[2]==QLlist[i]):
                    self.backgAdjustment=Adjustments[i]
        except:
            self.backgAdjustment=0
        print ("Adjustment:", self.backgAdjustment)
        numPts=0
        try:
#        if 1==1:
            for i in range(0,len(rawData.Energy)):
                j=numpy.argwhere(self.backgroundEnergy==rawData.Energy[i])
#                print(j,self.backgroundIntensity[j])
                intensityAfterSubtractedBackground[i]=rawData.Intensity[i]-self.backgroundIntensity[j]-self.backgAdjustment
                numPts=numPts+1
        except: 
            d=0   #dummy line
#        print(range(numPts,len(rawData.Energy)))
#  trim to size where background has been calculated
        intensityAfterSubtractedBackground=numpy.delete(intensityAfterSubtractedBackground,range(numPts,len(rawData.Energy)))
        rawData.Energy=numpy.delete(rawData.Energy,range(numPts,len(rawData.Energy)))
        rawData.Error=numpy.delete(rawData.Error,range(numPts,len(rawData.Error)))
                                                        
        if not os.path.exists(params.folderForBkgSubtractedFiles):
            os.makedirs(params.folderForBkgSubtractedFiles)

        FileafterBckgrdSubtr=open(params.folderForBkgSubtractedFiles+rawFileName,'w')

        for i in range (0,len(rawData.Energy)):
            FileafterBckgrdSubtr.write(str(rawData.Energy[i])+'  '+ str(intensityAfterSubtractedBackground[i]-offset)+ '  '+str(rawData.Error[i])+'\n')
        
        FileafterBckgrdSubtr.close()  


        
        dataWithFit=Plot(self.params)
        dataWithFit.plotSingle(params.folderForBkgSubtractedFiles,params.folderForBkgSubtractedFiles,[rawFileName])

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
        for j in range(3,len(smoothedDataEnergy)-4):
            diff.append(smoothedDataIntensity[j]-bkgDataIntensity[list(bkgDataEnergy).index(smoothedDataEnergy[j])])
        print(diff)
        plt.plot(smoothedDataEnergy, smoothedDataIntensity, 'b-', label='fit',linewidth=1.0)
        plt.plot(bkgDataEnergy, bkgDataIntensity, 'r-', label='fit',linewidth=1.0)
        plt.xlabel(RSE_Constants.X_LABEL)
        plt.ylabel(RSE_Constants.Y_LABEL)
        plt.ylim((0,self.params.maxY)) 
        plt.grid()
        plt.title(rawData.filenames[0]+' test')
        plt.savefig(folder+rawData.filenames[0]+'_test.pdf')
        plt.close()

        return min(diff)
        
