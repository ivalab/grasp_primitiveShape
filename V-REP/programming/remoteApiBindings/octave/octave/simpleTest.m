% Make sure to have the server side running in V-REP: 
% in a child script of a V-REP scene, add following command
% to be executed just once, at simulation start:
%
% simRemoteApi.start(19999)
%
% then start simulation, and run this program.
%
% IMPORTANT: for each successful call to simxStart, there
% should be a corresponding call to simxFinish at the end!

function simpleTest()
    disp('Program started');
    vrep=remApiSetup();
    simxFinish(-1); % just in case, close all opened connections
    clientID=simxStart('127.0.0.1',19999,true,true,5000,5);
    if (clientID>-1)
        disp('Connected to remote API server');

        % Now try to retrieve data in a blocking fashion (i.e. a service call):
        [res,objs]=simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking);
        if (res==vrep.simx_return_ok)
            fprintf('Number of objects in the scene: %d\n',length(objs));
        else
            fprintf('Remote API function call returned with error code: %d\n',res);
        end
            
        pause(2);

        % Now retrieve streaming data (i.e. in a non-blocking fashion):
        t=clock;
        startTime=t(6);
        currentTime=t(6);
        simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_streaming); % Initialize streaming
        while (currentTime-startTime < 5)   
            [returnCode,data]=simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_buffer); % Try to retrieve the streamed data
            if (returnCode==vrep.simx_return_ok) % After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
                fprintf('Mouse position x: %d\n',data); % Mouse position x is actualized when the cursor is over V-REP's window
            end
            t=clock;
            currentTime=t(6);
        end
            
        % Now send some data to V-REP in a non-blocking fashion:
        simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot);

        % Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
        simxGetPingTime(clientID);

        % Now close the connection to V-REP:    
        simxFinish(clientID);
    else
        disp('Failed connecting to remote API server');
    end
    disp('Program ended');
end
