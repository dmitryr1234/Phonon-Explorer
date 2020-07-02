from TextFile import *
import numpy
from numpy import *
import math
import os
import random
import io
import matlab.engine
from RSE_Constants import *

#This class deals with generation of wavevectors used for background determination
class BackgroundQ:
    def __init__(self,h,k,l,params,index): #h,k,l for the dataset for which background is being calculated
        #self.Qslash gives the values of the wavevector (in r.l.u) used for background determination
        #index enumerates how many time it has been called already. It allows the module to return
        #different values each time.
        self.params=params
        self.H=h
        self.K=k
        self.L=l
        self.index=index
        self.mult=1
        self.flag=0
        #CalcQslash takes input in reciprocal angstoms, result returned in r.l.u
        self.Qslash=self.CalcQslash()
#        print (self.Qslash)
#        self.fileName=str("H%5.2f K%5.2f L%5.2f" % (self.Qslash[0],self.Qslash[1],self.Qslash[2]))
#  REPLACE this line with the following that is commented out
        if self.flag==0:
            self.fileName=str(RSE_Constants.FILENAME_FORMAT % (self.Qslash[0],self.Qslash[1],self.Qslash[2]))    

    def Qabs(self):
        Qx=self.H*2*math.pi/self.params.a
        Qz=self.K*2*math.pi/self.params.b
        Qy=self.L*2*math.pi/self.params.c
        A=sqrt(Qx**2+Qy**2+Qz**2)
        return A

    def CalcQslash(self):

#a-lattice param along proj.u, b- along proj.v

#Users edit this function ONLY
#
        if self.index>6: #This statement controls when to stop generating Q's. In this
            self.flag=1    #example it will stop after 7 times (6+1).
            return

# Here we want to read off background from the minimum intensty of
# the following Q's: [-5,1,0],[-5,-1,0],[-6,0,0],[-6,-1,0],[-6,1,0],[-7,1,0], and [-7,-1,0]

        hs=[-5,-5,-6,-6,-6,-7,-7]
        ks=[1,-1,0,-1,1,1,-1]

        hslash=hs[self.index]
        kslash=ks[self.index]

        lslash=0
#        lslash=((self.Qabs()**2-(hslash*2*math.pi/self.params.a)**2-(kslash*2*math.pi/self.params.a)**2)**0.5)*self.params.c/(2*math.pi)

        Qslash=[hslash,kslash,lslash]
        if self.H>=-6 and hslash==-5:
            self.mult=1+(abs(self.H)-5)*.1
        if self.H>=-6 and hslash==-6:
            self.mult=1+(abs(self.H)-6)*.09
        if self.H>=-6 and hslash==-7:
            self.mult=0.82+(abs(self.H)-6)*.09
        if self.H<-6 and hslash==-5:
            self.mult=1.1*(1+(abs(self.H)-6)*.2)
        if self.H<-6 and hslash==-6:
            self.mult=1+(abs(self.H)-5)*.2
        if self.H<-6 and hslash==-7:
            self.mult=1+(abs(self.H)-7)*.2
            
        return [hslash,kslash,lslash]
