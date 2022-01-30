#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%

import math
import sys
import os
import io
import numpy as np  # !!!!
from RSE_Constants import *

class RawData: #Dataset can be either a single cut at one Q or several cuts put together for the purposes of multizone fitting,

    def __init__(self, params):


        import matlab.engine
        RSE_Constants.fileHandle=matlab.engine.start_matlab()
        RSE_Constants.fileHandle.addpath(os.getcwd()+'/Tools to access raw data/') # !!!!
        self.sqw_path=params.sqw_path # !!!!

        try: #This is needed only for Linux. Windows and Mac will though an exception, which is safely caught.
            dataFile = params.sqw_path
            HoracePath = params.HoracePath

            RSE_Constants.fileHandle.addpath(HoracePath)
            RSE_Constants.fileHandle.herbert_on()
            RSE_Constants.fileHandle.horace_on()
        except Exception as e:
            print("IGNORE THIS ERROR UNLESS RUNNING ON LINUX:", e)
        return
       


    def GetSlice(self, bin_h, bin_k, bin_l, bin_e, Projection_u, Projection_v):
        #Projection_u , v are passed as strings
        # RETURNS 1 if slice is not written, 0 if SUCCESS
        #eng = matlab.engine.start_matlab();
        import matlab.engine

        proj = dict(
            u=matlab.double(list(Projection_u)),
            v=matlab.double(list(Projection_v)),
            type='rrr',
            uoffset=matlab.double([0,0,0,0])
            )
        try:
            import StringIO
            out = StringIO.StringIO()
            err = StringIO.StringIO()
        except:
            out = io.StringIO()
            err = io.StringIO()

        
        self.Energy=[]
        self.Intensity=[]
        self.Error=[]
# The eval is to prevent the program from crashing when running with Python 2.7

#        bin_h_m = eval('matlab.double([*bin_h])')
#        bin_k_m = eval('matlab.double([*bin_k])')
#        bin_l_m = eval('matlab.double([*bin_l])')
#        bin_e_m = eval('matlab.double([*bin_e])')

        bin_h_m = matlab.double([bin_h])
        bin_k_m = matlab.double([bin_k])
        bin_l_m = matlab.double([bin_l])
        bin_e_m = matlab.double([bin_e])

        try:
            ourCut = RSE_Constants.fileHandle.Getslice( 
                self.sqw_path,  #### !!!!
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
        self.Intensity=np.zeros(NumPoints) # !!!!
        self.Error=np.zeros(NumPoints) # !!!!
        self.Energy=np.zeros(NumPoints) # !!!!

        for i in range(0,NumPoints-1):
            self.Energy[i]=ourCut['p'][i][0]
            self.Intensity[i]=ourCut['s'][i][0]
            self.Error[i]=ourCut['e'][i][0]
#        print(bin_h, bin_k, bin_l)
        return 0
