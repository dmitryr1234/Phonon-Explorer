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
        if self.params.dataFileType=="sqw":
            import matlab.engine
            RSE_Constants.fileHandle=matlab.engine.start_matlab()
            RSE_Constants.fileHandle.addpath(self.params.matlabFolder)
            RSE_Constants.FLAG=1
            return
        if self.params.dataFileType=="nxs":
            sys.path.append(self.params.mantidFolder)
            from skimage import transform
            from mantid.simpleapi import LoadMD, CutMD#, ConvertToMD, BinMD, ConvertUnits, Rebin

            fileHandle=LoadMD(self.params.sqw_path,FileBackEnd=True)
            RSE_Constants.fileHandle=fileHandle
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
    

    def removeNAN(self):
# removes data points where Intensity is zero or where error/intensity>0.3 Never mind the name.
        index=[]
        for i in range (0,len(self.Energy)):
             if numpy.isnan(self.Intensity[i]):
                 self.Intensity[i]=0
        for i in range (0,len(self.Energy)):
            if self.Intensity[i]>0:
                if self.Error[i]/self.Intensity[i]>0.3:
                    self.Intensity[i]=0
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

    def makeRawSlice(self, bin_h, bin_k, bin_l, bin_e,folder,file,minPoints):
        if self.params.dataFileType=="sqw":
            self.makeRawSliceSQW(bin_h, bin_k, bin_l, bin_e,minPoints)
        if self.params.dataFileType=="nxs":
            self.makeRawSliceNXS(bin_h, bin_k, bin_l, bin_e,minPoints)
        self.removeNAN()
        FileIsGood=self.dataIsValid(minPoints)
        if FileIsGood:
            fileForSlice=DataTextFile(folder,file)
            fileForSlice.Write(self.Energy,self.Intensity,self.Error)
            return 0
        return 1
  
    def makeRawSliceNXS(self, bin_h, bin_k, bin_l, bin_e,minPoints):
        from mantid.simpleapi import CutMD#, ConvertToMD, BinMD, ConvertUnits, Rebin
        from mantid.api import Projection
        P=Projection(self.params.Projection_u,self.params.Projection_v)
        Slice00=CutMD(RSE_Constants.fileHandle,Projection=P.createWorkspace(OutputWorkspace='proj_ws'),PBins=(bin_h, bin_k, bin_l, bin_e),NoPix=True)
        out=self.SaveMDToAscii(Slice00)
        self.Error=100*out[:,0]
        self.Intensity=100*out[:,1]
        self.Energy=out[:,2]
#        print (self.Intensity)
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
    

    def SaveMDToAscii(self,ws,filename="l",IgnoreIntegrated=True,NumEvNorm=True,Format='%.6e'):
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
        return toPrint
        
    def makeRawSliceSQW(self, bin_h, bin_k, bin_l, bin_e,minPoints):
        # RETURNS 1 if slice is not written, 0 if SUCCESS
        #eng = matlab.engine.start_matlab();
        import matlab.engine
        proj = dict(
            u=matlab.double(list(self.params.Projection_u)),
            v=matlab.double(list(self.params.Projection_v)),
            type='rrr',
            uoffset=matlab.double([0,0,0,0])
            )
        out = io.StringIO()
        err = io.StringIO()
        self.Energy=[]
        self.Intensity=[]
        self.Error=[]
# The eval is to prevent the program from crashing when running with Python 2.7        
        bin_h_m = eval('matlab.double([*bin_h])')
        bin_k_m = eval('matlab.double([*bin_k])')
        bin_l_m = eval('matlab.double([*bin_l])')
        bin_e_m = eval('matlab.double([*bin_e])')

        try:
            ourCut = RSE_Constants.fileHandle.Getslice( 
                self.params.sqw_path,
                proj,
                bin_h_m,
                bin_k_m,
                bin_l_m,
                bin_e_m,
                '-nopix',
                stdout=out,
                stderr=err)
        except Exception as e:
            print("I am here")
            print(e)
            return 1
    
        print("ourCut done")
        print("cut done")
        print(out.getvalue())
        print(err.getvalue())
#        print(ourCut)

#        print(ourCut['s'][2][0])
#        print(ourCut['p'][2][0])
#        print(ourCut['e'][2][0])

        NumPoints=len(ourCut['p'])
#        print(NumPoints) 
        self.Intensity=zeros(NumPoints)
        self.Error=zeros(NumPoints)
        self.Energy=zeros(NumPoints)

        for i in range(0,NumPoints-1):
            self.Energy[i]=ourCut['p'][i][0]
            self.Intensity[i]=100*ourCut['s'][i][0]
            self.Error[i]=100*ourCut['e'][i][0]
#        print(bin_h, bin_k, bin_l)
              
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

        h=FileName[1:7]
        k=FileName[8:13]
        l=FileName[15:20] 
        
        H=float(h);
        K=float(k);
        L=float(l);

        Q=[H,K,L]
        return Q
    
    def SubtractConstant(self,Const):
        for i in range(len(self.Intensity)):
            self.Intensity[i]=self.Intensity[i]-Const
    
class DataSmall_q(Dataset):

    def __init__(self,params,dataDirectory):
        self.params=params
        self.dataDirectory=dataDirectory
        self.filenames=[]
        return
        
    def Read(self):
#        try:   #if folder with data slices is not there, just skip this
        if 1==1:
            self.filenames = [file for file in os.listdir(self.dataDirectory) if file.startswith("H") and not file.endswith(".pdf")]
#            print(self.filenames)
            self.NumberofDatasets = len(self.filenames)
            self.dataset=Dataset(self.dataDirectory,self.filenames)
            self.Energy=self.dataset.Energy
            self.Intensity=self.dataset.Intensity
            self.Error=self.dataset.Error
