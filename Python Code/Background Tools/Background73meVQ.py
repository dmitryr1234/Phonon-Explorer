from TextFile import *
import numpy
from numpy import *
import math
import os
import random
import io
import matlab.engine
from RSE_Constants import *

########## Here the background is at L=10


#This class deals with generation of wavevectors used for background determination
class BackgroundQ:
    def __init__(self,h,k,l,params): #h,k,l for the dataset for which background is being calculated
        #self.Qslash gives the values of the wavevector (in r.l.u) used for background determination
        self.params=params
        self.H=h
        self.K=k
        self.L=l

        #CalcQslash takes input in reciprocal angstoms, result returned in r.l.u
        self.Qslash=self.CalcQslash()
        self.fileName=str("H%5.2f K%5.2f L%5.2f" % (self.Qslash[0],self.Qslash[1],self.Qslash[2]))
#  REPLACE this line with the following that is commented out
#        fileName=str(RSE_Constants.FILENAME_FORMAT % (self.H,self.K,self.L))    

    def Qabs(self):
        Qx=self.H*2*math.pi/self.params.a
        Qz=self.K*2*math.pi/self.params.b
        Qy=self.L*2*math.pi/self.params.c
        A=sqrt(Qx**2+Qy**2+Qz**2)
        return A

    def CalcQslash(self):

#a-lattice param along proj.u, b- along proj.v
              
        
        kslash=self.K
        lslash=10
        if (self.Qabs()>((lslash*2*math.pi/self.params.c)**2-(kslash*2*math.pi/self.params.a)**2)**0.5):
            hslash=-((self.Qabs()**2-(lslash*2*math.pi/self.params.c)**2-(kslash*2*math.pi/self.params.a)**2)**0.5)*self.params.a/(2*math.pi)
        else:
            hslash=0
        Qslash=[hslash,kslash,lslash]
#        Qs_s0=Qu**2+Qv**2+Qp**2
#        Qs_s=Qu1slash**2+Qv1slash**2+Qp1slash**2
#        print(math.sqrt(Qs_s))
#        print(math.sqrt(Qs_s0))
        return Qslash
