
from TextFile import *
from Data import *
from FittingFunction import *
from FittingData import *
from Display import *
import re
import os
import math
import time
from numpy import *
from WriteFinalParamToFile import *
from plotDataWithFit import *
from Background import *
import matplotlib.pyplot as plt
from RSE_Constants import *


def Adjust(H,K,L,Adjustment, maxY):
    filename=str(RSE_Constants.FILENAME_FORMAT % (H,K,L))
    data=Dataset(params.folderForBkgSubtractedFiles,[filename])
    data.SubtractConstant(Adjustment)
    dataFile=DataTextFile(params.folderForBkgSubtractedFiles,filename)
    dataFile.Write(data.Energy,data.Intensity,data.Error)
    plt.errorbar(data.Energy,data.Intensity,data.Error)
    plt.plot(data.Energy, data.Intensity, '*', label='data')
    plt.xlabel(RSE_Constants.X_LABEL)
    plt.ylabel(RSE_Constants.Y_LABEL)
    plt.title(filename)
                #plt.axis([0, 40, 0, 0.0005])
    plt.ylim((-0.001,maxY)) 
    plt.grid() 
    plt.savefig(params.folderForBkgSubtractedFiles+filename+'.pdf')
                #plt.show()
    plt.close()
    return

#factor=input('Enter factor (1 or -1):')

params=Parameters(RSE_Constants.INPUTS_PATH,RSE_Constants.INPUTS_FILENAME)

Qs=np.genfromtxt(params.folderForBkgSubtractedFiles+"BackgroundAdjustment.txt")
print(params.folderForBkgSubtractedFiles+"BackgroundAdjustment.txt")
QHlist=Qs[:,][:,0]
QKlist=Qs[:,][:,1]
QLlist=Qs[:,][:,2]
AdjustList=Qs[:,][:,3]

for i in range(0,len(QHlist)):
    Adjust(QHlist[i],QKlist[i],QLlist[i],float(AdjustList[i]),params.maxY)

folder=params.folderForBkgSubtractedFiles
#PlotDataWithFitting=PlotDataWithFitParamCustomFolder(params,folder,folder,folder)
Disp=Display()
Disp.MakePlotSummary(folder,params.ProcessedDataName)
