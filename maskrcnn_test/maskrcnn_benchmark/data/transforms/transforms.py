# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
import random

import torch
import torchvision
from torchvision.transforms import functional as F
from PIL import Image
from pycocotools import mask as maskUtils
import numpy as np

class Compose(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, image, target):
        for t in self.transforms:
            image, target = t(image, target)
        return image, target

    def __repr__(self):
        format_string = self.__class__.__name__ + "("
        for t in self.transforms:
            format_string += "\n"
            format_string += "    {0}".format(t)
        format_string += "\n)"
        return format_string


class Resize(object):
    def __init__(self, min_size, max_size):
        if not isinstance(min_size, (list, tuple)):
            min_size = (min_size,)
        self.min_size = min_size
        self.max_size = max_size

    # modified from torchvision to add support for max size
    def get_size(self, image_size):
        w, h = image_size
        size = random.choice(self.min_size)
        max_size = self.max_size
        if max_size is not None:
            min_original_size = float(min((w, h)))
            max_original_size = float(max((w, h)))
            if max_original_size / min_original_size * size > max_size:
                size = int(round(max_size * min_original_size / max_original_size))

        if (w <= h and w == size) or (h <= w and h == size):
            return (h, w)

        if w < h:
            ow = size
            oh = int(size * h / w)
        else:
            oh = size
            ow = int(size * w / h)

        return (oh, ow)

    def __call__(self, image, target):
        size = self.get_size(image.size)
        image = F.resize(image, size)
        target = target.resize(image.size)
        return image, target


class RandomHorizontalFlip(object):
    def __init__(self, prob=0.5):
        self.prob = prob

    def __call__(self, image, target):
        if random.random() < self.prob:
            image = F.hflip(image)
            target = target.transpose(0)
        return image, target


class ColorJitter(object):
    def __init__(self,
                 brightness=None,
                 contrast=None,
                 saturation=None,
                 hue=None,
                 ):
        self.color_jitter = torchvision.transforms.ColorJitter(
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            hue=hue,)

    def __call__(self, image, target):
        image = self.color_jitter(image)
        return image, target


class ToTensor(object):
    def __call__(self, image, target):
        return F.to_tensor(image), target


class Normalize(object):
    def __init__(self, mean, std, to_bgr255=True):
        self.mean = mean
        self.std = std
        self.to_bgr255 = to_bgr255

    def __call__(self, image, target):
        if self.to_bgr255:
            #pdb.set_trace()
            image = image[[2, 1, 0]] * 255
        
        # ipdb.set_trace()
        image = F.normalize(image, mean=self.mean, std=self.std)
        return image, target

class ChangeColor(object):
    def __call__(self, image, target):
        array_image = np.array(image)
        # new_array_image=np.zeros(array_image.shape)
        num_instnce=list(target.extra_fields['labels'].shape)[0]
        for i in range(num_instnce):
            instance = target.extra_fields['masks'].instances[i]
            segm=instance.polygons[0].polygons
            w,h = instance.size
            rles = maskUtils.frPyObjects(segm, h, w)
            rle = maskUtils.merge(rles)
            m = maskUtils.decode(rle)

            r_=array_image[:,:,0]*m
            r_[r_!=0]=random.randint(0,255)
            g_=array_image[:,:,1]*m
            g_[g_ != 0] = random.randint(0, 255)

            array_image[:,:,0]=np.where(r_>0,r_,array_image[:,:,0])
            array_image[:, :, 1] = np.where(g_ > 0, g_, array_image[:, :, 1])

            # new_array_image[:, :, 2] = array_image[:, :, 2]
        new_image=Image.fromarray(np.uint8(array_image))

        # image.show()
        # new_image.show()
        # return image, target
        return new_image, target