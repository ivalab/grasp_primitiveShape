#!/usr/bin/env python

import time
import os
import random
import shutil
import argparse
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
import cv2
from collections import namedtuple
from robot import Robot
from logger import Logger
import utils

import glob

def create_objects_from_shape(shapes,obj_mesh_dir):
    """ Create objects folder for simulation from shapes generated"""
    # delete and create block_gen directory for the simulator
    if os.path.exists(obj_mesh_dir):
        shutil.rmtree(obj_mesh_dir)
    os.mkdir(obj_mesh_dir)

    obj_shape_dir = os.path.abspath("objects/primitive_shapes")

    obj_list=[]
    for iter, shape in enumerate(shapes):
        # sample one object from shape primitive directory
        obj = random.choice(os.listdir(os.path.join(obj_shape_dir, shape + "_obj/")))
        obj_list.append(obj)
        shutil.copy(os.path.join(obj_shape_dir, shape + "_obj/", obj), os.path.join(obj_mesh_dir, obj))
    return obj_list

def main(args, shapes):
    is_sim = True # simulation

    num_obj = len(shapes) # number of object

    port_num=int(args.port)
    obj_mesh_dir = "objects/block_gen_"+str(port_num)  # where .obj are located
    obj_mesh_dir = os.path.abspath(obj_mesh_dir)

    # workspace in simulation
    workspace_limits = np.asarray([[0.275, 0.53], [-0.235, 0.19], [-0.1501, 0.3]])
    heightmap_resolution = 0.002 # meter
    random_seed = 1234
    np.random.seed(random_seed)

    ## Pre-loading and logging options
    continue_logging = False # Continue logging from previous session
    logging_directory = os.path.abspath('logs')


    ## Initialize data logger
    logger = Logger(continue_logging, logging_directory, num_obj, offset=int(args.offset))

    ## Start main training/testing loop

    NUM_ITERATIONS = int(args.num_iterations)
    for iter in range(NUM_ITERATIONS):
        obj_list=create_objects_from_shape(shapes,obj_mesh_dir)
        # Save obj list
        logger.save_obj_list(iter,obj_list)

        # Initialize pick-and-place system (camera and robot)
        robot = Robot(is_sim, obj_mesh_dir, num_obj,shapes, workspace_limits,port_num)



        # if is_sim: robot.check_sim()
        # print("checked_sim")
        # Get latest RGB-D image
        color_img, depth_img = robot.get_camera_data()
        depth_img = depth_img * robot.cam_depth_scale # Apply depth scale from calibration

        if (depth_img==0).all():
                continue
        # Get heightmap from RGB-D image (by re-projecting 3D point cloud)
        # color_heightmap, depth_heightmap = utils.get_heightmap(color_img, depth_img, robot.cam_intrinsics, robot.cam_pose, workspace_limits, heightmap_resolution)

        ## RGB projected
        # color_rgb_projected, _ = utils.get_projected_rgb(color_img, depth_img, robot.cam_intrinsics, robot.cam_pose, workspace_limits, heightmap_resolution)

        ## RGB image cut workspace limits
        # np.logical_and(surface_pts[:,0] >= workspace_limits[0][0], surface_pts[:,0] < workspace_limits[0][1]), surface_pts[:,1] >= workspace_limits[1][0]), surface_pts[:,1] < workspace_limits[1][1]), surface_pts[:,2] < workspace_limits[2][1])

        # valid_depth_heightmap = depth_heightmap.copy()
        # valid_depth_heightmap[np.isnan(valid_depth_heightmap)] = 0

        # Save RGB-D images and RGB-D heightmaps
        logger.save_images(iter, color_img, depth_img, '0')
        # logger.save_heightmaps(iter, color_heightmap, valid_depth_heightmap)

        ## iterative solution for getting modal segmasks using opencv and not needing cameras in Vrep
        thresh = [[0.300, 0.470, 0.650],  # blue
                  [0.340, 0.630, 0.300],  # green
                  [0.610, 0.450, 0.370],  # brown
                  [0.940, 0.550, 0.160],  # orange
                  [0.920, 0.780, 0.280],  # yellow
                  [0.749, 0.937, 0.270],  # lime
                  [0.660, 1.000, 0.760],  # mint
                  [0.690, 0.470, 0.631],  # purple
                  [0.462, 0.717, 0.698],  # cyan
                  [0.990, 0.615, 0.654]]  #pink
        segmodal_img_black_white = np.zeros((480, 640, 3)).astype(np.uint8)
        segmodal_img_bin = np.zeros((480, 640, 3)).astype(np.uint8)
        img = color_img / 255
        for idx_obj in range(num_obj):
            cur_thresh = np.array(thresh[idx_obj])
            margin = 0.1
            lower_color = cur_thresh * (1.0 - margin)
            upper_color = cur_thresh * (1.0 + margin)

            mask = cv2.inRange(img, lower_color, upper_color)
            res = cv2.bitwise_and(img, img, mask=mask) # keep the values where mask = 1
            res = np.where(res != 0, 1, 0) # res !=0 then 1 else 0

            # construct segmodal black and white image
            segmodal_img_black_white = segmodal_img_black_white + res * 255
            segmodal_img_black_white=np.minimum(segmodal_img_black_white, 255)
            segmodal_img_black_white = segmodal_img_black_white.astype(np.uint8)
            # construct segmodal bin image
            bicolor_img_mask = np.where(res != 0, (idx_obj + 1), 0).astype(np.uint8)
            segmodal_img_bin = segmodal_img_bin + bicolor_img_mask


        logger.save_segmodal(iter, segmodal_img_black_white, segmodal_img_bin, '0')


        # pose saver
        positions, orientations = robot.get_obj_positions_and_orientations()
        logger.save_positions_and_orientations(iter, positions, orientations)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Data Collection Process")
    parser.add_argument("-n", "--num_iterations", default=25000, help="number of images to collect")
    parser.add_argument("-o", "--offset", default=0, help="start saving images starting from #offset image")
    parser.add_argument("-p", "--port", default=19999, help="port number")
    args = parser.parse_args()
    # Shapes to use
    shapes = ["Semisphere", "Cuboid", "Cylinder", "Ring", "Stick","Sphere"]
    main(args, shapes)
