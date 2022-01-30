#________________________________________________________________________%
#              University of Colorado Boulder                            %
#                                                                        %
#              Dmitry Reznik, Irada Ahmadova, Aaron Sokolik                             %       
#                                                                        %
#    Work supported by the DOE, Office of Basic Energy Sciences,         %
#    Office of Science, under Contract No. DE-SC0006939                  %                  
#________________________________________________________________________%

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !                                                                         !
# !         This file was added by Tyler Sterling on 08.04.2021             !
# !                                                                         !
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# system modules
import numpy
from scipy.ndimage import gaussian_filter

# custom modules
from TextFile import *
from Data import *
from plotDataWithFit import *
from RSE_Constants import *
from FitParameters import *

# ------------------------------------------------------------------------------------------------

class SmoothedBackground:

    """
    DESCRIPTION: 

    from a set of cuts for bg determination, find the smooth background as follows:

        1. interpolate eacg cut onto a coarse, uniformly spaced energy grid. this is needed
            since the gaussian_filter in scipy expects uniform spacing.
        2. use gaussian convolution to 'smooth' the data in the cut. the gaussian width is the
            'Resolution' variable from the Input_Parameters file. It has dimensions of energy
            and is the standard deviation of the gaussian_kernel.
        3. interpolate the 'smoothed' data onto a fine spaced energy grid. the fine grid is
            commensurate for all cuts so that it is straight forward to do the point-by-point
            minumum. note, values outside the bounds of the interpolated data are set to an
            extremely high value (RSE_Constants.INTERPOLATION_MASK) so that the point-by-point min.
            selects the smooth data from the cuts with the largest extent in energy.
        4. downsample the smoothed data onto the original energy grid of the raw data file
            (again using interpolation ...). this is the background that is subtracted from the raw data
            to determining the bg subtracted data that is written to the subtr_background directory.

    WARNING: 

    in retrospect, I should have used the 'Data' class to read/write the files. 
    if the format of the files changes, this whole file will be broken. it won't be hard to 
    fix in the future if this happens. if any issues arise, contact Ty at ty.sterling@colorado.edu

    TODO: 

        1. this does not currently do any linear subtraction or constant subtraction. i noticed that 
            Background.Background does it, but i havent really looked carefully at how it works. i 
            can add it later if it is needed.
    """

    # ------------------------------------------------------------------------------------------------

    def __init__(self,folder):

        """
        loop over all files in the bg folder and select which ones are cuts for bg determination (i.e. 
        not fit* or *.pdf files, etc.)
        """

        # the directory where the bg data are.
        self.bg_folder = folder

        # get the cuts for bg determination in the folder
        self.bg_files = []
        ls = os.listdir(folder)
        for f_name in ls:
            if f_name.startswith(RSE_Constants.STARTS_WITH) and not \
                    f_name.endswith(RSE_Constants.ENDS_WITH):
                self.bg_files.append(f_name)
        
    # ================================================================================================
    # ------------------------------------------------------------------------------------------------
    # the stuff below here is to determine the background and write the files
    # ------------------------------------------------------------------------------------------------
    # ================================================================================================

    def smooth_cuts_for_this_Q(self,params,rawFileName):

        """
        loop over the bg files and get the smoothed, fine data for each. write the data to files.
        """

        # the gaussian smoothing width
        self.sigma = params.Resolution

        sf_data = [] # this will hold all of the smooth, fine bg data for this raw file

        for bg_file in self.bg_files:

            # load the file
            bg_file_path = os.path.join(self.bg_folder,bg_file)
            bg_data = np.loadtxt(bg_file_path)

            # go and actually do the smoothing
            fine_e, sf_int = self._smooth_cut(bg_data)
            sf_data.append(sf_int)

            # write the smooth, fine data to a file for later plotting
            self._write_smooth_file(fine_e,sf_int,bg_file)

        # get the point-by-point minimum of the smoothed data
        pbp_min = np.array(sf_data).min(axis=0)
        self._write_smooth_file(fine_e,pbp_min,'pbp_min')

        # now go and write the 'B_' files
        self._write_background(fine_e,pbp_min,params.path_data,rawFileName)

    # ------------------------------------------------------------------------------------------------
    # private methods for determining background and writing files below here
    # ------------------------------------------------------------------------------------------------
    
    def _smooth_cut(self,bg_data):

        """
        actually do the smoothing. return the fine energy grid and the smoothed data.
        """
        
        # get the coarse, uniformly spaced energy grid
        coarse_e_step = (bg_data[1:,0]-bg_data[:-1,0]).min() # smallest e_step in the file
        coarse_e_min = bg_data[:,0].min() 
        coarse_e_max = bg_data[:,0].max()
        coarse_e_grid = np.arange(coarse_e_min,coarse_e_max+coarse_e_step,coarse_e_step)

        # interpolate the intensities onto the coarse grid
        coarse_int = np.interp(coarse_e_grid,bg_data[:,0],bg_data[:,1])

        # now smooth with gaussian interpolation
        smooth_int = gaussian_filter(coarse_int,self.sigma) 

        # get the fine energy grid to interpolate smoothed data onto. the parameters are the same 
        # for all files. they are read from RSE_Constants
        fine_e_step = RSE_Constants.E_STEP
        fine_e_min = RSE_Constants.E_MIN
        fine_e_max = RSE_Constants.E_MAX
        fine_e_grid = np.arange(fine_e_min,fine_e_max+fine_e_step,fine_e_step)

        # now interpolate the smooth intensity onto the fine grid
        interp_mask = RSE_Constants.INTERPOLATION_MASK
        fine_int = np.interp(fine_e_grid,coarse_e_grid,smooth_int,left=interp_mask,right=interp_mask)

        return fine_e_grid, fine_int

    # ------------------------------------------------------------------------------------------------

    def _write_smooth_file(self,fine_e,sf_int,bg_file):

        """
        write the smoothed bg on the fine grid to a file named 'smooth_H * K * L * Phi * Theta *' in 
        the randomFilesForBackground directory. the data are trimmed so that all of the interpolated
        intensity that are out of bounds are not written. 
        """

        # the file name. it is the file name that was read prepended with 'smooth_'
        smooth_file = os.path.join(self.bg_folder,RSE_Constants.SMOOTHED_STARTS_WITH+bg_file)

        # trim the data where there was no intensity in the file.
        inds = np.argwhere(sf_int < RSE_Constants.INTERPOLATION_MASK*0.99).flatten()
        num_data = inds.shape[0]
        fine_e = fine_e[inds].reshape(num_data,1)
        sf_int = sf_int[inds].reshape(num_data,1)

        # write the data to the smoothed data file
        out_data = np.append(fine_e,sf_int,axis=1)
        np.savetxt(smooth_file,out_data,fmt=RSE_Constants.OUTPUT_DATA_PRECISION)
    
    # ------------------------------------------------------------------------------------------------

    def _write_background(self,fine_e,pbp_min,raw_file_path,raw_file_name):

        """
        write the smoothed bg on the coarse grid in the raw data file to the 'B_H * K * L *' file in 
        the good_slices directory. the data are trimmed so that all of the interpolated intensities
        that are out of bounds are not written.
        """

        # the raw data file. we need to read it to determine the energy grid.
        raw_file = os.path.join(raw_file_path,raw_file_name)
        raw_data = np.loadtxt(raw_file)

        # trim the data where there is no intensity.
        inds = np.argwhere(pbp_min < RSE_Constants.INTERPOLATION_MASK*0.99).flatten()
        fine_e = fine_e[inds]
        pbp_min = pbp_min[inds]

        # the coarse e grid in the raw data file
        coarse_e = raw_data[:,0]
        num_data = coarse_e.shape[0]

        # down sample the bg onto the energy grid of the raw data
        bg = np.interp(coarse_e,fine_e,pbp_min)
        
        # the file to write.
        bg_file = os.path.join(raw_file_path,RSE_Constants.BACKGR_PREFIX+raw_file_name)

        # now write to the file
        coarse_e = coarse_e.reshape(1,num_data)
        bg = bg.reshape(1,num_data)
        out_data = np.append(coarse_e,bg,axis=0) # for some reason, the B_ file is written along axis 0
        np.savetxt(bg_file,out_data,fmt=RSE_Constants.OUTPUT_DATA_PRECISION)

    # ================================================================================================
    # ------------------------------------------------------------------------------------------------
    # the stuff below here reads the raw and bg files, subtracts the bg, and writes the bg subtracted
    # files to the subtr_background directory.
    # ------------------------------------------------------------------------------------------------
    # ================================================================================================

    def subtract_background(self,params,raw_file_name):

        """
        read the raw file, the B_ background file, subtracte the background from the raw data,
        and write the subtracted data to the subtr_background directory.
        """

        # enforce that the subtracted background folder exists
        subtr_path = os.path.join(params.projectRootDir,params.ProcessedDataName)
        subtr_path = os.path.join(subtr_path,'subtr_background')
        subtr_file = os.path.join(subtr_path,raw_file_name)
        if not os.path.exists(subtr_path):
            os.mkdir(subtr_path)

        # read the raw data
        raw_file = os.path.join(params.path_data,raw_file_name)
        raw_data = np.loadtxt(raw_file)

        # read the B_ file
        bg_file = os.path.join(params.path_data,RSE_Constants.BACKGR_PREFIX+raw_file_name)
        bg_data = np.loadtxt(bg_file).T # transpose since it is written with different format than data

        # subtract the background from the intensity
        raw_data[:,1] = raw_data[:,1]-bg_data[:,1]

        # now write the subtracted file
        np.savetxt(subtr_file,raw_data,fmt=RSE_Constants.OUTPUT_DATA_PRECISION)
    
    # ------------------------------------------------------------------------------------------------

    # ================================================================================================
    # ------------------------------------------------------------------------------------------------
    # the stuff below here is to read the files and make the plots. should be consistent with the 
    # plot file names written by Dmitrys Background class
    # ------------------------------------------------------------------------------------------------
    # ================================================================================================

    def plot_all_in_one(self,params,raw_file_name):

        """
        make the plot showing all bg data points + the pbp_min background
        """

        plot_with_bg = Plot(params) # class for making plots

        # the final background for this Q on the full fine grid
        bg_file = os.path.join(self.bg_folder,RSE_Constants.SMOOTHED_STARTS_WITH+'pbp_min')
        bg_data = np.loadtxt(bg_file)
        backgroundArray = []
        backgroundArray.append(bg_data[:,0])
        backgroundArray.append(bg_data[:,1])

        # make the plot showing all bg data points + the pbp_min background
        plot_with_bg.plotSingle(self.bg_folder,self.bg_folder,self.bg_files,
               backgroundArray,raw_file_name+'_all')

    # ------------------------------------------------------------------------------------------------

    def plot_raw_cut(self,params,raw_file_name):

        """
        make the plot showing the raw cut at the Q points + the pbp_min background
        """

        plot_with_bg = Plot(params) # class for making plots

        # the final background for this Q on the full fine grid
        bg_file = os.path.join(self.bg_folder,RSE_Constants.SMOOTHED_STARTS_WITH+'pbp_min')
        bg_data = np.loadtxt(bg_file)
        backgroundArray = []
        backgroundArray.append(bg_data[:,0])
        backgroundArray.append(bg_data[:,1])

        # make the plot showing all bg data points + the pbp_min background
        plot_with_bg.plotSingle(params.path_data,params.path_data,[raw_file_name],
               backgroundArray,raw_file_name)

    # ------------------------------------------------------------------------------------------------

    def plot_subtr_cut(self,params,raw_file_name):

        """
        make the plot of the bg subtracted data
        """

        plot_with_bg = Plot(params) # class for making plots

        # path to subtr_background
        subtr_path = os.path.join(params.projectRootDir,params.ProcessedDataName)
        subtr_path = os.path.join(subtr_path,'subtr_background/')

        # make the plot showing all bg data points + the pbp_min background
        plot_with_bg.plotSingle(subtr_path,subtr_path,[raw_file_name],FitResultsArray=0,
                title=raw_file_name)

    # ------------------------------------------------------------------------------------------------


