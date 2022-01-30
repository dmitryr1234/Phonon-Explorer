#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


from TextFile import *
import numpy
from numpy import *
import math
import os
import random
import io
from RSE_Constants import *
import time
import sys
from decimal import *
getcontext().prec=6
#from nexusformat.nexus import *

class Dataset: #Dataset can be either a single cut at one Q or several cuts put together for the purposes of multizone fitting,
    # In the former case it is initialized with an array of filenames that has one filename, in the latter case with an array containing many filenames. 
    def __init__(self,folder,filenames):
#        print(filenames)
        self.NumberofDatasets = len(filenames)
        self.Energy=[]
        self.Intensity=[]
        self.Error=[]
        self.Nint=[]
        self.Neng=[]
        self.filenames=filenames
        self.dataDirectory=folder
        self.appendDataset()
        self.tempIndex=1
        #self.eng = matlab.engine.start_matlab()
    def initialize(self):
        sys.path.insert(0,"Tools to access raw data")
        R=__import__(self.params.rawDataClassFile)
#        RSE_Constants.rawData=R.RawData(self.params.sqw_path);
        RSE_Constants.rawData=R.RawData(self.params);

        RSE_Constants.FLAG=1

        return

    def appendDataset(self):
        for m in range (0,self.NumberofDatasets):
#            print(self.dataDirectory,self.filenames[m])
            fileData=DataTextFile(self.dataDirectory,self.filenames[m])
            AllData=fileData.Read()
            energy=AllData[:,][:,0]+100*m
            intensity=AllData[:,][:,1] 
            error=AllData[:,][:,2]
            self.Energy=numpy.append(self.Energy,energy) 
            self.Intensity=numpy.append(self.Intensity,intensity)
            self.Error=numpy.append(self.Error,error)
    

    def clean(self):
# removes data points where Intensity is zero or where error/intensity>self.params.ErrorToIntensityMaxRatio
        index=[]
        for i in range (0,len(self.Energy)):
             if numpy.isnan(self.Intensity[i]):
                 self.Intensity[i]=0
        for i in range (0,len(self.Energy)):
            if self.Intensity[i]>0:
                if self.Error[i]/self.Intensity[i]>=self.params.ErrorToIntensityMaxRatio:
                    d=0
#                    self.Intensity[i]=0
        index.extend(np.nonzero(self.Intensity))
        Nint=zeros(len(index[0]))
        Neng=zeros(len(index[0]))
        Nerr=zeros(len(index[0]))
        for i in range (0,len(index[0])):
            Nint[i]=self.Intensity[index[0][i]]
            Neng[i]=self.Energy[index[0][i]]
            Nerr[i]=self.Error[index[0][i]]
        self.Intensity=Nint
        self.Energy=Neng
        self.Error=Nerr
        
    def smooth(self):
        firstEnergyIndex=0
        lastEnergyIndex=len(self.Energy)-1
#        print(params.Resolution, params.e_step,0.8*params.Resolution/params.e_step)
#        print(data.Energy[firstEnergyIndex:lastEnergyIndex:int(0.8*params.Resolution/params.e_step)])
        positions=self.Energy[firstEnergyIndex:lastEnergyIndex:int(params.Resolution/params.e_step)]
#        print(positions)
#        print([data.Energy[lastEnergyIndex]])
        if positions[len(positions)-1]<self.Energy[lastEnergyIndex]:
            positions=numpy.append(positions,[self.Energy[lastEnergyIndex]])
