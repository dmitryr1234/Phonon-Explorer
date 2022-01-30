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

#ProjectDir='StretchingTests100'
ProjectDir='Longitudinal_110_bin01'

location_ForPlots='E:/Data_LSNO_120meV_240K/'+ProjectDir + '/temp450/'
if not os.path.isdir(location_ForPlots):
    os.makedirs(location_ForPlots)



#datasetdir1='E:/Data_LSNO_120meV_240K/'+ProjectDir + '/good_slices/'
#datasetdir2='E:/Data_LSNO_120meV_450K/'+ProjectDir + '/good_slices/'
datasetdir1='E:/Data_LSNO_120meV_240K/'+ProjectDir + '/subtr_background/'
datasetdir2='E:/Data_LSNO_120meV_450K/'+ProjectDir + '/subtr_background/'

      
filenames1=[file for file in os.listdir(datasetdir1) if file.startswith("H")and not file.endswith("pdf")]
filenames2=[file for file in os.listdir(datasetdir2) if file.startswith("H")and not file.endswith("pdf")]
print (filenames1)
print (filenames2)
T1=10
T2=10
M1=1
M2=1
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
for i in range(0,len(filenames1)):
    for j in range(0,len(filenames2)):
        if filenames1[i]==filenames2[j]:
           print(filenames1[i],filenames2[j])
        
           AllData1=np.genfromtxt(datasetdir1+filenames1[i])
           intensity1=AllData1[:,][:,1]
           energy1=AllData1[:,][:,0]
           error1=AllData1[:,][:,2]
           for ii in range(0,len(energy1)):
               intensity1[ii]=M1*intensity1[ii]/(1+1/(np.exp(energy1[ii]/(0.08617*T1))-1))
               error1[ii]=M1*error1[ii]/(1+1/(np.exp(energy1[ii]/(0.08617*T1))-1))

           AllData2=np.genfromtxt(datasetdir2+filenames2[j])
           intensity2=AllData2[:,][:,1]
           energy2=AllData2[:,][:,0]
           error2=AllData2[:,][:,2]
           for ii in range(0,len(energy2)):
               intensity2[ii]=M2*intensity2[ii]/(1+1/(np.exp(energy2[ii]/(0.08617*T2))-1))
               error2[ii]=M2*error2[ii]/(1+1/(np.exp(energy2[ii]/(0.08617*T2))-1))
#               print 1.0+1/(np.exp(energy2[ii]/(0.08617*T2))-1.0)

#           plt.figure(figsize=(8.27,11.69,))
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

