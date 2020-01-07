import matplotlib.pyplot as plt
import numpy as np
import glob as gb
import cv2
import os
import shutil
from tqdm import tqdm
from multiprocessing import Pool
import skimage

ONLY_TEST = False
MULTI_NUMBER = 12
SPLIT_NUMBER = 11
BASE_NUMBER = 500


def transfer(path):
    # print(path)
    # for splitting
    # TODO(Clark): the number should be updated
    if int(path[0:path.find('/')]) < 75000:
        target = 'train'
    else:
        target = 'test'

    if ONLY_TEST:
        target = 'test'

    # generate depth_image
    npy = np.load(path)
    npy = np.round(npy, decimals=4)
    npy=np.round((npy-0.5)*255).astype(np.uint8)
    # TODO(Clark): the name is not flexible
    target_depth_path = 'Dataset/' + target + '/depth_png/depth_image_' + path[-10:-4] + '.png'

    # add oil-painting noise part
    fill_img = cv2.imread(path[0:path.find('depth_npy')] +'segmasks_filled/segmask_img_filled_' + path[-10:-4] + '.png', 0)
    fill_img_enlarge = cv2.dilate(fill_img, np.ones((20, 20)).astype('uint8'), iterations=2)
    fill_img_enlarge = np.where(fill_img_enlarge == 255, 1, 0).astype('uint8')
    dst = npy.copy()

    height = dst.shape[0]
    width = dst.shape[1]
    oil_image = np.zeros((height, width))
    R = 4
    stroke_mask = []
    for y in range(-R, R):
        for x in range(-R, R):
            if y * y + x * x < R * R:
                stroke_mask.append((y, x))

    for y in tqdm(range(height)):
        for x in range(width):
            # progress = np.round(100*(y*width+x)/(width*height), 2)
            # print( "Progress: ", str(progress)+"%", end='\r' )
            local_histogram = np.zeros(256)
            local_channel_count = np.zeros(256)
            for dy, dx in stroke_mask:
                yy = y + dy
                xx = x + dx
                if yy < 0 or yy >= height or xx <= 0 or xx >= width:
                    continue
                intensity = dst[yy, xx]
                local_histogram[intensity] += 1

                local_channel_count[intensity] += dst[yy, xx]

            max_intensity = np.argmax(local_histogram)
            max_intensity_count = local_histogram[max_intensity]

            oil_image[y, x] = local_channel_count[max_intensity] / max_intensity_count

    oil_image = oil_image.astype('uint8')
    ROI_oil_image = (fill_img_enlarge*oil_image+(1-fill_img_enlarge)*npy)

    # add oil-painting noise part
    #Final_dst = skimage.util.random_noise(ROI_oil_image/255.0, mode="gaussian", var=0.00002)
    #Final_dst=np.round(Final_dst*255).astype('uint8')
    
    # save
    # Final_dst = cv2.cvtColor(Final_dst, cv2.COLOR_GRAY2BGR)
    Final_dst = cv2.cvtColor(ROI_oil_image, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(target_depth_path, Final_dst)
    
    # copy mask_img
    sourse_mask_path = path[0:path.find('depth_npy')] + 'segmasks_label/segmask_img_label_' + path[-10:-4] + '.png'
    target_mask_path = 'Dataset/' + target + '/segmasks_label/segmask_img_label_' + path[-10:-4] + '.png'
    shutil.copy(sourse_mask_path, target_mask_path)

    # copy color_img
    sourse_color_path = path[0:path.find('depth_npy')] + 'color_images/color_image_' + path[-10:-4] + '.png'
    target_color_path = 'Dataset/' + target + '/color_images/color_image_' + path[-10:-4] + '.png'
    shutil.copy(sourse_color_path, target_color_path)


def path_cut(element):
    return int(element[0:element.find('/')])


if __name__ == '__main__':

    if os.path.exists('Dataset'):
        shutil.rmtree('Dataset')
    os.mkdir('Dataset')
    # Todo(Clark): Have not tested yet, not sure if it will work or not
    dir_list = os.listdir('.')
    target_dir_path_list = []
    for path in dir_list:
        if os.path.isdir(path):
            target_dir_path_list.append(path)
    target_dir_path_list.sort()
    # Todo(Clark): Not a good solution here
    if len(target_dir_path_list[0]) > 6:
        for iter, dir_path in enumerate(target_dir_path_list):
            os.rename(dir_path, str(iter * 5000))

    target_dir_path_list = []
    dir_path_list = os.listdir('.')
    for path in dir_path_list:
        if os.path.isdir(path) and path[0].isdigit():
            target_dir_path_list.append(os.path.join(path, 'data', 'depth_npy'))
    target_dir_path_list.sort(key=path_cut)
    npy_path_list = []
    for i in range(len(target_dir_path_list)):
        npy_path_list.extend(gb.glob(os.path.join(target_dir_path_list[i], "*.npy")))

    os.mkdir('Dataset/train')
    os.mkdir('Dataset/train/segmasks_label')
    os.mkdir('Dataset/train/depth_png')
    os.mkdir('Dataset/train/color_images')

    os.mkdir('Dataset/test')
    os.mkdir('Dataset/test/segmasks_label')
    os.mkdir('Dataset/test/depth_png')
    os.mkdir('Dataset/test/color_images')

    pool2 = Pool(processes=MULTI_NUMBER)
    pool2.map(transfer, npy_path_list)
    pool2.close()
    pool2.join()
    print('Preprocessing data part finished')

    print('All Finished')