#        print(positions)
        params.positionGuesses=positions
        params.NumberofPeaks=len(positions)        
        params.InitWidthsFinal=params.MinPeakWidthForSmoothing
        params.WidthLowerBound=params.MinPeakWidthForSmoothing
        InitGuess=InitialGuesses(params,self)
        InitGuess.NumberofPeaks=len(positions) #overwrite
        fData=FittingData(params,InitGuess,self)
        self.fitParamsFofSmoothing=fData.doFitting()
        
        
    def removeNAN(self):
        Neng=np.zeros(1)
        Nint=np.zeros(1)
        Nerr=np.zeros(1)
        for i in range (0,len(self.Energy)):
             if not numpy.isnan(self.Intensity[i]):
                 Neng=numpy.append(Neng,self.Energy[i])
                 Nint=numpy.append(Nint,self.Intensity[i])
                 Nerr=numpy.append(Nerr,self.Error[i])
        self.Intensity=Nint[1:len(Nint)]
        self.Energy=Neng[1:len(Nint)]
        self.Error=Nerr[1:len(Nint)]

    def makeRawSlice(self, bin_h, bin_k, bin_l, bin_e,folder,file,minPoints,mult=1):

        bin_h[0]=bin_h[0]+self.params.Offset_H
        bin_h[1]=bin_h[1]+self.params.Offset_H
        bin_k[0]=bin_k[0]+self.params.Offset_K
        bin_k[1]=bin_k[1]+self.params.Offset_K
        bin_l[0]=bin_l[0]+self.params.Offset_L
        bin_l[1]=bin_l[1]+self.params.Offset_L
        bin_e[0]=bin_e[0]+self.params.Offset_E
        bin_e[2]=bin_e[2]+self.params.Offset_E

        RSE_Constants.rawData.GetSlice(bin_h, bin_k, bin_l, bin_e, self.params.Projection_u, self.params.Projection_v)

        bin_h[0]=bin_h[0]-self.params.Offset_H
        bin_h[1]=bin_h[1]-self.params.Offset_H
        bin_k[0]=bin_k[0]-self.params.Offset_K
        bin_k[1]=bin_k[1]-self.params.Offset_K
        bin_l[0]=bin_l[0]-self.params.Offset_L
        bin_l[1]=bin_l[1]-self.params.Offset_L
        bin_e[0]=bin_e[0]-self.params.Offset_E
        bin_e[2]=bin_e[2]-self.params.Offset_E

        self.Energy=RSE_Constants.rawData.Energy
        self.Intensity=RSE_Constants.rawData.Intensity
        self.Error=RSE_Constants.rawData.Error
        
        self.clean()
        FileIsGood=self.dataIsValid(minPoints)
        if FileIsGood:
            fileForSlice=DataTextFile(folder,file)
