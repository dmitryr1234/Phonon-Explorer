#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


import os
import PyPDF2 
from PyPDF2 import PdfFileReader, PdfFileMerger
from RSE_Constants import *


class Display:
    def MakePlotSummary(self,folder,subdir):
        files_dir = folder
        name=RSE_Constants.NOT_STARTS_WITH+subdir+RSE_Constants.ALL_PLOTS
#        if(1==1):
        try: 
            pdf_files = [f for f in sorted(os.listdir(files_dir)) if f.startswith(RSE_Constants.STARTS_WITH) and f.endswith(RSE_Constants.ENDS_WITH) and not f.startswith(RSE_Constants.NOT_STARTS_WITH)]
            merger = PdfFileMerger()

            for filename in pdf_files:
                merger.append(PdfFileReader(os.path.join(files_dir, filename), "rb"))

            merger.write(os.path.join(files_dir, name))
        except Exception as e:
            print ("MakePlotsSumary failed in "+folder)
            print(e)
