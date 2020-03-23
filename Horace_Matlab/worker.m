function worker(class_name,job_controls_string)
% function used as standard worker to do a job in different matlab
% session
%
% To work, should be present on a data searh path, before Herbert is
% initialized as may need to initialize Herbert and Horace itself
%
%Inputs:
% class_name -- the name of the class, which do the job. The class
%               should inherit from JobExecutor and overload
%               do_job method
%
% job_controls_string - the structure, containining information, necessary to
%              initiate job
%
%
if isempty(which('herbert_init.m'))
    horace_on();
end
% Check current state of mpi framework and set up deployment status

mis = MPI_State.instance();
mis.is_deployed = true;
is_tested = mis.is_tested;
% for testing, production job should just finish itself
clot = onCleanup(@()(setattr(mis,'is_deployed',false)));


je = feval(class_name);

[je,job_arguments,err_mess]=je.init_worker(job_controls_string);

if ~isempty(err_mess)
    % clear all existing messages for this job
    je.receive_all_messages();
    
    mess = aMessage('failed');
    mess.payload = sprintf('job N%d failed at init_worker. Reason: %s',...
        je.job_id,err_mess);
    je.send_message(mess);
    if ~is_tested
        exit;
    else
        error('WORKER:init_worker',mess.payload)
    end
end
%
mis.logger = @(step,n_steps,time,add_info)...
    (je.log_progress(step,n_steps,time,add_info));

mis.check_cancelled = @()(f_canc(je));
%
%
try
    if iscell(job_arguments)
        je = je.do_job(job_arguments{:});
    else
        je = je.do_job(job_arguments);
    end
catch ME
    if ~strcmpi(ME.identifier,'MESSAGE_FRAMEWORK:cancelled')
        % clear all existing messages for this job
        je.receive_all_messages();
        
        mess = aMessage('failed');
        mess.payload = sprintf('job N%d failed at do_job method. Reason: %s',...
            je.job_id,ME.message);
        je.send_message(mess);
    end
    if ~is_tested
        exit;
    else
        error('WORKER:do_job',mess.payload)
    end
end
%
je.finish_job();

if ~is_tested
    exit;
end

end

function f_canc(job_executor)
    if job_executor.is_job_cancelled()
        error('MESSAGE_FRAMEWORK:cancelled','Messages framework has been cancelled or not initialized any more')
    end
end