#            print ('mult  '+ str(mult))
            fileForSlice.Write(self.Energy,mult*self.Intensity,mult*self.Error)
            return 0
        return 1

    def dim2array(self,d):
        
        """
        Create a numpy array containing bin centers along the dimension d
        input: d - IMDDimension
        return: numpy array, from min+st/2 to max-st/2 with step st  
        """
        dmin=d.getMinimum()
        dmax=d.getMaximum()
        dstep=d.getX(1)-d.getX(0)
        return np.arange(dmin+dstep/2,dmax,dstep)
    

    '''def SaveMDToAscii(self,ws,filename="l",IgnoreIntegrated=True,NumEvNorm=True,Format='%.6e'):
#        """
#        Save an MDHistoToWorkspace to an ascii file (column format)
#        input: ws - handle to the workspace
#        input: filename - path to the output filename
#        input: IgnoreIntegrated - if True, the integrated dimensions are ignored (smaller files), but that information is lost
#        input: NumEvNorm - must be set to true if data was converted to MD from a histo workspace (like NXSPE) and no MDNorm... algorithms were used
#        input: Format - value to pass to numpy.savetxt
#        return: nothing
#        """
        if ws.id()!='MDHistoWorkspace':
            raise ValueError("The workspace is not an MDHistoToWorkspace")
        #get dimensions
        if IgnoreIntegrated:
            dims=ws.getNonIntegratedDimensions()
        else:
            dims=[ws.getDimension(i) for i in range(ws.getNumDims())]
        dimarrays=[self.dim2array(d) for d in dims]
        newdimarrays=np.meshgrid(*dimarrays,indexing='ij')
        #get data
        data=ws.getSignalArray()*1.
        err2=ws.getErrorSquaredArray()*1.
        if NumEvNorm:
            nev=ws.getNumEventsArray()
            data/=nev
            err2/=nev
        err=np.sqrt(err2)
        #write file
        header="Intensity Error "+" ".join([d.getName() for d in dims])
        header+="\n shape: "+"x".join([str(d.getNBins()) for d in dims])
        toPrint=np.c_[data.flatten(),err.flatten()]
        for d in newdimarrays:
            toPrint=np.c_[toPrint,d.flatten()]
        return toPrint'''
                
    def dataIsValid(self,minPointsInDataFile):

        nn=0
        FileIsGood=False
        for i in range (0,len(self.Energy)):
            if self.Intensity[i]>0:
                if self.Error[i]/self.Intensity[i]<self.params.ErrorToIntensityMaxRatio:
                   nn=nn+1
        if nn>minPointsInDataFile:
            FileIsGood=True

        return FileIsGood  

    def ExtractQfromFileName(self,FileName):

        h=FileName[1:FileName.find("K")]
        k=FileName[FileName.find("K")+1:FileName.find("L")]
        l=FileName[FileName.find("L")+1:21] 

        H=float(h);
        K=float(k);
        L=float(l);

        Q=[H,K,L]
        return Q

    def SubtractConstant(self,Const):
        for i in range(len(self.Intensity)):
            self.Intensity[i]=self.Intensity[i]-Const

    def SubtractLine(self,Intercept,Slope):
        for i in range(len(self.Intensity)):
            self.Intensity[i]=self.Intensity[i]-Intercept-Slope*self.Energy[i]

    def DivideByBoseFactorNorm(self,T,M=1.0):  #M normalization
        for i in range(0,len(self.Energy)):
           self.Intensity[i]=M*self.Intensity[i]/(1+1/(np.exp(self.Energy[i]/(0.08617*T))-1))
           self.Error[i]=M*self.Error[i]/(1+1/(np.exp(self.Energy[i]/(0.08617*T))-1))
           
class DataSmall_q(Dataset):

    def __init__(self,params,dataDirectory,q=[1000,1000,1000]):
        self.params=params
        self.dataDirectory=dataDirectory
        self.filenames=[]
        self.q=q
#        print(q)
        return
        
    def Read(self):
        try:   #if folder with data slices is not there, just skip this
#        if 1==1:
            self.filenames = self.Filterlist([file for file in os.listdir(self.dataDirectory) if file.startswith("H") and not file.endswith(".pdf")])
            
#            print(self.filenames)
            self.NumberofDatasets = len(self.filenames)
            self.dataset=Dataset(self.dataDirectory,self.filenames)
            self.Energy=self.dataset.Energy
            self.Intensity=self.dataset.Intensity
            self.Error=self.dataset.Error
#            print(self.NumberofDatasets)
        except:
            print("data 116, except");
#            return
        return
    
    def Filterlist(self,filenames):
        filteredFilenames=[]
        if self.q==[1000,1000,1000]:
            return filenames
        else:
           sys.path.insert(0,"reduced q Algorithms")
           Sq=__import__(self.params.SmallqAlgorithm)
           for i in range(0,len(filenames)):
               filename=filenames[i]
               Q=self.ExtractQfromFileName(filename)
               qq=Sq.Smallq(Q)
               q=qq.q

