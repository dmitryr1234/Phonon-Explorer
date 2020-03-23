
from TextFile import *
from Data import *
import re
import os
import math
import time
from numpy import *
from RSE_Constants import *


params=Parameters(RSE_Constants.INPUTS_PATH,RSE_Constants.INPUTS_FILENAME)

dataFileNames=[file for file in os.listdir(params.folderForBkgSubtractedFiles) if file.startswith("H") and not file.endswith("pdf")]
Data=Dataset(params.folderForBkgSubtractedFiles,[dataFileNames[0]])
TxtFile=open(params.folderForBkgSubtractedFiles+"BackgroundAdjustment.txt",'w+')

for i in range(0,len(dataFileNames)):
    Q=Data.ExtractQfromFileName(dataFileNames[i])
    TxtFile.write(str(Q[0])+'  '+str(Q[1])+'  '+str(Q[2])+"  0"+'\n')
TxtFile.close()
