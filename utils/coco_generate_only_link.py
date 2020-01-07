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

if __name__ == "__main__":

    if os.path.exists('../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco'):
        shutil.rmtree('../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco')
    os.mkdir('../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco')
    os.symlink(os.path.abspath('Dataset/annotations'),'../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco/annotations')
    os.symlink(os.path.abspath('Dataset/train'),'../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco/train'+DATASET_NAME_SUFFIX)
    os.symlink(os.path.abspath('Dataset/test'),'../maskrcnn_test/maskrcnn_benchmark/data/datasets/datasets/coco/test'+DATASET_NAME_SUFFIX)
