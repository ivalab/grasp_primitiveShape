import numpy as np
import os
import re
from tqdm import tqdm
import fnmatch
# import pdb
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import copy
#import torch
#from torchvision import transforms as T
import argparse

def filter_for_png(root, files):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]

    return files
    
def compute_mean_var():
    ROOT_DIR_LIST = ['train', 'val', 'test']
    for ROOT_DIR in ROOT_DIR_LIST:
        if not os.path.exists('Dataset/' + ROOT_DIR):
            continue
        IMAGE_DIR = os.path.join('Dataset/',ROOT_DIR, "depth_png")

        cum_mean = 0.0
        cum_mean_squared = 0.0
        # filter for png images
        for root, _, files in os.walk(IMAGE_DIR):
            image_files = filter_for_png(root, files)
            # go through each image
            for image_filename in tqdm(image_files):

                image = cv2.imread(image_filename,-1).astype(np.float32)
                # pdb.set_trace()
                cum_mean += image/255.0
                cum_mean_squared += np.square(image/255.0)

                # print("mean : {}".format(image.mean()))
                if image.mean() == 0:
                    # pdb.set_trace()
                    print(image_filename)
                # pdb.set_trace()

            # mean, var = cum_mean / len(image_files), cum_var / len(image_files)
            meanD_1 = np.mean(cum_mean[:,:,0] / len(image_files))
            meanD_2 = np.mean(cum_mean[:,:,1] / len(image_files))
            meanD_3 = np.mean(cum_mean[:,:,2] / len(image_files))

            stdD_1 = np.sqrt(np.mean(cum_mean_squared[:,:,0]  / len(image_files))- (meanD_1 ** 2))
            stdD_2 = np.sqrt(np.mean(cum_mean_squared[:,:,1]  / len(image_files))- (meanD_2 ** 2))
            stdD_3 = np.sqrt(np.mean(cum_mean_squared[:,:,2]  / len(image_files))- (meanD_3 ** 2))

            
            print(ROOT_DIR)
            print("meanD_1 = %f;  stdD_1 = %f" % ( meanD_1,  stdD_1))
            print("meanD_2 = %f;  stdD_2 = %f" % ( meanD_2,  stdD_2))
            print("meanD_3 = %f;  stdD_3 = %f" % ( meanD_3,  stdD_3))





if __name__ == "__main__":
    compute_mean_var()
