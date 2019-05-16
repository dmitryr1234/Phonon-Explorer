#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%


import os.path

#All constants and paths

class RSE_Constants():


    INPUTS_PATH_MAIN = os.path.normpath('/home/asquiggle/Phonon-Explorer/Input_Files')
    INPUTS_FILENAME_MAIN = r'InputParameters.txt'
    FITTING_PARAM_FILE = r'_FittingParam.txt'
    
    INPUTS_PATH = INPUTS_PATH_MAIN
    INPUTS_FILENAME = r'InputParameters.txt'
    BACKGR_PREFIX = r'B_'
    
    BACKGROUND_SUBTRACTED_FOLDER = r'randomGoodFilesForBackground'
    ALL_FILES_APPEND = r'_AllFilesWithBackground.pdf'
    SAVE_BACK = r'_Background.pdf'
    ALL_PLOTS = r'_ALLPlots.pdf'
    STARTS_WITH = r'H'
    ENDS_WITH = r'.pdf'
    NOT_STARTS_WITH = r'x'
    
    #Plots
    X_LABEL = r'Energy'
    Y_LABEL = r'Intensity'
    SYMBOL = ['*','+','o','^','r*','r+','ro','r^','b*','b+','bo','b^','g*','g+','go','g^','*','+','o','^','r*','r+','ro','r^','b*','b+','bo','b^','g*','g+','go','g^','*','+','o','^','r*','r+','ro','r^','b*','b+','bo','b^','g*','g+','go','g^']
    
    #Raw Slices
    SLICE_TEMP_DIRECTORY = os.path.normpath('E:/TestData/450K_Data/Temp') #Not used in this version
    GEN_FOLDER = 'randomGoodFilesForBackground_'

    #Data.py
    DIR_FORMAT = r'H%5.2f K%5.2f L%5.2f/'
    FILENAME_FORMAT = r'H%5.2f K%5.2f L%5.2f'
    FLAG=0 #Never change this

    #FittingData.py
    TEMP_FILE = r'guru99.py'

    #SaveParamtoTxt.py
    FINAL_FIT_PARAMS = r'FinilFittingParam.txt'

    

    
