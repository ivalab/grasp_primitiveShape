import matplotlib.pyplot as plt
import numpy as np
import glob as gb
import cv2
import os
import shutil
from tqdm import tqdm
from multiprocessing import Pool

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
   
    dir_path_list=gb.glob(Src_dir+'/*')
    for dir_path in tqdm(dir_path_list):
        index=dir_path[dir_path.find('/')+1:]
        
        transfer(dir_path,index)

