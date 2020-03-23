function MakeHoraceCut()
     
% cut_sqw-Horace software command,for description please follow the link:
% http://horace.isis.rl.ac.uk/Manipulating_and_extracting_data_from_SQW_files_and_objects#cut_sqw

% sqw_path----Directory where the sqw file is stored (large datasets from time-of-flight neutron inelastic scattering spectrometer)

% save_xye - See http://horace.isis.rl.ac.uk/Manipulating_and_extracting_data_from_SQW_files_and_objects#save_xye

% locationForRandomFilesBGR---Directory where randomproj_100.u = [1 0 0];
proj_100.u = [1 0 0];
proj_100.v = [0 1 0];

proj_100.type = 'rrr';
proj_100.uoffset = [0,0,0,0];
sqw_path='E:/IPTS-12942/UD55_50meV_450K.sqw';
bin_e=[-0.5,0.5]

%    bin_e=[energy_start,deltaEnergy,energy_end+Offset*deltaEnergy];


        bin_l=[-0.5,0.5];
      
        bin_h=[-4.9,0.01,-2.1];
        
        bin_k=[-0.1,0.1];
  
                
                slice_2D= cut_sqw(sqw_path,proj_100,bin_h, bin_k, bin_l, bin_e)
                plot(slice_2D);
grid on;
keep_figure;
%                save_xye(slice_2D,sprintf(strcat(location_rawSlices,file)));
%                save_xye(slice_2D,strcat(location,file));

end