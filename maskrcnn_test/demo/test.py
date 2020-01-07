import matplotlib.pyplot as plt
import numpy as np
import glob as gb
import cv2
import os
import shutil
from tqdm import tqdm
from multiprocessing import Pool

import argparse
from maskrcnn_benchmark.config import cfg
from predictor_kinect import COCODemo

import time

Src_dir='multi_objects_4_review'

def Kinect_DepthNormalization (depthImage):
    [row,col] = depthImage.shape
    widthBound = row-1
    heightBound = col-1

    # initializing working image; leave original matrix aside
    filledDepth = depthImage

    #initializing the filter matrix
    filterBlock3x3 = np.zeros((3,3))
    
    # to keep count of zero pixels found
    zeroPixels = 0
    
    #The main loop
    for x in range(row):
        for y in range(col):      
            #Only for pixels with 0 depth value; else skip
            if filledDepth[x,y] == 0:

                zeroPixels = zeroPixels+1
                # values set to identify a positive filter result.
                p = 0
                # Taking a cube of 3x3 around the 0 depth pixel
                # q = index
                # select two pixels behind and two ahead in a row
                # select two pixels behind and two ahead in a column
                # leave the center pixel (as its the one to be filled)
                for xi in range(-1,1+1):
                    q = 0
                    for yi in range(-1,1+1):
                        # updating index for next pass
                        xSearch = x + xi
                        ySearch = y + yi
                        # xSearch and ySearch to avoid edges
                        if (xSearch > 0 and xSearch < widthBound and ySearch > 0 and ySearch < heightBound):
                        # save values from depth image into filter
                            filterBlock3x3[p,q] = filledDepth[xSearch,ySearch]
                        q = q+1
                    p = p+1

                v = filterBlock3x3[np.nonzero(filterBlock3x3)]
                
                if v.size==0: 
                    filledDepth[x,y] = 0
                else:
                    temp=np.diff(np.append(v,10**5))
                    indices =  np.where(temp > 0)[0]
                    i =  np.argmax(np.diff(np.append(0,indices)))
                    mode = v[indices[i]]
                    # fill in the x,y value with the statistical mode of the values
                    filledDepth[x,y] = mode

    return filledDepth, zeroPixels
                


def transfer(dir_path,index):
    depth_npy_path=dir_path+'/depth_npy_'+str(index)+'.npy'

    # 1. stretch
    npy = np.load(depth_npy_path)
    npy = np.round(npy, decimals=4)
    # npy = np.where(npy != 0, np.round( npy * 255).astype(np.uint8), 0) # no stretch
    npy=np.where(npy!=0,np.round((npy-0.5)*255).astype(np.uint8),0)
    
    # 2. crop
    top=40
    bottom = 20
    left=25
    right = 40
    crop_img = npy[top:-bottom, left:-right]
    
    # 3. copy border
    borderType = cv2.BORDER_REPLICATE
    dst = cv2.copyMakeBorder(crop_img, top, bottom, left, right, borderType, None)
    
    # 4. median filter
    filledDepth, zeroPixels =Kinect_DepthNormalization(dst)

    # final. save
    depth_img_path = dir_path+'/depth_img_'+str(index)+'.png'
    filledDepth_three_channel = cv2.cvtColor(filledDepth, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(depth_img_path, filledDepth_three_channel)

   
if __name__ == '__main__':

    ## Set the parameters
    parser = argparse.ArgumentParser(description="PyTorch Object Detection Webcam Demo")
    parser.add_argument(
        "--config-file",
        # default="../configs/demo_95000_stretch_air2_e2e_mask_rcnn_R_50_FPN_1x.yaml",  # Stretch+air2
        default="../configs/demo_95000_stretch_noise_air3_e2e_mask_rcnn_R_50_FPN_1x.yaml", # Stretch+noise+air2
        # default="../configs/demo_95000_raw_air2_e2e_mask_rcnn_R_50_FPN_1x.yaml",  # Raw+air2
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.45,
        help="Minimum score for the prediction to be shown",
    )
    parser.add_argument(
        "--min-image-size",
        type=int,
        default=224,
        help="Smallest size of the image to feed to the model. "
            "Model was trained with 800, which gives best results",
    )
    parser.add_argument(
        "--show-mask-heatmaps",
        dest="show_mask_heatmaps",
        help="Show a heatmap probability for the top masks-per-dim masks",
        action="store_true",
    )
    parser.add_argument(
        "--masks-per-dim",
        type=int,
        default=2,
        help="Number of heatmaps per dimension to show",
    )
    parser.add_argument(
        "opts",
        help="Modify model config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )

    args = parser.parse_args()

    # load config from file and command-line arguments
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()

    # prepare object that handles inference plus adds predictions on top of image
    coco_demo = COCODemo(
        cfg,
        confidence_threshold=args.confidence_threshold,
        show_mask_heatmaps=args.show_mask_heatmaps,
        masks_per_dim=args.masks_per_dim,
        min_image_size=args.min_image_size,
    )


    ## delete old files
    dir_path_list = gb.glob(Src_dir + '/*/predict_mask*')
    for dir_path in tqdm(dir_path_list):
        os.remove(dir_path)


    ## For single folder
    #*********************************************************
    
    dir_path_list=gb.glob(Src_dir+'/*')
    for dir_path in tqdm(dir_path_list):

        start_time = time.time()

        index=dir_path[dir_path.find('/')+1:]
        
        transfer(dir_path,index)

        index=dir_path[dir_path.find('/')+1:]
        
        depth_img_path = dir_path + '/depth_img_' + str(index) + '.png'
        img = cv2.imread(depth_img_path)

        color_img_path= dir_path + '/color_image_' + str(index) + '.png'
        img_show = cv2.imread(color_img_path)

        # run
        composite,mask_output = coco_demo.run_on_opencv_image(img,img_show)

        inference_time=time.time() - start_time
        print("Single Time: {:.2f} s / img".format(inference_time))
        avg_inference_time=avg_inference_time+inference_time

        # For test
        # cv2.imshow("COCO detections", composite)

        cv2.imwrite(dir_path + '/visualized_image_'+str(index)+'.png',composite)

        # Save mask_label & mask_filled area
        for i in range(len(mask_output)):
            cv2.imwrite(dir_path + '/predict_mask_img_bin_' + str(index) + '_' + str(i) + '.png',
                        mask_output[i])
            cv2.imwrite(dir_path + '/predict_mask_img_black_white_' + str(index) + '_' + str(i) + '.png',
                        255*mask_output[i])
        
    avg_inference_time=avg_inference_time/len(dir_path_list)
    print("Average Time: {:.2f} s / img".format(avg_inference_time))

