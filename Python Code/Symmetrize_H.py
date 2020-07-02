#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


import os
import numpy as np
from Display import *
from collections import namedtuple
import matplotlib.pyplot as plt

def ExtractQfromFileName(FileName):

    if FileName[0]=='H':
        h=FileName[1:7]
        k=FileName[8:13]
        l=FileName[15:20]
    else:
        h=FileName[3:10]
        k=FileName[11:16]
        l=FileName[17:23]
    print (h,k,l)
    H=float(h);
    K=float(k);
    L=float(l);

    Q=[H,K,L]
    return Q

T=10
#location_ForPlots='E:/Data_LSNO_120meV_'+str(T)+'K/StretchingBkgExplore/good_slices/'

#datasetdir1='E:/Data_LSNO_120meV_240K/StretchingTests100forBackgr/good_slices/randomGoodFilesForBackground_H-6.00 K 0.00 L 0.00/'
datasetdir1='E:/Data_LSNO_120meV_240K/Longitudinal_LSNO110K01DH01K005/good_slices/'
      
filenames1=[file for file in os.listdir(datasetdir1) if file.startswith("H")and not file.endswith("pdf")]
filenames2=[file for file in os.listdir(datasetdir1) if file.startswith("B_H")and not file.endswith("pdf")]

print (filenames1)
print (filenames2)



T1=10
T2=450

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
for i in range(0,len(filenames1)):
    Q=ExtractQfromFileName(filenames1[i])
    if Q[1]<0:
        DataPlus=np.genfromtxt(datasetdir1+filenames1[i])
        intensity1=DataPlus[:,][:,1]
        energy1=DataPlus[:,][:,0]
        error1=DataPlus[:,][:,2]

        os.remove(datasetdir1+filenames1[i])
        File2=filenames1[i].replace('K-','K ')
        DataMinus=np.genfromtxt(datasetdir1+File2)
        intensity2=DataMinus[:,][:,1]
        energy2=DataMinus[:,][:,0]
        error2=DataMinus[:,][:,2]
        intensitySum=intensity1
        error=error1
    
        os.remove(datasetdir1+File2)
        try:
            for k in range(0,len(energy1)):
                j=np.argwhere(energy2==energy1[k])
                print(j)
                intensitySum[k]=(intensity1[k]+intensity2[j])/2
                error[k]=0.5*(error1[k]**2+error2[j]**2)**0.5
        except:
            d=1
        
        TxtFile=open(datasetdir1+File2,'w+')    
        for i in range (0,len(energy1)):
            TxtFile.write(str(energy1[i])+'  '+str(intensity1[i])+'  '+str(error1[i])+'\n')
        TxtFile.close()
  
blah
if 1==1:
    for j in range(0,len(filenames2)):
        if filenames1[i]==filenames2[j]:
           print(filenames1[i],filenames2[j])
        
           AllData1=np.genfromtxt(datasetdir1+filenames1[i])
           intensity1=AllData1[:,][:,1]
           energy1=AllData1[:,][:,0]
           error1=AllData1[:,][:,2]
           for ii in range(0,len(energy1)):
               intensity1[ii]=intensity1[ii]/(1+1/(np.exp(energy1[ii]/(0.08617*T1))-1))
               error1[ii]=error1[ii]/(1+1/(np.exp(energy1[ii]/(0.08617*T1))-1))

           AllData2=np.genfromtxt(datasetdir2+filenames2[j])
           intensity2=AllData2[:,][:,1]
           energy2=AllData2[:,][:,0]
           error2=AllData2[:,][:,2]
           for ii in range(0,len(energy2)):
               intensity2[ii]=intensity2[ii]/(1+1/(np.exp(energy2[ii]/(0.08617*T2))-1))
               error2[ii]=error2[ii]/(1+1/(np.exp(energy2[ii]/(0.08617*T2))-1))
#               print 1.0+1/(np.exp(energy2[ii]/(0.08617*T2))-1.0)

           plt.figure(figsize=(8.27,11.69,))
           plt.errorbar(energy1,intensity1,error1,fmt='o')
           plt.errorbar(energy2,intensity2,error2,fmt='*')
           plt.xlabel('Energy')
           plt.ylabel('Intensity')
           plt.grid() 
           plt.title(filenames1[i]+"  dh=0.1 dk=0.2 dl=0.5")
           #plt.text(20, 0.001,filenames1[i],fontdict=font)
           plt.savefig(location_ForPlots+filenames1[i]+'a4'+'portrait'+'.pdf')
           #plt.show()
           plt.close()
Disp=Display()
Disp.MakePlotSummary(location_ForPlots,'')

