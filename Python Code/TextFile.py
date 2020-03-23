#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%



import numpy as np
import math
import os

class TextFile():
      
    def __init__(self,FolderName,FileName):
        self.filename = FileName
        self.foldername = FolderName
            
    def getFileName(self):
        return self.filename

    def getFolderName(self):
        return self.foldername

class Parameters(TextFile):

    def __init__(self,FolderName,FileName):
        TextFile.__init__(self,FolderName,FileName)
#        print(self.foldername)
#        print(self.filename)
        with open(os.path.join(self.foldername,self.filename)) as f:
             parameters = f.read().splitlines()
        
#        for i in range(0,len(parameters)):
#            print i,parameters[i]
#        self.sqw_path=self.Parse(parameters[0])
        self.keyword=''
        self.BkgMode=self.evalIntWarning(self.ParseByKeyword("BkgMode",parameters),0)
        self.QMode=self.evalIntWarning(self.ParseByKeyword("QMode",parameters),0)
        self.sqw_path=self.evalError(self.ParseByKeyword("sqw_path",parameters))
        self.dataFileType=self.sqw_path[self.sqw_path.index('.')+1:].lower()
        self.projectRootDir=self.evalError(self.ParseByKeyword("projectRootDir",parameters))
        if self.dataFileType=="nxs":
            self.mantidFolder=self.evalError(self.ParseByKeyword("mantidFolder",parameters))
        if self.dataFileType=="sqw":
            self.matlabFolder=self.evalError(self.ParseByKeyword("matlabFolder",parameters))
        self.ProcessedDataName=self.evalError(self.ParseByKeyword("ProcessedDataName",parameters))
        self.path_data=self.evalError(self.ParseByKeyword("projectRootDir",parameters))+self.ProcessedDataName+'/good_slices/'
        if not os.path.isdir(self.path_data):
            os.makedirs(self.path_data)
        #print(self.path_data)
        self.Projection_u=np.asarray(self.evalError(self.ParseByKeyword("Projection_u",parameters)).split(",")).astype(np.float)
        self.Projection_v=np.asarray(self.evalError(self.ParseByKeyword("Projection_v",parameters)).split(",")).astype(np.float)
        self.path_InputFiles=self.evalError(self.ParseByKeyword("InputFilesDir",parameters))
        self.ErrorToIntensityMaxRatio=self.evalRealWarning(self.ParseByKeyword("ErrorToIntensityMaxRatio",parameters),0.3)
        if self.QMode==1:    
            self.textfile_for_selectedQs=self.evalError(self.ParseByKeyword("textfile_for_selectedQs",parameters))
        if self.QMode==0:
            self.qh=self.evalRealWarning(self.ParseByKeyword("qh",parameters),0)
            self.qk=self.evalRealWarning(self.ParseByKeyword("qk",parameters),0)
            self.ql=self.evalRealWarning(self.ParseByKeyword("ql",parameters),0)
            self.h_start=self.evalIntWarning(self.ParseByKeyword("h_start",parameters),0)
            self.h_end=self.evalIntWarning(self.ParseByKeyword("h_end",parameters),0)
            self.k_start=self.evalIntWarning(self.ParseByKeyword("k_start",parameters),0)
            self.k_end=self.evalIntWarning(self.ParseByKeyword("k_end",parameters),0)
            self.l_start=self.evalIntWarning(self.ParseByKeyword("l_start",parameters),0)
            self.l_end=self.evalIntWarning(self.ParseByKeyword("l_end",parameters),0)
        self.e_start=eval(self.evalError(self.ParseByKeyword("e_start",parameters)))
        self.e_end=eval(self.evalError(self.ParseByKeyword("e_end",parameters)))
        self.e_step=eval(self.evalError(self.ParseByKeyword("e_step",parameters)))
        self.Deltah=eval(self.evalError(self.ParseByKeyword("Deltah",parameters)))
        self.Deltak=eval(self.evalError(self.ParseByKeyword("Deltak",parameters)))
        self.Deltal=eval(self.evalError(self.ParseByKeyword("Deltal",parameters)))
        self.MinPointsInDataFile=self.evalIntWarning(self.ParseByKeyword("MinPointsInDataFile",parameters),10)
        self.location_ForPlots=self.path_data
        self.maxY=eval(self.evalError(self.ParseByKeyword("maxY",parameters)))
        self.dataFileNameStart=self.evalWarning(self.ParseByKeyword("dataFileNameStart",parameters),"H")
        
    def ReadBackgroundParams(self):
        with open(os.path.join(self.foldername,self.filename)) as f:
             parameters = f.read().splitlines()

        self.a=eval(self.evalError(self.ParseByKeyword("a",parameters)))
        self.b=eval(self.evalError(self.ParseByKeyword("b",parameters)))
        self.c=eval(self.evalError(self.ParseByKeyword("c",parameters)))
        self.phiRange=0#eval(self.ParseByKeyword("phiRange",parameters)) Not used now
        self.thetaRange=0#eval(self.ParseByKeyword("thetaRange",parameters)) Not used now
        self.NumberOfTries=self.evalIntWarning(self.ParseByKeyword("NumberOfTries",parameters),10)
        self.maxFiles=self.evalIntWarning(self.ParseByKeyword("maxFiles",parameters),10)
