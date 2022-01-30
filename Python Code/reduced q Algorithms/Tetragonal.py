#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#   Dmitry Reznik, Irada Ahmadova, Aaron Sokolik, Ty Sterling            %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


import math

#First two components of q and Q (h and k) are along symmetry-equivalent directions

class Smallq: #Dataset can be either a single cut at one Q or several cuts put together for the purposes of multizone fitting,

    def __init__(self,Q):
        smallH=self.ConvertToSmallH(Q[0])
        smallK=self.ConvertToSmallH(Q[1])
        smallL=self.ConvertToSmallH(Q[2])
        self.q=[smallH,smallK,smallL]
        if (smallH<smallK):
            self.q=[smallK,smallH,smallL]
        self.GenerateSmallQList()

    def ConvertToSmallH(self,H):
        qh,Gh=math.modf(H)
        qh=(abs(qh))
        if qh>0.5:
            qh=1-qh
        return qh

    def GenerateSmallQList(self):
        self.qlist=[self.q]
        if self.q[0]!=self.q[1]:
            self.qlist.append([self.q[1],self.q[0],self.q[2]])
        for i in range(0,len(self.qlist)):
            print(self.qlist[i])
            
        