#            print(self.NumberofDatasets)
#        except:
#            print("data 116, except");
#            return
        return

    def Generate(self):
        bin_e=[self.params.e_start,self.params.e_step,self.params.e_end]
        qh=self.params.qh
        qk=self.params.qk
        ql=self.params.ql
        signVarL=[]
        signVarL=self.signVar(ql)
        signVarH=self.signVar(qh)
        signVarK=self.signVar(qk)        
        if RSE_Constants.FLAG==0:
            self.initialize();
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
                               try:
                                   self.makeRawSlice(bin_h, bin_k, bin_l, bin_e,self.dataDirectory,fileName,self.params.MinPointsInDataFile)#, eng)
#                                   print(fileName)
                               except Exception as e:
#                                   print(e)
                                   continue
                                   print("no slice")
        
       # return

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
        Qs=np.genfromtxt(os.path.join(self.params.path_InputFiles+self.params.textfile_for_selectedQs))
        QHlist=Qs[:,][:,0]
        QKlist=Qs[:,][:,1]
        QLlist=Qs[:,][:,2]
        if RSE_Constants.FLAG==0:
            self.initialize();
        for i in range (0,len(QHlist)):
            fileName=str(RSE_Constants.FILENAME_FORMAT % (QHlist[i],QKlist[i],QLlist[i]))
            bin_h=[QHlist[i]-self.params.Deltah, QHlist[i]+self.params.Deltah]
            bin_k=[QKlist[i]-self.params.Deltak, QKlist[i]+self.params.Deltak]        
            bin_l=[QLlist[i]-self.params.Deltal, QLlist[i]+self.params.Deltal]
            try:
#                print(fileName)
                self.makeRawSlice(bin_h, bin_k, bin_l, bin_e,self.dataDirectory,fileName,self.params.MinPointsInDataFile)#,eng)
                   
            except Exception as e:
                print(e)
                print("no slice")
                return
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
            self.fileHandle = self.initialize();
        for i in range (0,len(dataFileNames)):
#            print(dataFileNames[i])
            Q=self.ExtractQfromFileName(dataFileNames[i])
            data=Dataset(self.dataDirectory,[dataFileNames[i]])
            energy_start=data.Energy[0]
            deltaEnergy=self.params.e_step
            lastEnergyIndex=len(data.Energy)-1
            energy_end=data.Energy[lastEnergyIndex-1]
            Offset=floor(self.params.Resolution/deltaEnergy)+1;
# bin_e is class atribute. not bin_h, bin_k, bin_l, because they are different for every random file, but bin_e is the same.
            self.bin_e=[energy_start-Offset*deltaEnergy,deltaEnergy,energy_end+Offset*deltaEnergy];
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
#        print(self.bin_e)
#        print(bin_h)
#        print(bin_k)
#        print(bin_l)
        numFiles=1
        if self.params.BackgroundAlgorithm=="Standard":
            dataFileNames=[file for file in os.listdir(folder) if file.startswith("H") and not file.endswith("pdf")]
            numFiles=len(dataFileNames)
            if len(dataFileNames)>=self.params.maxFiles:
                print(folder + " full")
                return
        
        try:
#        if 1==1:
            self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,fileName,self.params.MinPointsInDataBackgroundFile)#,eng)
#            print(folder+fileName)
        except Exception as e:
            print(e)
            print("no slice 1")
#        print(math.sqrt((self.H*2*math.pi/self.params.a)**2+(self.K*2*math.pi/self.params.b)**2+(self.L*2*math.pi/self.params.c)**2))
        
        # Now do the random files; Try two times maxFiles, break when number of successfully saved files equals to maxFiles

        for i in range (0,2*self.params.maxFiles):
            if self.GenerateBackgroundDataFile(folder)==0:
                numFiles=numFiles+1
            if numFiles==self.params.maxFiles:
                break
        return
    
    def GenerateBackgroundDataFile(self,folder):
#        Angles=self.GeneratePhiTheta()
#        Phi=Angles[0]
#        Theta=Angles[1]
#        phiInDegrees=Phi*180/math.pi
#        thetaInDegrees=Theta*180/math.pi
        sys.path.insert(0,"Background Tools")
        B=__import__(self.params.BackgroundAlgorithm)
        BkgQ=B.BackgroundQ(self.H,self.K,self.L,self.params)

        #CalcQslash takes input in reciprocal angstoms, result returned in r.l.u
#        Qslash=self.CalcQslash(self.H*2*math.pi/self.params.a,self.K*2*math.pi/self.params.b,self.L*2*math.pi/self.params.c,Phi,Theta)
#  REPLACE this line with the following that is commented out
#        fileName=str(RSE_Constants.FILENAME_FORMAT % (self.H,self.K,self.L))
#        fileName=str("H%5.2f K%5.2f L%5.2f Phi%5.2f Theta%5.2f" % (BkgQ.Qslash[0],BkgQ.Qslash[1],BkgQ.Qslash[2],phiInDegrees,thetaInDegrees))
#        print(fileName)
        bin_h=[BkgQ.Qslash[0]-self.params.Deltah, BkgQ.Qslash[0]+self.params.Deltah]
        bin_k=[BkgQ.Qslash[1]-self.params.Deltak, BkgQ.Qslash[1]+self.params.Deltak]        
        bin_l=[BkgQ.Qslash[2]-self.params.Deltal, BkgQ.Qslash[2]+self.params.Deltal]
        try:
#            print(folder+BkgQ.fileName)
            return self.makeRawSlice(bin_h, bin_k, bin_l, self.bin_e,folder,BkgQ.fileName,self.params.MinPointsInDataBackgroundFile)#,eng)

        except Exception as e:
            print(e)
            print("no slice 2")
            return 1
        
