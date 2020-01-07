import time
import datetime
import os
import numpy as np
import cv2
import scipy.io

class Logger():

    def __init__(self, continue_logging, logging_directory, num_obj, offset):
        self.offset = offset

        # Create directory to save data
        timestamp = time.time()
        timestamp_value = datetime.datetime.fromtimestamp(timestamp)
        self.continue_logging = continue_logging
        if self.continue_logging:
            self.base_directory = logging_directory
            print('Pre-loading data logging session: %s' % (self.base_directory))
        else:
            self.base_directory = os.path.join(logging_directory, timestamp_value.strftime('%Y-%m-%d.%H:%M:%S'))
            print('Creating data logging session: %s' % (self.base_directory))

        self.color_images_directory = os.path.join(self.base_directory, 'data', 'color_images')
        if not os.path.exists(self.color_images_directory):
            os.makedirs(self.color_images_directory)

        self.depth_images_directory = os.path.join(self.base_directory, 'data', 'depth_images')
        if not os.path.exists(self.depth_images_directory):
            os.makedirs(self.depth_images_directory)

        self.depth_npy_directory =  os.path.join(self.base_directory, 'data', 'depth_npy')
        if not os.path.exists(self.depth_npy_directory):
            os.makedirs(self.depth_npy_directory)

        self.segmask_rgb_directory =  os.path.join(self.base_directory, 'data', 'segmasks_filled')
        if not os.path.exists(self.segmask_rgb_directory):
            os.makedirs(self.segmask_rgb_directory)

        self.segmask_bin_directory =  os.path.join(self.base_directory, 'data', 'segmasks_label')
        if not os.path.exists(self.segmask_bin_directory):
            os.makedirs(self.segmask_bin_directory)



    def save_images(self, iteration, color_image, depth_image, mode):
        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(self.color_images_directory, 'color_image_%06d.png' % (iteration + self.offset)), color_image)

        # save npy files (takes a lot of space)
        np.save(os.path.join(self.depth_npy_directory, 'depth_npy_%06d.npy' % (iteration + self.offset)), depth_image)

        # For visulization
        depth_image = np.round(depth_image * 10000).astype(np.uint16) # Save depth in 1e-4 meters
        depth_image = cv2.cvtColor(depth_image, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(os.path.join(self.depth_images_directory, 'depth_image_%06d.png' % (iteration + self.offset)), depth_image)

    def save_segmask(self, iteration, segmask_img_filled, segmask_img_label):
        """ Method to save segmask image """
        ## rgb segmask images
        segmask_img_filled = cv2.cvtColor(segmask_img_filled, cv2.COLOR_RGB2GRAY)
        cv2.imwrite(os.path.join(self.segmask_rgb_directory, 'segmask_img_filled_%06d.png' % (iteration + self.offset)), segmask_img_filled)

        ## binary segmask images
        segmask_img_label = cv2.cvtColor(segmask_img_label, cv2.COLOR_RGB2GRAY)
        cv2.imwrite(os.path.join(self.segmask_bin_directory, 'segmask_img_label_%06d.png' % (iteration + self.offset)), segmask_img_label)

    def save_obj_list(self,iteration,obj_list):
        filepath = os.path.join(self.base_directory, 'data', 'obj_list.txt')
        with open(filepath, "a") as f:
            f.write('%06d' % (iteration+ self.offset))
            for obj in obj_list:
                f.write(" " + obj)
            f.write("\n")
        f.close()