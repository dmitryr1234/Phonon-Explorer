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

location_ForPlots='E:/Bagage22/Bagage_22_TA/subtr_background/'
location_ForPlots='E:/Bagage22/Bagage_22_TA_002/good_slices/'

FileNames=[]
'''





#FileNames.append("H-6.67 K 0.00 L 0.00")



FileNames.append("H-4.70 K-4.70 L 0.00")
FileNames.append("H-4.80 K-4.80 L 0.00")
#FileNames.append("H-5.33 K 0.00 L 0.00")
FileNames.append("H-4.90 K-4.90 L 0.00")
FileNames.append("H-5.00 K-5.00 L 0.00")
FileNames.append("H-5.10 K-5.10 L 0.00")
FileNames.append("H-5.20 K-5.20 L 0.00")
FileNames.append("H-5.30 K-5.30 L 0.00")
FileNames.append("H-5.40 K-5.40 L 0.00")
FileNames.append("H-5.50 K-5.50 L 0.00")

FileNames.append("H-5.50 K-3.50 L 0.00")
FileNames.append("H-5.60 K-3.60 L 0.00")
FileNames.append("H-5.70 K-3.70 L 0.00")
FileNames.append("H-5.80 K-3.80 L 0.00")
#FileNames.append("H-5.33 K 0.00 L 0.00")
FileNames.append("H-5.90 K-3.90 L 0.00")
FileNames.append("H-6.00 K-4.00 L 0.00")
FileNames.append("H-6.10 K-4.10 L 0.00")
FileNames.append("H-6.20 K-4.20 L 0.00")
FileNames.append("H-6.30 K-4.30 L 0.00")
FileNames.append("H-6.40 K-4.40 L 0.00")
FileNames.append("H-6.50 K-4.50 L 0.00")

FileNames.append("H 0.00 K 0.00 L-5.50")
FileNames.append("H 0.00 K 0.00 L-5.55")
FileNames.append("H 0.00 K 0.00 L-5.60")
FileNames.append("H 0.00 K 0.00 L-5.65")
FileNames.append("H 0.00 K 0.00 L-5.70")
FileNames.append("H 0.00 K 0.00 L-5.75")
FileNames.append("H 0.00 K 0.00 L-5.80")
FileNames.append("H 0.00 K 0.00 L-5.85")
FileNames.append("H 0.00 K 0.00 L-6.00")
FileNames.append("H 0.00 K 0.00 L-6.05")
FileNames.append("H 0.00 K 0.00 L-6.10")
FileNames.append("H 0.00 K 0.00 L-6.15")
'''

FileNames.append("H-1.00 K 0.00 L-2.00")
FileNames.append("H-0.95 K 0.00 L-2.00")
FileNames.append("H-0.90 K 0.00 L-2.00")
FileNames.append("H-0.85 K 0.00 L-2.00")
FileNames.append("H-0.80 K 0.00 L-2.00")
FileNames.append("H-0.75 K 0.00 L-2.00")
FileNames.append("H-0.70 K 0.00 L-2.00")
FileNames.append("H-0.65 K 0.00 L-2.00")
FileNames.append("H-0.60 K 0.00 L-2.00")
FileNames.append("H-0.55 K 0.00 L-2.00")
FileNames.append("H-0.50 K 0.00 L-2.00")
FileNames.append("H-0.45 K 0.00 L-2.00")
FileNames.append("H-0.40 K 0.00 L-2.00")
FileNames.append("H-0.35 K 0.00 L-2.00")
FileNames.append("H-0.30 K 0.00 L-2.00")
FileNames.append("H-0.25 K 0.00 L-2.00")
FileNames.append("H-0.20 K 0.00 L-2.00")
FileNames.append("H-0.15 K 0.00 L-2.00")
FileNames.append("H-0.10 K 0.00 L-2.00")
FileNames.append("H-0.05 K 0.00 L-2.00")
FileNames.append("H 0.00 K 0.00 L-2.00")
FileNames.append("H 0.05 K 0.00 L-2.00")
FileNames.append("H 0.10 K 0.00 L-2.00")
FileNames.append("H 0.15 K 0.00 L-2.00")
FileNames.append("H 0.20 K 0.00 L-2.00")
FileNames.append("H 0.25 K 0.00 L-2.00")
FileNames.append("H 0.30 K 0.00 L-2.00")
FileNames.append("H 0.35 K 0.00 L-2.00")
FileNames.append("H 0.40 K 0.00 L-2.00")
FileNames.append("H 0.45 K 0.00 L-2.00")
FileNames.append("H 0.50 K 0.00 L-2.00")
FileNames.append("H 0.55 K 0.00 L-2.00")
FileNames.append("H 0.60 K 0.00 L-2.00")
FileNames.append("H 0.65 K 0.00 L-2.00")
FileNames.append("H 0.70 K 0.00 L-2.00")
FileNames.append("H 0.75 K 0.00 L-2.00")
FileNames.append("H 0.80 K 0.00 L-2.00")
FileNames.append("H 0.85 K 0.00 L-2.00")
FileNames.append("H 0.90 K 0.00 L-2.00")
FileNames.append("H 0.95 K 0.00 L-2.00")
FileNames.append("H 1.00 K 0.00 L-2.00")



