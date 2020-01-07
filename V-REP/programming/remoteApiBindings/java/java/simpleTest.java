// Make sure to have the server side running in V-REP: 
// in a child script of a V-REP scene, add following command
// to be executed just once, at simulation start:
//
// simRemoteApi.start(19999)
//
// then start simulation, and run this program.
//
// IMPORTANT: for each successful call to simxStart, there
// should be a corresponding call to simxFinish at the end!

import coppelia.IntW;
import coppelia.IntWA;
import coppelia.remoteApi;

public class simpleTest
{
    public static void main(String[] args)
    {
        System.out.println("Program started");
        remoteApi vrep = new remoteApi();
        vrep.simxFinish(-1); // just in case, close all opened connections
        int clientID = vrep.simxStart("127.0.0.1",19999,true,true,5000,5);
        if (clientID!=-1)
        {
            System.out.println("Connected to remote API server");   

            // Now try to retrieve data in a blocking fashion (i.e. a service call):
            IntWA objectHandles = new IntWA(1);
            int ret=vrep.simxGetObjects(clientID,vrep.sim_handle_all,objectHandles,vrep.simx_opmode_blocking);
            if (ret==vrep.simx_return_ok)
                System.out.format("Number of objects in the scene: %d\n",objectHandles.getArray().length);
            else
                System.out.format("Remote API function call returned with error code: %d\n",ret);
                
            try
            {
                Thread.sleep(2000);
            }
            catch(InterruptedException ex)
            {
                Thread.currentThread().interrupt();
            }
    
            // Now retrieve streaming data (i.e. in a non-blocking fashion):
            long startTime=System.currentTimeMillis();
            IntW mouseX = new IntW(0);
            vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,mouseX,vrep.simx_opmode_streaming); // Initialize streaming
            while (System.currentTimeMillis()-startTime < 5000)
            {
                ret=vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,mouseX,vrep.simx_opmode_buffer); // Try to retrieve the streamed data
                if (ret==vrep.simx_return_ok) // After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
                    System.out.format("Mouse position x: %d\n",mouseX.getValue()); // Mouse position x is actualized when the cursor is over V-REP's window
            }
            
            // Now send some data to V-REP in a non-blocking fashion:
            vrep.simxAddStatusbarMessage(clientID,"Hello V-REP!",vrep.simx_opmode_oneshot);

            // Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
            IntW pingTime = new IntW(0);
            vrep.simxGetPingTime(clientID,pingTime);

            // Now close the connection to V-REP:   
            vrep.simxFinish(clientID);
        }
        else
            System.out.println("Failed connecting to remote API server");
        System.out.println("Program ended");
    }
}
            
