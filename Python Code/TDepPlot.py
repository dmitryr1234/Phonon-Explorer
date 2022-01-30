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

location_ForPlots='E:/Data_LSNO_120meV/plots/'

FileName="H-5.00 K 0.00 L 0.00"

datasetdir=[]

datasetdir.append('E:/Data_LSNO_120meV_10K/Longitudinal_110_binH01K005/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_190K/Longitudinal_110_bin01/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_240K/Longitudinal_LSNO110H01K005/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_300K/Longitudinal_LSNO110H01K005/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_450K/Longitudinal_LSNO110H01K005/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_600K/Longitudinal_LSNO110H01K005/subtr_background/')
'''
datasetdir.append('E:/Data_LSNO_120meV_10K/StretchingTests100/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_190K/StretchingTests100/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_240K/StretchingTests100/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_300K/StretchingTests100/subtr_background/')
#datasetdir.append('E:/Data_LSNO_120meV_450K/StretchingTests100/subtr_background/')
#datasetdir.append('E:/Data_LSNO_120meV_600K/StretchingTests100/subtr_background/')
'''
NumDir=6
estep=1.25
offset=0
#T=[10,190,240,300,450,600]
T=[0.1,0.1,0.1,0.1,0.1,0.1]
Norm=[1,1,1,0.75,0.75,0.75]
#offs=[0,0.0012,0.0012,0.0012,0.0012,0.0012]
offs=[0,0.0008,0.0008,0.0008,0.0008,0.0008]

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

intensity=[]
energy=[]
error=[]
energyMin=1000
energyMax=-500
for i in range(0,len(datasetdir)):
    AllData=np.genfromtxt(datasetdir[i]+FileName)
    energy=AllData[:,][:,0]
    energyMin=min(np.amin(energy),energyMin)
    energyMax=max(np.amax(energy),energyMax)
print(energyMin,energyMax)
energy0=np.zeros(int((energyMax-energyMin)/estep)+1)
intensity0=np.zeros((len(energy0),len(datasetdir)))
error0=np.zeros((len(energy0),len(datasetdir)))
for i in range(0,len(energy0)):
    energy0[i]=energyMin+i*estep
#print(energy0)

for i in range(0,len(datasetdir)):
    AllData=np.genfromtxt(datasetdir[i]+FileName)
    intensity=AllData[:,][:,1]
    energy=AllData[:,][:,0]
    error=AllData[:,][:,2]
    offset=offset+offs[i]
    print(offset)
    for j in range(0,len(energy)):
        index=np.argwhere(energy0==energy[j])
        intensity0[index,i]=Norm[i]*intensity[j]/(1+1/(np.exp(energy[j]/(0.08617*T[i]))-1))+offset
        error0[index,i]=Norm[i]*error[j]/(1+1/(np.exp(energy[j]/(0.08617*T[i]))-1))

#print(intensity0)
StringArray=[]
for j in range(0,len(energy0)):
    string=str(energy0[j])
    for i in range(0,len(datasetdir)):
        string+=(','+str(intensity0[j,i])+','+str(error0[j,i]))
    string+='\n'
    StringArray.append(string)

if not os.path.isdir(location_ForPlots):
    os.makedirs(location_ForPlots)
        
TxtFile=open(location_ForPlots+FileName,'w+')    
for i in range (0,len(energy0)):
    TxtFile.write(StringArray[i])
TxtFile.close()


#DataForPlotFinal=[]

#for i in range(0,len(datasetdir)):
'''
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
           plt.title(filenames1[i]+"  dh=0.05 dk=0.1 dl=2")
           #plt.text(20, 0.001,filenames1[i],fontdict=font)
           plt.savefig(location_ForPlots+filenames1[i]+'a4'+'portrait'+'.pdf')
           #plt.show()
           plt.close()
Disp=Display()
Disp.MakePlotSummary(location_ForPlots,'')
'''