#        self.Resolution=eval(self.evalError(self.ParseByKeyword("Resolution",parameters)))
        self.MinPointsInDataBackgroundFile=self.evalIntWarning(self.ParseByKeyword("MinPointsInDataBackgroundFile",parameters),10)
        
        self.MinPeakWidthForSmoothing=eval(self.evalError(self.ParseByKeyword("MinPeakWidthForSmoothing",parameters)))
        self.InitWidthsFinal=self.MinPeakWidthForSmoothing
        self.Resolution=self.MinPeakWidthForSmoothing
        self.BackgroundAlgorithm=self.evalWarning(self.ParseByKeyword("BackgroundAlgorithm",parameters),"Standard")
        if self.BackgroundAlgorithm!="Standard":
            self.maxFiles=2
        self.NumberofPeaks=0
        self.ReadSharedParams(parameters)

    def ReadMultizoneFitParams(self):
        with open(os.path.join(self.foldername,self.filename)) as f:
             parameters = f.read().splitlines()

        self.WidthLowerBound=eval(self.ParseByKeyword("WidthLowerBound",parameters))
        self.fileWithGuesses=self.evalError(self.ParseByKeyword("fileWithGuesses",parameters))
        self.InitWidthsFinal=self.WidthLowerBound

        try:
#        if 1==1:
            with open(self.path_InputFiles+self.fileWithGuesses) as f:
                self.positionGuesses=[float(x) for x in next(f).split()]

            self.NumberofPeaks=len(self.positionGuesses)
#            print ("Position Guesses ",self.positionGuesses,"number of peaks ",self.NumberofPeaks)
        except:
            print ("WARNING: Position Guesses not specified")

        self.ReadSharedParams(parameters)

    def ReadSharedParams(self,parameters): #multizone and background
        self.locationForOutputParam=self.path_data
        self.InitAmplitudes=eval(self.ParseByKeyword("InitialAmplitude",parameters))
        self.folderForBkgSubtractedFiles=self.projectRootDir+self.ProcessedDataName+'/subtr_background/'
        self.NumberofFitIter=self.evalIntWarning(self.ParseByKeyword("NumberofIter",parameters),3)


        
    def getIndex(self,keyword,parameters):
        for i in range(0,len(parameters)):
            try:
                if keyword==parameters[i][:parameters[i].index('=')]:
                    return i
            except:
                d=1
        return -1
    def ParseByKeyword(self,keyword,parameters):
        Index=self.getIndex(keyword,parameters)
        self.keyword=keyword
        if Index==-1:
            return "None"
        return self.Parse(parameters[Index])
    def Parse(self,line):
        return line[line.index('=')+1:]
    def evalRealWarning(self,string,default):
        if string=="None":
            print("WARNING: "+self.keyword+" not specified")
            return default
        else:
            return eval(string)
    def evalIntWarning(self,string,default):
        if string=="None":
            print("WARNING: "+self.keyword+" not specified")
            return default
        else:
            return int(string)
    def evalWarning(self,string,default):
        if string=="None":
            print("WARNING: "+self.keyword+" not specified")
            return default
        else:
            return string

    def evalError(self,string):
        if string=="None":
            print("Parameter ERROR: "+ self.keyword+" not specified")
            raise Exception("Parameter ERROR: "+self.keyword+" not specified")
        else:
            return string
        
class DataTextFile(TextFile):
    def __init__(self,FolderName,FileName):
        TextFile.__init__(self,FolderName,FileName)
        
    def Read(self):
#        print (self.foldername+self.filename)
        data=np.genfromtxt(self.foldername+self.filename)
        return data
    
    def Write(self, Energy, Intensity, Error):

#        print os.path.isdir("E:/")
        if not os.path.isdir(self.foldername):
            os.makedirs(self.foldername)

        TxtFile=open(self.foldername+self.filename,'w+')    
        for i in range (0,len(Energy)):
            TxtFile.write(str(Energy[i])+'  '+str(Intensity[i])+'  '+str(Error[i])+'\n')
        TxtFile.close()
        
    