#               q=self.ConvertToSmallQ(Q)
               if (abs(q[0]-self.q[0])<0.0001 and abs(q[1]-self.q[1])<0.0001 and abs(q[2]-self.q[2])<0.0001):
                   filteredFilenames.append(filename)
                   
        return filteredFilenames               
   
    def Generate(self):
        bin_e=[self.params.e_start,self.params.e_step,self.params.e_end]
        qh=self.params.qh
        qk=self.params.qk
        ql=self.params.ql
        sys.path.insert(0,"reduced q Algorithms")
        Sq=__import__(self.params.SmallqAlgorithm)
        qq=Sq.Smallq([qh,qk,ql])
        signVarL=[]
        signVarL=self.signVar(ql)
        signVarH=self.signVar(qh)
        signVarK=self.signVar(qk)        
        if RSE_Constants.FLAG==0:
            self.initialize();
        for jjj in range(0,len(qq.qlist)):
            qh=qq.qlist[jjj][0]
            qk=qq.qlist[jjj][1]
            ql=qq.qlist[jjj][2]
            for l in range (self.params.l_start,self.params.l_end+1):
                for ii in range (0,len(signVarL)):
                    L=l+signVarL[ii]*ql
                    bin_l=[L-self.params.Deltal, L+self.params.Deltal]
                    for h in range (self.params.h_start,self.params.h_end+1):
                        for jj in range (0,len(signVarH)):
                           H=h+signVarH[jj]*qh
                           bin_h=[H-self.params.Deltah, H+self.params.Deltah]
                           for k in range (self.params.k_start,self.params.k_end+1):
                               for kk in range (0,len(signVarK)):
                                   K=k+signVarK[kk]*qk
                                   bin_k=[K-self.params.Deltak, K+self.params.Deltak]
                               
                                   fileName=str(RSE_Constants.FILENAME_FORMAT % (H,K,L))
#                                   if 1==1:
                                   print(H,K,L)
#                                   if abs(h)>2:
#                                   if H%h!=0 and h*h>(k*k+l*l):
                                   try:
                                       
                                        self.makeRawSlice(bin_h, bin_k, bin_l, bin_e,self.dataDirectory,fileName,self.params.MinPointsInDataFile)#, eng)
#                                       print(fileName)
                                   except Exception as e:
                                       print(e)
                                       continue
                                       print("no slice")
        
        return

    def signVar(self,q):
        if q==0 or q==0.5:
            return [1]
        else:
            return [-1,1]
    
class CollectionOfQs(Dataset):
    def __init__(self,params):
        self.params=params
        self.dataDirectory=self.params.path_data

    def Generate(self):
        bin_e=[self.params.e_start,self.params.e_step,self.params.e_end]        
        Qs=np.genfromtxt(self.params.path_InputFiles+self.params.textfile_for_selectedQs)
        try:
            QHlist=Qs[:,][:,0]
            QKlist=Qs[:,][:,1]
            QLlist=Qs[:,][:,2]
        except:
            QHlist=[Qs[0]]
            QKlist=[Qs[1]]
            QLlist=[Qs[2]]
        if RSE_Constants.FLAG==0:
            self.initialize();
        for i in range (0,len(QHlist)):
            fileName=str(RSE_Constants.FILENAME_FORMAT % (QHlist[i],QKlist[i],QLlist[i]))
            bin_h=[QHlist[i]-self.params.Deltah, QHlist[i]+self.params.Deltah]
            bin_k=[QKlist[i]-self.params.Deltak, QKlist[i]+self.params.Deltak]        
            bin_l=[QLlist[i]-self.params.Deltal, QLlist[i]+self.params.Deltal]
            try:
                print(fileName)
                self.makeRawSlice(bin_h, bin_k, bin_l, bin_e,self.dataDirectory,fileName,self.params.MinPointsInDataFile)#,eng)
                   
            except Exception as e:
                print(e)
                print("no slice CollectionOfQs")
        return

class DataBackgroundQs(Dataset):
    def __init__(self,params):
        self.params=params
        self.params.ReadBackgroundParams()
        self.dataDirectory=self.params.path_data
    def GenerateAllFiles(self):
#        os.listdir(self.dataDirectory)
        dataFileNames=[file for file in os.listdir(self.dataDirectory) if file.startswith("H") and not file.endswith("pdf")]
        if RSE_Constants.FLAG==0:
            self.fileHandle = self.initialize()
        for i in range (0,len(dataFileNames)):
#            print(dataFileNames[i])
            Q=self.ExtractQfromFileName(dataFileNames[i])
            data=Dataset(self.dataDirectory,[dataFileNames[i]])
            self.energy_start=data.Energy[0]
            deltaEnergy=self.params.e_step
            lastEnergyIndex=len(data.Energy)-1
            self.energy_end=data.Energy[lastEnergyIndex]
            Offset=floor(self.params.Resolution/deltaEnergy)+1;
