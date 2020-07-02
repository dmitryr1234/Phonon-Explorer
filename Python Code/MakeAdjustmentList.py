
from TextFile import *
from Data import *
import re
import os
import math
import time
from numpy import *
from RSE_Constants import *


params=Parameters(RSE_Constants.INPUTS_PATH,RSE_Constants.INPUTS_FILENAME)

folder=params.folderForBkgSubtractedFiles
#folder=params.path_data

dataFileNames=[file for file in os.listdir(folder) if file.startswith("H") and not file.endswith("pdf")]
Data=Dataset(folder,[dataFileNames[0]])
TxtFile=open(folder+"BackgroundAdjustment.txt",'w+')

for i in range(0,len(dataFileNames)):
    Q=Data.ExtractQfromFileName(dataFileNames[i])
    TxtFile.write(str(Q[0])+'  '+str(Q[1])+'  '+str(Q[2])+" "+sys.argv[1]+" "+sys.argv[2]+'\n')
TxtFile.close()
