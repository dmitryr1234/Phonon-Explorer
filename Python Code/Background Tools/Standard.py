#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%



from TextFile import *
import numpy
from numpy import *
import math
import os
import random
import io
from RSE_Constants import *

#This class deals with generation of wavevectors used for background determination
class BackgroundQ:
    def __init__(self,h,k,l,params): #h,k,l for the dataset for which background is being calculated
        #self.Qslash gives the values of the wavevector (in r.l.u) used for background determination
        self.params=params
        self.H=h
        self.K=k
        self.L=l
        Angles=self.GeneratePhiTheta()
        Phi=Angles[0]
        Theta=Angles[1]
        phiInDegrees=Phi*180/math.pi
        thetaInDegrees=Theta*180/math.pi

        #CalcQslash takes input in reciprocal angstoms, result returned in r.l.u
        self.Qslash=self.CalcQslash(self.H*2*math.pi/self.params.a,self.K*2*math.pi/self.params.b,self.L*2*math.pi/self.params.c,Phi,Theta)
        self.fileName=str("H%5.2f K%5.2f L%5.2f Phi%5.2f Theta%5.2f" % (self.Qslash[0],self.Qslash[1],self.Qslash[2],phiInDegrees,thetaInDegrees))
#  REPLACE this line with the following that is commented out
#        fileName=str(RSE_Constants.FILENAME_FORMAT % (self.H,self.K,self.L))    

    def GeneratePhiTheta(self):
        offset = random.uniform(0.5*max([2*math.pi/self.params.a,2*math.pi/self.params.b,2*math.pi/self.params.c]),1.5*max([2*math.pi/self.params.a,2*math.pi/self.params.b,2*math.pi/self.params.c]))
#        phiRange=max(0.4,numpy.atan(offset/Qabs(H,K,L,a,b,c)))
        phiRange=math.atan(offset/self.Qabs())
        phiRangeC=min(phiRange,1)

        randomXi=random.uniform(0,2*math.pi)
        mult=-1
#        if math.cos(randomXi)<0:
#            mult=-1
              
        randomPhi=phiRangeC*math.cos(randomXi)
        randomTheta=phiRangeC*math.sin(randomXi)
        
#        randomPhi=phiRangeC*mult
#        randomTheta=0
        return [randomPhi,randomTheta]
    def Qabs(self):
        Qx=self.H*2*math.pi/self.params.a
        Qz=self.K*2*math.pi/self.params.b
        Qy=self.L*2*math.pi/self.params.c
        A=sqrt(Qx**2+Qy**2+Qz**2)
        return A

    def CalcQslash(self,Qu,Qv,Qp,randomPhi,randomTheta):

#a-lattice param along proj.u, b- along proj.v

        Qu_p=math.sqrt(Qu*Qu+Qp*Qp)*math.cos(randomTheta)+Qv*math.sin(randomTheta)
        Qv1slash=Qv*math.cos(randomTheta)-math.sqrt(Qu*Qu+Qp*Qp)*math.sin(randomTheta)

        Qu2slash=Qu_p*Qu/math.sqrt(Qu*Qu+Qp*Qp)
        Qp2slash=Qu_p*Qp/math.sqrt(Qu*Qu+Qp*Qp)

        Qu1slash=Qu2slash*math.cos(randomPhi)-Qp2slash*math.sin(randomPhi)
        Qp1slash=Qu2slash*math.sin(randomPhi)+Qp2slash*math.cos(randomPhi)
              
              
        hslash=Qu1slash*self.params.a/(2*math.pi)
        kslash=Qv1slash*self.params.b/(2*math.pi)
        lslash=Qp1slash*self.params.c/(2*math.pi)
        Qslash=[hslash,kslash,lslash]
        Qs_s0=Qu**2+Qv**2+Qp**2
        Qs_s=Qu1slash**2+Qv1slash**2+Qp1slash**2
#        print(math.sqrt(Qs_s))
#        print(math.sqrt(Qs_s0))
        return Qslash
