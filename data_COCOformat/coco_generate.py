#!/usr/bin/env python3

import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
from pycococreatortools import pycococreatortools
import cv2
import argparse
import shutil
from tqdm import tqdm 
DATASET_NAME_SUFFIX='_ddd_70000'

INFO = {
    "description": "Dataset",
    "url": "",
    "version": "0.1.0",
    "year": 2019,
    "contributor": "Clark(Yunzhi) Lin",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'Semisphere',
        'supercategory': 'shape',
    },
    {
        'id': 2,
        'name': 'Cuboid',
        'supercategory': 'shape',
    },
    {
        'id': 3,
        'name': 'Cylinder',
        'supercategory': 'shape',
    },
    {
        'id': 4,
        'name': 'Ring',
        'supercategory': 'shape',
    },
    {
        'id': 5,
        'name': 'Stick',
        'supercategory': 'shape',
    },
    {
        'id': 6,
        'name': 'Sphere',
        'supercategory': 'shape',
    }
]

def filter_for_png(root, files):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    
    return files


def main():


    ROOT_DIR_LIST = ['train','val','test']
    for ROOT_DIR in ROOT_DIR_LIST:
        if not os.path.exists('Dataset/'+ROOT_DIR):
            continue
        IMAGE_DIR = os.path.join('Dataset',ROOT_DIR, "depth_png")
        ANNOTATION_DIR = os.path.join('Dataset',ROOT_DIR, "segmasks_label")

        coco_output = {
            "info": INFO,
            "licenses": LICENSES,
            "categories": CATEGORIES,
            "images": [],
            "annotations": []
        }

        image_id = 1
        segmentation_id = 1

        # filter for png images
        for root, _, files in os.walk(IMAGE_DIR):
            image_files = filter_for_png(root, files)

            # go through each image
            for image_filename in tqdm(image_files):
                image = Image.open(image_filename)
                image_info = pycococreatortools.create_image_info(
                    image_id, os.path.basename(image_filename), image.size)
                coco_output["images"].append(image_info)

                # filter for associated png annotations
                annotation_filename=os.path.join(ANNOTATION_DIR ,'segmask_img_label_'+image_filename[-10:-4]+'.png')
                # for root, _, files in os.walk(ANNOTATION_DIR):
                #     annotation_filename = filter_for_annotations(root, files, image_filename)

                    # go through each associated annotation
                    # for annotation_filename in annotation_files:

                # print(annotation_filename)
                #yunzhi
                # class_id = [x['id'] for x in CATEGORIES if x['name'] in annotation_filename][0]
                raw_image_segmask=cv2.imread(annotation_filename,-1)
                for i in range(1,7):
                    if i in raw_image_segmask:
                        category_info = {'id': i, 'is_crowd': 0}
                        # binary_mask=np.zeros(raw_image_segmask.shape)
                        binary_mask=np.where(raw_image_segmask==i,i,0)
                # category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}

                # #need checking
                # binary_mask = np.asarray(Image.open(annotation_filename)
                #     .convert('1')).astype(np.uint8)

                        annotation_info = pycococreatortools.create_annotation_info(
                            segmentation_id, image_id, category_info, binary_mask,
                            image.size, tolerance=2)

                        if annotation_info is not None:
                            coco_output["annotations"].append(annotation_info)

                        segmentation_id = segmentation_id + 1

                image_id = image_id + 1

        # TODO(Clark): Maybe we could have a better name here
        if ROOT_DIR=='train': # must have 'coco'
            with open('Dataset/annotations/coco_primitive_train'+DATASET_NAME_SUFFIX+'.json', 'w') as output_json_file:
                json.dump(coco_output, output_json_file)
        elif ROOT_DIR=='val': # must have 'coco'
            with open('Dataset/annotations/coco_primitive_val'+DATASET_NAME_SUFFIX+'.json', 'w') as output_json_file:
                json.dump(coco_output, output_json_file)
        elif ROOT_DIR=='test':
            with open('Dataset/annotations/coco_primitive_test'+DATASET_NAME_SUFFIX+'.json', 'w') as output_json_file:
                json.dump(coco_output, output_json_file)

    print('Finish!')

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="COCO-style Data Generation Process")
    # parser.add_argument("-m", "--model", default=0, help="train, val or test dataset")
    # args = parser.parse_args()
    if os.path.exists('Dataset/annotations'):
        shutil.rmtree('Dataset/annotations')
    os.mkdir('Dataset/annotations')
    main()
    # TODO(Clark): The name is too long
    if os.path.exists('../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco'):
        shutil.rmtree('../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco')
    os.mkdir('../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco')
    os.symlink(os.path.abspath('Dataset/annotations'),'../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco/annotations')
    os.symlink(os.path.abspath('Dataset/train'),'../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco/train'+DATASET_NAME_SUFFIX)
    os.symlink(os.path.abspath('Dataset/test'),'../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco/test'+DATASET_NAME_SUFFIX)
