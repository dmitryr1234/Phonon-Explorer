function path=horace_on(non_default_path)
%  safely switches Horace on
%  horace_on()                         -- calls Horace with default settings
%  horace_on(non_default_horace_path)  -- calls Horace with non-default Horace folder;
%
%
% $Revision: 1588 $ ($Date: 2018-02-23 10:57:45 +0000 (Fri, 23 Feb 2018) $)
%

default_horace_path ='/home/asquiggle/Physics/ReznikLab/ISIS/Horace';
default_herbert_path='/home/asquiggle/Physics/ReznikLab/ISIS/Herbert';
default_spinw_path = '/home/asquiggle/Physics/ReznikLab/ISIS/spinW';

if exist('non_default_path','var') && (strcmpi(non_default_path,'where') || strcmpi(non_default_path,'which'))
    path = find_default_path(default_horace_path);
    return;
end

warn_state=warning('off','all');    % turn of warnings (so don't get errors if remove non-existent paths)
try
    horace_off();
catch
end
warning(warn_state);    % return warnings to initial state

% if spinW start up file exist, try to initialize it
sw_start = which('spinw_on.m');
if ~isempty(sw_start)
    spinw_on(default_spinw_path);
end

herbert_initated=~isempty(which('herbert_init.m'));

% if Herbert is not initiated, try to init it.
if ~herbert_initated
    try
        try_herbert_on(default_herbert_path);
    catch
        error('HORACE_ON:wrong_dependencies','Can not initiate Herbert');
    end
else % reinitialize Herbert on where it is now.
    her_path = fileparts(which('herbert_init.m'));
    herbert_on(her_path);
end

% init Horace
if nargin==1
    start_app(non_default_path);
else
    start_app(default_horace_path);
end
path = fileparts(which('horace_init.m'));

hc = hor_config();
if hc.is_default
%% make server-specific settings
%  hc.mem_chunk_size = 10000000;
%  hc.threads = 8;
%  hc.use_mex = 1;
   hc.force_mex_if_use_mex = 0;
%  hc.delete_tmp = 1;
end
hpc = hpc_config
if hpc.is_default
   hpc.use_mex_for_combine = 1;
%  hpc.mex_combine_thread_mode = 1;
%  hpc.mex_combine_buffer_size = 2048;
%  hpc.accum_in_separate_process = 1;
%  hpc.accumulating_process_num = 8;
end

warning('off','MATLAB:subscripting:noSubscriptsSpecified');

function start_app(path)
addpath(path);
horace_init;

function path =find_default_path(her_default_path)
path = which('horace_init.m');
if isempty(path)
    path = her_default_path;
    if ~exist(fullfile(path,'horace_init.m'),'file')
        path='';
    end
else
    path=fileparts(path);
end

function try_herbert_on(default_herbert_path)

if exist(default_herbert_path,'var')
    if ~isempty(default_herbert_path)
        herbert_on(default_herbert_path);
    else
        herbert_on();
    end
else
    herbert_on();
end

function path=herbert_on(non_default_path)
% The function intended to switch Herbert on and
% return the path were Herbert is resided or 
% empty string if Herbert has not been found
%
%
% The function has to be present in Matlab search path 
% and modified for each machine to know default Herbert location
%
%Usage:
%>>path=herbert_on(); 
%       enables Herbert and initiates Herbert default search path
%>>path=herbert_on('where'); 
%       reports current location of herbert or empty if not found
%
%>>path=herbert_on('a path'); 
%       initiates Herbert on non-default search path
%
%
%
%
her_default_path='/home/asquiggle/Physics/ReznikLab/ISIS/Herbert';
%
if exist('non_default_path','var') && (strcmpi(non_default_path,'where') || strcmpi(non_default_path,'which'))
    path = find_her_default_path(her_default_path);   
    return;
end
if nargin==1 
    start_herbert(non_default_path);    
else
    start_herbert(her_default_path);    
end
path = fileparts(which('herbert_init.m'));

% set up multiusers computer specific settings,
% namely settings which are common for all new users of the specific computer
% e.g.:
hec = herbert_config()
if hec.is_default
% hec.use_mex_C = true;
    hec.log_level = 1;
end


function start_herbert(path)

try
    herbert_off;
catch
end
addpath(path);
herbert_init;

function path =find_her_default_path(her_default_path)
path = which('herbert_init.m');
if isempty(path)
    path = her_default_path;
    if ~exist(fullfile(path,'herbert_init.m'),'file')
        path='';
    end
else
    path=fileparts(path);
end

