#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


import math

class Smallq: #Dataset can be either a single cut at one Q or several cuts put together for the purposes of multizone fitting,

    def __init__(self,Q):
        self.q=[self.ConvertToSmallH(Q[0]),self.ConvertToSmallH(Q[1]),self.ConvertToSmallH(Q[2])]

    def ConvertToSmallH(self,H):
        qh,Gh=math.modf(H)
        qh=(abs(qh))
        if qh>0.5:
            qh=1-qh
        return qh