# bin_e is class atribute. not bin_h, bin_k, bin_l, because they are different for every random file, but bin_e is the same.
            self.bin_e=[self.energy_start-Offset*deltaEnergy,deltaEnergy,self.energy_end+Offset*deltaEnergy];
            self.GenerateFolder(Q)#,eng)
    def GenerateFolder(self,Q):#,eng):
        self.H=Q[0]
        self.K=Q[1]
        self.L=Q[2]
        folder=self.dataDirectory+RSE_Constants.GEN_FOLDER+str(RSE_Constants.DIR_FORMAT % (self.H,self.K,self.L))
        if not os.path.isdir(folder):
            os.makedirs(folder)
        # Save original file first
#  REPLACE this line with the following that is commented out
        fileName=str(RSE_Constants.FILENAME_FORMAT % (self.H,self.K,self.L))
#        fileName=str("H%5.2f K%5.2f L%5.2f Phi%5.2f Theta%5.2f" % (self.H,self.K,self.L,0,0))

        bin_h=[self.H-self.params.Deltah, self.H+self.params.Deltah]
        bin_k=[self.K-self.params.Deltak, self.K+self.params.Deltak]        
        bin_l=[self.L-self.params.Deltal, self.L+self.params.Deltal]
#        print(self.bin_e,self.params.e_end)
#        print(bin_h)
#        print(bin_k)
#        print(bin_l)
        dataFileNames=[file for file in os.listdir(folder) if file.startswith("H") and not file.endswith("pdf")]
        numFiles=len(dataFileNames)
        if self.params.BackgroundAlgorithm=="Standard":
            if len(dataFileNames)>=self.params.maxFiles:
                if(self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)==1):
                    self.bin_e=[self.bin_e[0],self.bin_e[1],self.energy_end]
                    if(self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)==1):
                        self.bin_e=[self.energy_start,self.bin_e[1],self.energy_end]
                        self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)
            
                print(folder+fileName)
                return
        
        try:            
#            self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)#,eng)
            if(self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)==1):
                self.bin_e=[self.bin_e[0],self.bin_e[1],self.energy_end]
                if(self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)==1):
                    self.bin_e=[self.energy_start,self.bin_e[1],self.energy_end]
                    self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)
            numFiles=numFiles+1
            print(folder+fileName)
        except Exception as e:
            print(e)
            print("no slice 1")
#        print(math.sqrt((self.H*2*math.pi/self.params.a)**2+(self.K*2*math.pi/self.params.b)**2+(self.L*2*math.pi/self.params.c)**2))
        
        # Now do the Q' files; Try two times maxFiles, break when number of successfully saved files equals to maxFiles
        print("maxfiles  ",self.params.maxFiles)
        for i in range (0,2*self.params.maxFiles):
            if self.GenerateBackgroundDataFile(folder,i)==0:
                numFiles=numFiles+1
            if numFiles==self.params.maxFiles:
                break
        return
    
    def GenerateBackgroundDataFile(self,folder,index):

        sys.path.insert(0,"Background Tools")
        B=__import__(self.params.BackgroundAlgorithm)
        BkgQ=B.BackgroundQ(self.H,self.K,self.L,self.params,index)
        if BkgQ.flag==1:
            return 3
        #CalcQslash takes input in reciprocal angstoms, result returned in r.l.u
        
        bin_h=[BkgQ.Qslash[0]-self.params.Deltah, BkgQ.Qslash[0]+self.params.Deltah]
        bin_k=[BkgQ.Qslash[1]-self.params.Deltak, BkgQ.Qslash[1]+self.params.Deltak]        
        bin_l=[BkgQ.Qslash[2]-self.params.Deltal, BkgQ.Qslash[2]+self.params.Deltal]
        try:
            print(folder+BkgQ.fileName)
            return self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,BkgQ.fileName,self.params.MinPointsInDataBackgroundFile,BkgQ.mult)
        except Exception as e:
            print(e)
            print("no slice 2")
            return 1
        