'''
FileNames.append("H 0.50 K 0.00 L-6.00")
FileNames.append("H 0.45 K 0.00 L-6.00")
FileNames.append("H 0.40 K 0.00 L-6.00")
FileNames.append("H 0.35 K 0.00 L-6.00")
FileNames.append("H 0.30 K 0.00 L-6.00")
FileNames.append("H 0.25 K 0.00 L-6.00")
FileNames.append("H 0.20 K 0.00 L-6.00")

FileNames.append("H-6.00 K-1.00 L 0.00")
FileNames.append("H-6.00 K-0.90 L 0.00")
FileNames.append("H-6.00 K-0.80 L 0.00")
FileNames.append("H-6.00 K-0.70 L 0.00")
FileNames.append("H-6.00 K-0.60 L 0.00")
FileNames.append("H-6.00 K-0.50 L 0.00")
FileNames.append("H-6.00 K-0.40 L 0.00")
FileNames.append("H-6.00 K-0.30 L 0.00")
FileNames.append("H-6.00 K-0.20 L 0.00")
FileNames.append("H-6.00 K-0.10 L 0.00")
FileNames.append("H-6.00 K 0.00 L 0.00")
FileNames.append("H-6.00 K 0.10 L 0.00")
FileNames.append("H-6.00 K 0.20 L 0.00")
FileNames.append("H-6.00 K 0.30 L 0.00")
FileNames.append("H-6.00 K 0.40 L 0.00")
FileNames.append("H-6.00 K 0.50 L 0.00")
FileNames.append("H-6.00 K 0.60 L 0.00")
FileNames.append("H-6.00 K 0.70 L 0.00")
FileNames.append("H-6.00 K 0.80 L 0.00")
FileNames.append("H-6.00 K 0.90 L 0.00")
FileNames.append("H-6.00 K 1.00 L 0.00")
'''
Temp=240
estep=0.25

H=np.zeros(len(FileNames))
print(FileNames[1][8:13])
#for i in range (0,len(FileNames)):
    #H[i]=eval(FileNames[i][8:13])+5
#print(FileNames[1][1:5])
#for i in range (0,len(FileNames)):
#    H[i]=eval(FileNames[i][1:5])
    


datasetdir='E:/Bagage22/Bagage_22_TA/subtr_background/'
datasetdir=location_ForPlots
#datasetdir='E:/Data_LSNO_120meV_'+str(Temp)+'K/Longitudinal_110_binH01K005/subtr_background/'
#datasetdir='E:/Data_LSNO_120meV_'+str(Temp)+'K/Transverse_LSNO100/subtr_background/'
'''


datasetdir.append('E:/Data_LSNO_120meV_10K/StretchingTests0/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_190K/StretchingTests0/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_240K/StretchingTests0/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_300K/StretchingTests0/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_450K/StretchingTests0/good_slices/')
datasetdir.append('E:/Data_LSNO_120meV_600K/StretchingTests0/good_slices/')

datasetdir.append('E:/Data_LSNO_120meV_10K/StretchingTests0/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_190K/StretchingTests0/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_240K/StretchingTests0/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_300K/StretchingTests0/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_450K/StretchingTests0/subtr_background/')
datasetdir.append('E:/Data_LSNO_120meV_600K/StretchingTests0/subtr_background/')

NumDir=6

      

Norm=[1,1,1,0.75,0.75,0.75]
'''
offset=3000.000



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
for i in range(0,len(FileNames)):
    AllData=np.genfromtxt(datasetdir+FileNames[i])
    energy=AllData[:,][:,0]
    energyMin=min(np.amin(energy),energyMin)
    energyMax=max(np.amax(energy),energyMax)
print(energyMin,energyMax)
energy0=np.zeros(int((energyMax-energyMin)/estep)+1)
intensity0=np.zeros((len(energy0),len(FileNames)))
error0=np.zeros((len(energy0),len(FileNames)))
for i in range(0,len(energy0)):
    energy0[i]=energyMin+i*estep
#print(energy0)
T=1
for i in range(0,len(FileNames)):
    AllData=np.genfromtxt(datasetdir+FileNames[i])
    intensity=AllData[:,][:,1]
    energy=AllData[:,][:,0]
    error=AllData[:,][:,2]

    for j in range(0,len(energy)-1):
        for jj in range(0,len(energy0)):
            if np.isclose(energy0[jj],energy[j], rtol=0.0001):
                index=jj
#        intensity0[index,i]=(7.0/H[i])*(7.0/H[i])*intensity[j]/(1+1/(np.exp(energy[j]/(0.08617*T))-1))+i*offset
#        error0[index,i]=(7.0/H[i])*(7.0/H[i])*error[j]/(1+1/(np.exp(energy[j]/(0.08617*T))-1))
                intensity0[index,i]=intensity[j]/(1+1/(np.exp(energy[j]/(0.08617*T))-1))#+i*offset
                error0[index,i]=error[j]/(1+1/(np.exp(energy[j]/(0.08617*T))-1))

print(intensity0)
StringArray=[]
for j in range(0,len(energy0)):
    string=str(energy0[j])
    for i in range(0,len(FileNames)):
        string+=(','+str(intensity0[j,i]))#+','+str(error0[j,i]))
    string+='\n'
    StringArray.append(string)
print(location_ForPlots)
if not os.path.isdir(location_ForPlots):
    os.makedirs(location_ForPlots)
T=10
TxtFile=open(location_ForPlots+'/Disp.csv','w+')
FirstLine='0'
#for i in range(len(FileNames)):
#    FirstLine+=','+str(H[i])#+','+str(H[i])
#FirstLine+='\n'
#TxtFile.write(FirstLine)
for i in range (0,len(energy0)):
    TxtFile.write(StringArray[i])
    print(StringArray[i])
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

