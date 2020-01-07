function sysCall_init()
    print("Simulator launched, welcome!")
    print("<font color='green'>(for quick customizations, edit the sandbox script <i>system/sndbxscpt.txt</i>)</font>@html")
end

function sysCall_cleanup()
    print("Leaving...")
end

function sysCall_beforeSimulation()
    print("Simulation started.")
end

function sysCall_afterSimulation()
    print("Simulation stopped.")
    ___m=nil
end

function sysCall_sensing()
    local s=sim.getSimulationState()
    if s==sim.simulation_advancing_abouttostop and not ___m then
        print("simulation stopping...")
        ___m=true
    end
end

function sysCall_suspend()
    print("Simulation suspended.")
end

function sysCall_resume()
    print("Simulation resumed.")
end

--[[ Following callbacks are also supported:
function sysCall_nonSimulation()
end


function sysCall_beforeMainScript()
    local outData={doNotRunMainScript=false} -- when true, then the main script won't be executed
    return outData
end

function sysCall_actuation()
end

function sysCall_suspended()
end

function sysCall_beforeInstanceSwitch()
end

function sysCall_afterInstanceSwitch()
end

function sysCall_beforeCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be copied")
    end
end

function sysCall_afterCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was copied")
    end
end

function sysCall_beforeDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be deleted")
    end
    -- inData.allObjects indicates if all objects in the scene will be deleted
end

function sysCall_afterDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was deleted")
    end
    -- inData.allObjects indicates if all objects in the scene were deleted
end

function sysCall_afterCreate(inData)
    for i=1,#inData.objectHandles,1 do
        print("Object with handle "..inData.objectHandles[i].." was created")
    end
end
--]]