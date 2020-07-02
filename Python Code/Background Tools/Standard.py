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

#IMPORTANT: This algorithm will work only if the u-v matrix vectors are [1 0 0],[0,1,0], or [0 0 1]
    
    def __init__(self,h,k,l,params,index): #h,k,l for the dataset for which background is being calculated
        #self.Qslash gives the values of the wavevector (in r.l.u) used for background determination
        #index allows the calling program to pass how many times this routine has been called.
        self.params=params
        self.H=h
        self.K=k
        self.L=l

        Pperp=np.cross(params.Projection_u,params.Projection_v)
        
        uA=2*math.pi*(params.Projection_u[0]*h/self.params.a+params.Projection_u[1]*k/self.params.b+params.Projection_u[2]*l/self.params.c)
        vA=2*math.pi*(params.Projection_v[0]*h/self.params.a+params.Projection_v[1]*k/self.params.b+params.Projection_v[2]*l/self.params.c)
        pA=2*math.pi*(Pperp[0]*h/self.params.a+Pperp[1]*k/self.params.b+Pperp[2]*l/self.params.c)

        self.a_star=2*math.pi*(params.Projection_u[0]/self.params.a+params.Projection_u[1]/self.params.b+params.Projection_u[2]/self.params.c)
        self.b_star=2*math.pi*(params.Projection_v[0]/self.params.a+params.Projection_v[1]/self.params.b+params.Projection_v[2]/self.params.c)
        self.c_star=2*math.pi*(Pperp[0]/self.params.a+Pperp[1]/self.params.b+Pperp[2]/self.params.c)
        Angles=self.GeneratePhiTheta()
        Phi=Angles[0]
        Theta=Angles[1]
        phiInDegrees=Phi*180/math.pi
        thetaInDegrees=Theta*180/math.pi

        self.flag=0 #Setting the flag to 1 will stop background file generation, inactive in the Standard algorithm
        self.mult=1 #Allows to set the multiplyer for intensity and error in backgound files (Typically to apply Q^2), inactive in the Standard algorithm
        
        #CalcQslash takes input in reciprocal angstoms, result returned in r.l.u
#        self.Qslash=self.CalcQslash(self.H*2*math.pi/self.params.a,self.K*2*math.pi/self.params.b,self.L*2*math.pi/self.params.c,Phi,Theta)
        self.Qslash=self.CalcQslash(uA,vA,pA,Phi,Theta)

        self.fileName=str("H%5.2f K%5.2f L%5.2f Phi%5.2f Theta%5.2f" % (self.Qslash[0],self.Qslash[1],self.Qslash[2],phiInDegrees,thetaInDegrees))
#        print (self.fileName)
#  REPLACE this line with the following that is commented out
#        fileName=str(RSE_Constants.FILENAME_FORMAT % (self.H,self.K,self.L))    

    def GeneratePhiTheta(self):

        offset_mid=max([2*math.pi/self.params.a,2*math.pi/self.params.b,2*math.pi/self.params.c])
        offset = random.uniform(0.8*offset_mid,3.5*offset_mid)
#        phiRange=max(0.4,numpy.atan(offset/Qabs(H,K,L,a,b,c)))
        phiRange=math.atan(offset/self.Qabs())
        phiRangeC=min(phiRange,1)

        randomXi=random.uniform(0,2*math.pi)
        mult=1
        if math.cos(randomXi)<0:
            mult=-1
              
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

        Qu_plane=math.sqrt(Qu*Qu+Qv*Qv)*math.cos(randomTheta)+Qp*math.sin(randomTheta)
        Q_outOfPlane1slash=Qp*math.cos(randomTheta)-math.sqrt(Qu*Qu+Qv*Qv)*math.sin(randomTheta)

        Qu2slash=Qu_plane*Qu/math.sqrt(Qu*Qu+Qv*Qv)
        Qv2slash=Qu_plane*Qv/math.sqrt(Qu*Qu+Qv*Qv)

        Qu1slash=Qu2slash*math.cos(randomPhi)-Qv2slash*math.sin(randomPhi)
        Qv1slash=Qu2slash*math.sin(randomPhi)+Qv2slash*math.cos(randomPhi)
              
              
        hslash=Qu1slash/self.a_star
        kslash=Qv1slash/self.b_star
        lslash=Q_outOfPlane1slash/self.c_star
        Qslash=[hslash,kslash,lslash]
        Qs_s0=Qu**2+Qv**2+Qp**2
        Qs_s=Qu1slash**2+Qv1slash**2+Q_outOfPlane1slash**2
#        print(math.sqrt(Qs_s))
#        print(math.sqrt(Qs_s0))
        return Qslash
