import socket
import select
import struct
import time
import os
import numpy as np
import utils
from simulation import vrep
import random

class Robot(object):
    
    def __init__(self, is_sim, obj_mesh_dir, num_obj,shapes, workspace_limits,
                 port_num=19997):

        temp_dict=dict(list(enumerate(shapes)))
        self.shapes_dict=dict(zip(temp_dict.values(), temp_dict.keys()))

        self.is_sim = is_sim
        self.workspace_limits = workspace_limits

        # If in simulation...
        if self.is_sim:

            # Define colors for object meshes (Tableau palette)
            self.color_space = np.asarray([[78.0, 121.0, 167.0], # blue
                                           [89.0, 161.0, 79.0], # green
                                           [156, 117, 95], # brown
                                           [242, 142, 43], # orange
                                           [237.0, 201.0, 72.0], # yellow
                                           # [186, 176, 172], # gray (bef)
                                           [191, 239, 69], # lime
                                           # [255.0, 87.0, 89.0], # red (bef)
                                           [170, 255, 195], # mint
                                           [176, 122, 161], # purple
                                           [118, 183, 178], # cyan
                                           [255, 157, 167]])/255.0 #pink

            # Read files in object mesh directory
            self.obj_mesh_dir = obj_mesh_dir
            self.num_obj = num_obj
            self.mesh_list =os.listdir(self.obj_mesh_dir)
            random.shuffle(self.mesh_list)
            self.obj_mesh_color = self.color_space[np.asarray(range(self.num_obj)) % 10, :]

            # Make sure to have the server side running in V-REP:
            # in a child script of a V-REP scene, add following command
            # to be executed just once, at simulation start:
            #
            # simExtRemoteApiStart(19999)
            #
            # then start simulation, and run this program.
            #
            # IMPORTANT: for each successful call to simxStart, there
            # should be a corresponding call to simxFinish at the end!

            # MODIFY remoteApiConnections.txt

            # Connect to simulator
            vrep.simxFinish(-1) # Just in case, close all opened connections
            self.sim_client = vrep.simxStart('127.0.0.1', port_num, True, False, 5000, 3)  # Connect to V-REP on port 19997

            if self.sim_client == -1:
                print('Failed to connect to simulation (V-REP remote API server). Exiting.')
                exit()
            else:
                print('Connected to simulation.')
                self.restart_sim()

            # Setup virtual camera in simulation
            self.setup_sim_camera()

            # Add objects to simulation environment
            # print("Adding objects ...")
            self.add_objects()
            # print("Added objects !")

    def setup_sim_camera(self):

        # Get handle to camera
        sim_ret, self.cam_handle = vrep.simxGetObjectHandle(self.sim_client, 'Vision_sensor_persp', vrep.simx_opmode_blocking)

        # Get camera pose and intrinsics in simulation
        sim_ret, cam_position = vrep.simxGetObjectPosition(self.sim_client, self.cam_handle, -1, vrep.simx_opmode_blocking)
        sim_ret, cam_orientation = vrep.simxGetObjectOrientation(self.sim_client, self.cam_handle, -1, vrep.simx_opmode_blocking)
        cam_trans = np.eye(4,4)
        cam_trans[0:3,3] = np.asarray(cam_position)
        cam_orientation = [-cam_orientation[0], -cam_orientation[1], -cam_orientation[2]]
        cam_rotm = np.eye(4,4)
        cam_rotm[0:3,0:3] = np.linalg.inv(utils.euler2rotm(cam_orientation))
        self.cam_pose = np.dot(cam_trans, cam_rotm) # Compute rigid transformation representating camera pose
        self.cam_depth_scale = 1

        # Get background image
        self.bg_color_img, self.bg_depth_img = self.get_camera_data()
        self.bg_depth_img = self.bg_depth_img * self.cam_depth_scale


    def get_camera_data(self):

        if self.is_sim:

            # Get color image from simulation
            sim_ret, resolution, raw_image = vrep.simxGetVisionSensorImage(self.sim_client, self.cam_handle, 0, vrep.simx_opmode_blocking)
            color_img = np.asarray(raw_image)
            color_img.shape = (resolution[1], resolution[0], 3)
            color_img = color_img.astype(np.float)/255
            color_img[color_img < 0] += 1
            color_img *= 255
            color_img = np.fliplr(color_img)
            # Todo(Clark): Here there is a bug in the Vrep, we fix it manually
            # color_img[181,480]=color_img[181,481]
            color_img = color_img.astype(np.uint8)

            # Get depth image from simulation
            sim_ret, resolution, depth_buffer = vrep.simxGetVisionSensorDepthBuffer(self.sim_client, self.cam_handle, vrep.simx_opmode_blocking)

            depth_img = np.asarray(depth_buffer)
            depth_img.shape = (resolution[1], resolution[0])
            depth_img = np.fliplr(depth_img)
            zNear = 0.5
            zFar = 1.5
            depth_img = depth_img * (zFar - zNear) + zNear
        return color_img, depth_img

    def add_objects(self):

        # Add each object to robot workspace at x,y location and orientation (random or pre-loaded)
        self.object_handles = []
        for object_idx in range(self.num_obj):
            curr_mesh_file = os.path.join(self.obj_mesh_dir, self.mesh_list[object_idx])
            curr_shape_name = self.mesh_list[object_idx][0:self.mesh_list[object_idx].find('_')]
            # Todo(Clark): Change the range of x and y
            drop_x = (self.workspace_limits[0][1] - self.workspace_limits[0][0])*0.6 * np.random.random_sample() + \
                     self.workspace_limits[0][0]+0.2*(self.workspace_limits[0][1] - self.workspace_limits[0][0])
            drop_y = (self.workspace_limits[1][1] - self.workspace_limits[1][0])*0.6 * np.random.random_sample() + \
                     self.workspace_limits[1][0]+0.2*(self.workspace_limits[1][1] - self.workspace_limits[1][0])

            object_position = [drop_x, drop_y, 0]  # where to change height
            # Todo(Clark): Special placement
            # default static
            object_static=0


            if curr_shape_name=='Bowl':
                object_orientation =[1/6*np.pi*(np.random.random_sample()-0.5),1/6*np.pi*(np.random.random_sample()-0.5),0]
            elif curr_shape_name=='Cylinder' or curr_shape_name=='Cuboid':
                if np.random.randint(2)==1: # right up on ground
                    object_orientation = [1 / 10 * np.pi * (np.random.random_sample() - 0.5),
                                          1 / 10 * np.pi * (np.random.random_sample() - 0.5), 0]
                else:
                    object_orientation = [2 * np.pi * np.random.random_sample(), 2 * np.pi * np.random.random_sample(),
                                          2 * np.pi * np.random.random_sample()]  # where to change rotation
            elif curr_shape_name == 'Ring':
                choice=np.random.randint(5)
                # print(choice)
                if choice==0: # right up on ground
                    object_static = 1
                    object_orientation = [0.5*np.pi,
                                          0, 2 * np.pi * np.random.random_sample()]
                    object_position = [drop_x, drop_y, -0.02]  # where to change heigh
                elif choice==1:  # on ground
                    object_orientation = [2 * np.pi * np.random.random_sample(), 2 * np.pi * np.random.random_sample(),
                                          2 * np.pi * np.random.random_sample()]  # where to change rotation
                else: # in the air
                    object_position = [drop_x, drop_y, -0.0935+0.02+0.14*np.random.random_sample()]  # where to change height
                    object_static=1

                    choice2 = np.random.randint(2)
                    if choice2 == 0:  # rotate 90
                        object_orientation = [0.5*np.pi+1/15 * np.pi * (np.random.random_sample()-0.5), 1/15 * np.pi * (np.random.random_sample()-0.5),
                                              2 * np.pi * np.random.random_sample()]  # where to change rotation
                    else:  # right up
                        object_orientation = [0+1/15 * np.pi * (np.random.random_sample()-0.5), 1/15 * np.pi *(np.random.random_sample()-0.5),
                                              2 * np.pi * np.random.random_sample()]  # where to change rotation


            elif curr_shape_name == 'Stick':
                choice = np.random.randint(3)

                if choice != 0:  # on ground
                    object_orientation = [2 * np.pi * np.random.random_sample(), 2 * np.pi * np.random.random_sample(),
                                          2 * np.pi * np.random.random_sample()]  # where to change rotation
                else:  # in the air
                    object_position = [drop_x, drop_y,
                                       -0.0935 + 0.01+0.14* np.random.random_sample()]  # where to change height
                    object_static = 1
                    object_orientation = [0.5*np.pi+1/15 * np.pi * (np.random.random_sample()-0.5),
                                          1/15 * np.pi * (np.random.random_sample()-0.5),
                                          2 * np.pi * np.random.random_sample()]  # where to change rotation
            else:
                object_orientation = [2*np.pi*np.random.random_sample(), 2*np.pi*np.random.random_sample(), 2*np.pi*np.random.random_sample()] # where to change rotation


            object_color = [self.obj_mesh_color[self.shapes_dict[curr_shape_name]][0], self.obj_mesh_color[self.shapes_dict[curr_shape_name]][1], self.obj_mesh_color[self.shapes_dict[curr_shape_name]][2]]
            ret_resp,ret_ints,ret_floats,ret_strings,ret_buffer = vrep.simxCallScriptFunction(self.sim_client, 'remoteApiCommandServer',vrep.sim_scripttype_childscript,'importShape',[object_static], object_position + object_orientation + object_color, [curr_mesh_file, curr_shape_name], bytearray(), vrep.simx_opmode_blocking)


            if ret_resp == 8:
                print('Failed to add new objects to simulation. Please restart.')
                self.restart_sim()
                self.add_objects()
                return

            curr_shape_handle = ret_ints[0]
            self.object_handles.append(curr_shape_handle)
            time.sleep(1)
        self.prev_obj_positions = []
        self.obj_positions = []


    def restart_sim(self):

        sim_ret, self.UR5_target_handle = vrep.simxGetObjectHandle(self.sim_client,'UR5_target',vrep.simx_opmode_blocking)
        vrep.simxSetObjectPosition(self.sim_client, self.UR5_target_handle, -1, (0.35,0,0.15), vrep.simx_opmode_blocking)
        vrep.simxStopSimulation(self.sim_client, vrep.simx_opmode_blocking)
        vrep.simxStartSimulation(self.sim_client, vrep.simx_opmode_blocking)
        time.sleep(1)
        sim_ret, self.RG2_tip_handle = vrep.simxGetObjectHandle(self.sim_client, 'UR5_tip', vrep.simx_opmode_blocking)
        sim_ret, gripper_position = vrep.simxGetObjectPosition(self.sim_client, self.RG2_tip_handle, -1, vrep.simx_opmode_blocking)
        while gripper_position[2] > 0.4: # V-REP bug requiring multiple starts and stops to restart
            vrep.simxStopSimulation(self.sim_client, vrep.simx_opmode_blocking)
            vrep.simxStartSimulation(self.sim_client, vrep.simx_opmode_blocking)
            time.sleep(1)
            sim_ret, gripper_position = vrep.simxGetObjectPosition(self.sim_client, self.RG2_tip_handle, -1, vrep.simx_opmode_blocking)


    def check_sim(self):

        # Check if simulation is stable by checking if gripper is within workspace
        sim_ret, gripper_position = vrep.simxGetObjectPosition(self.sim_client, self.RG2_tip_handle, -1, vrep.simx_opmode_blocking)
        sim_ok = gripper_position[0] > self.workspace_limits[0][0] - 0.1 and gripper_position[0] < self.workspace_limits[0][1] + 0.1 and gripper_position[1] > self.workspace_limits[1][0] - 0.1 and gripper_position[1] < self.workspace_limits[1][1] + 0.1 and gripper_position[2] > self.workspace_limits[2][0] and gripper_position[2] < self.workspace_limits[2][1]
        if not sim_ok:
            print('Simulation unstable. Restarting environment.')
            self.restart_sim()
            self.add_objects()
