-- Make sure to have V-REP running, with followig scene loaded:
--
-- scenes/B0-basedRemoteApiDemo.ttt
--
-- Do not launch simulation, and make sure that the B0 resolver
-- is running. Then run "simpleTest"
--
-- The client side (i.e. "simpleTest") depends on:
--
-- b0RemoteApi (Lua script), which depends on:
-- messagePack (Lua script)
-- b0Lua (shared library), which depends on:
-- b0 (shared library), which depends on:
-- boost_chrono (shared library)
-- boost_system (shared library)
-- boost_thread (shared library)
-- libzmq (shared library)

require 'b0RemoteApi'

local client=b0RemoteApi('b0RemoteApi_luaClient','b0RemoteApi')
local doNextStep=true

function simulationStepStarted(msg)
    local simTime=msg[2].simulationTime
    print('Simulation step started. Simulation time: ',simTime)
end
        
function simulationStepDone(msg)
    local simTime=msg[2].simulationTime
    print('Simulation step done. Simulation time: ',simTime)
    doNextStep=true
end
    
function imageCallback(msg)
    print('Received image.',msg[2])
    client.simxSetVisionSensorImage(passiveVisionSensorHandle[2],false,msg[3],client.simxDefaultPublisher())
end
    
client.simxAddStatusbarMessage('Hello world!',client.simxDefaultPublisher())
visionSensorHandle=client.simxGetObjectHandle('VisionSensor',client.simxServiceCall())
passiveVisionSensorHandle=client.simxGetObjectHandle('PassiveVisionSensor',client.simxServiceCall())
client.simxSynchronous(true)
    
--dedicatedSub=client.simxCreateSubscriber(imageCallback,1,true)
--client.simxGetVisionSensorImage(visionSensorHandle[2],false,dedicatedSub)
--dedicatedPub=client.simxCreatePublisher()
client.simxGetVisionSensorImage(visionSensorHandle[2],false,client.simxDefaultSubscriber(imageCallback))

client.simxGetSimulationStepStarted(client.simxDefaultSubscriber(simulationStepStarted))
client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simulationStepDone))
client.simxStartSimulation(client.simxDefaultPublisher())

startTime=client.simxGetTimeInMs()
while client.simxGetTimeInMs()<startTime+5000 do 
    if doNextStep then
        doNextStep=false
        client.simxSynchronousTrigger()
    end
    client.simxSpinOnce()
end
client.simxStopSimulation(client.simxDefaultPublisher())
client.delete()