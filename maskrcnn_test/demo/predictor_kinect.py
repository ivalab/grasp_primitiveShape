# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
import cv2
import torch
import torchvision
from torchvision import _C
from torchvision import transforms as T

from maskrcnn_benchmark.modeling.detector import build_detection_model
from maskrcnn_benchmark.utils.checkpoint import DetectronCheckpointer
from maskrcnn_benchmark.structures.image_list import to_image_list
from maskrcnn_benchmark.modeling.roi_heads.mask_head.inference import Masker
from maskrcnn_benchmark import layers as L
from maskrcnn_benchmark.utils import cv2_util
import os

Color_dict={
    1:  [241,24,231], #rose
    2:  [89.0, 161.0, 79.0], #green
    3:  [234, 9, 9], #red
    4:  [242, 142, 43], # orange
    5:  [251.0, 234.0, 28.0], # yello
    6:  [26, 170, 240] # blue


}


class COCODemo(object):
    # COCO categories for pretty print
    CATEGORIES = [

        "__background",
        "Semisphere",
        "Cuboid",
        "Cylinder",
        "Ring",
        "Stick",
        "Sphere",

    ]




    # CATEGORIES = [
    #
    #     "__background",
    #     "cylinder",
    #     "sphere",
    #     "ring",
    #     "cube",
    #     "cone",
    #     "bowl",
    #     "ellipsoid",
    #
    # ]
    # CATEGORIES = [
    #     "__background",
    #     "person",
    #     "bicycle",
    #     "car",
    #     "motorcycle",
    #     "airplane",
    #     "bus",
    #     "train",
    #     "truck",
    #     "boat",
    #     "traffic light",
    #     "fire hydrant",
    #     "stop sign",
    #     "parking meter",
    #     "bench",
    #     "bird",
    #     "cat",
    #     "dog",
    #     "horse",
    #     "sheep",
    #     "cow",
    #     "elephant",
    #     "bear",
    #     "zebra",
    #     "giraffe",
    #     "backpack",
    #     "umbrella",
    #     "handbag",
    #     "tie",
    #     "suitcase",
    #     "frisbee",
    #     "skis",
    #     "snowboard",
    #     "sports ball",
    #     "kite",
    #     "baseball bat",
    #     "baseball glove",
    #     "skateboard",
    #     "surfboard",
    #     "tennis racket",
    #     "bottle",
    #     "wine glass",
    #     "cup",
    #     "fork",
    #     "knife",
    #     "spoon",
    #     "bowl",
    #     "banana",
    #     "apple",
    #     "sandwich",
    #     "orange",
    #     "broccoli",
    #     "carrot",
    #     "hot dog",
    #     "pizza",
    #     "donut",
    #     "cake",
    #     "chair",
    #     "couch",
    #     "potted plant",
    #     "bed",
    #     "dining table",
    #     "toilet",
    #     "tv",
    #     "laptop",
    #     "mouse",
    #     "remote",
    #     "keyboard",
    #     "cell phone",
    #     "microwave",
    #     "oven",
    #     "toaster",
    #     "sink",
    #     "refrigerator",
    #     "book",
    #     "clock",
    #     "vase",
    #     "scissors",
    #     "teddy bear",
    #     "hair drier",
    #     "toothbrush",
    # ]

    def __init__(
        self,
        cfg,
        confidence_threshold=0.7,
        show_mask_heatmaps=False,
        masks_per_dim=2,
        min_image_size=224,
    ):
        self.cfg = cfg.clone()
        self.model = build_detection_model(cfg)
        self.model.eval()
        self.device = torch.device(cfg.MODEL.DEVICE)
        self.model.to(self.device)
        self.min_image_size = min_image_size

        save_dir = cfg.OUTPUT_DIR
        checkpointer = DetectronCheckpointer(cfg, self.model, save_dir=save_dir)
        _ = checkpointer.load(cfg.MODEL.WEIGHT)

        self.transforms = self.build_transform()

        mask_threshold = -1 if show_mask_heatmaps else 0.5
        self.masker = Masker(threshold=mask_threshold, padding=1)

        # used to make colors for each class
        self.palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])

        self.cpu_device = torch.device("cpu")
        self.confidence_threshold = confidence_threshold
        self.show_mask_heatmaps = show_mask_heatmaps
        self.masks_per_dim = masks_per_dim

    def build_transform(self):
        """
        Creates a basic transformation that was used to train the models
        """
        cfg = self.cfg

        # we are loading images with OpenCV, so we don't need to convert them
        # to BGR, they are already! So all we need to do is to normalize
        # by 255 if we want to convert to BGR255 format, or flip the channels
        # if we want it to be in RGB in [0-1] range.
        if cfg.INPUT.TO_BGR255:
            to_bgr_transform = T.Lambda(lambda x: x * 255)
        else:
            to_bgr_transform = T.Lambda(lambda x: x[[2, 1, 0]])

        normalize_transform = T.Normalize(
            mean=cfg.INPUT.PIXEL_MEAN, std=cfg.INPUT.PIXEL_STD
        )

        transform = T.Compose(
            [
                T.ToPILImage(),
                #T.Resize(self.min_image_size),
                T.ToTensor(),
                #to_bgr_transform,
                normalize_transform,
            ]
        )
        return transform

    def run_on_opencv_image(self, image,img_show):
        """
        Arguments:
            image (np.ndarray): an image as returned by OpenCV
        Returns:
            prediction (BoxList): the detected objects. Additional information
                of the detection properties can be found in the fields of
                the BoxList via `prediction.fields()`
        """
        predictions = self.compute_prediction(image)
        top_predictions = self.select_top_predictions(predictions)

        #result = image.copy()
        result=img_show
        if self.show_mask_heatmaps:
            return self.create_mask_montage(result, top_predictions)

        # Todo(Clark): Change the order to apply mask first

        # apply box, update to save the coordinates
        result,top_predictions_bbox = self.overlay_boxes(result, top_predictions)

        # apply mask
        result, mask_output,top_predictions_mask = self.overlay_mask(result, top_predictions_bbox)

        # # apply box
        # result = self.overlay_boxes(result, top_predictions)
        #
        # if self.cfg.MODEL.MASK_ON:
        #     result,mask_out = self.overlay_mask(result, top_predictions)

        # if self.cfg.MODEL.KEYPOINT_ON:
        #     result = self.overlay_keypoints(result, top_predictions)

        result = self.overlay_class_names(result, top_predictions_mask)

        return result,mask_output

    def compute_prediction(self, original_image):
        """
        Arguments:
            original_image (np.ndarray): an image as returned by OpenCV
        Returns:
            prediction (BoxList): the detected objects. Additional information
                of the detection properties can be found in the fields of
                the BoxList via `prediction.fields()`
        """
        # apply pre-processing to image
        image = self.transforms(original_image)
        # convert to an ImageList, padded so that it is divisible by
        # cfg.DATALOADER.SIZE_DIVISIBILITY
        image_list = to_image_list(image, self.cfg.DATALOADER.SIZE_DIVISIBILITY)
        image_list = image_list.to(self.device)
        # compute predictions
        with torch.no_grad():
            predictions = self.model(image_list)
        predictions = [o.to(self.cpu_device) for o in predictions]

        # always single image is passed at a time
        prediction = predictions[0]

        # reshape prediction (a BoxList) into the original image size
        height, width = original_image.shape[:-1]
        prediction = prediction.resize((width, height))

        if prediction.has_field("mask"):
            # if we have masks, paste the masks in the right position
            # in the image, as defined by the bounding boxes
            masks = prediction.get_field("mask")
            # always single image is passed at a time
            masks = self.masker([masks], [prediction])[0]
            prediction.add_field("mask", masks)
        return prediction

    def select_top_predictions(self, predictions):
        """
        Select only predictions which have a `score` > self.confidence_threshold,
        and returns the predictions in descending order of score
        Arguments:create_mask_montage
            predictions (BoxList): the result of the computation by the model.
                It should contain the field `scores`.
        Returns:
            prediction (BoxList): the detected objects. Additional information
                of the detection properties can be found in the fields of
                the BoxList via `prediction.fields()`
        """
        scores = predictions.get_field("scores")
        keep = torch.nonzero(scores > self.confidence_threshold).squeeze(1)
        predictions = predictions[keep]
        scores = predictions.get_field("scores")
        _, idx = scores.sort(0, descending=True)
        return predictions[idx]

    def compute_colors_for_labels(self, labels):
        """
        Simple function that adds fixed colors depending on the class
        """
        # colors = labels[:, None] * self.palette
        # colors = (colors % 255).numpy().astype("uint8")

        temp_labels=(labels[:, None]).numpy().astype("int8").tolist()
        colors=[]
        for i in temp_labels:
            colors.append([   Color_dict[i[0]][2],Color_dict[i[0]][1],Color_dict[i[0]][0]])
        return colors

    def py_mask_nms(self, masks, scores, threshold=0.5):


        if (masks.shape)[0]!=0:
            _, row, column = masks[0].shape
        else:
            return torch.LongTensor([])

        areas=[]
        for mask in masks:
            thresh=mask[0, :, :, None]
            area=np.sum(thresh[:, :, 0].squeeze())
            areas.append(area)
        areas = np.array(areas)
        _, order = scores.sort(0, descending=True)
        keep = []
        while order.numel() > 0:
            if order.numel() == 1:
                i = order.item()
                keep.append(i)
                break
            else:
                i = order[0].item()
                keep.append(i)

            inter=[]
            list_inter = masks[order[0]] * masks[order[1:]]
            for j in list_inter:
                inter.append(np.sum(j.squeeze()))
            inter=np.array(inter)
            iou = np.array(inter / (areas[i] + areas[order[1:]] - inter))  # [N-1,]
            ## Todo(Clark): Maybe not good to hack here.
            iou2= np.array(inter / (areas[order[1:]]))
            idx=np.nonzero((iou <= threshold) & (iou2<= 0.8))
            if np.size(idx) == 0:
                break
            order = order[idx[0] + 1]
        return torch.LongTensor(keep)

    def overlay_boxes(self, image, predictions):
        """
        Adds the predicted boxes on top of the image
        Arguments:
            image (np.ndarray): an image as returned by OpenCV
            predictions (BoxList): the result of the computation by the model.
                It should contain the field `labels`.
        """
        # build up a blank txt
        # filepath = os.path.join(dir_path, 'bbox_saver_%s.txt' % str(index))
        # with open(filepath, "w") as f:
        #     f.close()


        boxes = predictions.bbox

        ## ROI
        row, column, _ = image.shape
        keep = []
        idx = 0
        for box in boxes:
            box = box.to(torch.int64)
            top_left, bottom_right = box[:2].tolist(), box[2:].tolist()

            # Todo(Clark):
            if not (40<top_left[0] and top_left[0]<row-20 and 25<top_left[1] and top_left[1]<column-40 and
                40 < bottom_right[0] and bottom_right[0] < row-20 and 25 < bottom_right[1] and bottom_right[1] < column-40):
                idx = idx + 1
                continue

            keep.append(idx)

            idx = idx + 1
        predictions_afterROI = predictions[torch.from_numpy(np.array(keep)).type(torch.int64)]


        # ## NMS
        # boxes = predictions_afterROI.bbox
        # scores = predictions_afterROI.get_field("scores")
        #
        #
        # if boxes.numel() == 0:
        #     keep_nms = torch.empty((0,), dtype=torch.int64, device=boxes.device)
        #
        # keep_nms= self.py_nms(boxes, scores, 0.55)
        #
        # # keep_nms=torchvision.ops.nms(boxes, scores, 0.7)
        #
        # predictions_afterNMS = predictions_afterROI[keep_nms]



        # ## Paint
        # labels = predictions_afterNMS.get_field("labels")
        # boxes = predictions_afterNMS.bbox
        # colors = self.compute_colors_for_labels(labels).tolist()
        #
        # for box, color in zip(boxes, colors):
        #     box = box.to(torch.int64)
        #     top_left, bottom_right = box[:2].tolist(), box[2:].tolist()
        #
        #
        #     with open(filepath, "a+") as f:
        #         f.write(str(top_left) + "\t" + str(bottom_right))
        #         f.write("\n")
        #         f.close()
        #
        #     image = cv2.rectangle(
        #         image, tuple(top_left), tuple(bottom_right), tuple(color), 1
        #     )
        return image, predictions_afterROI
        # return image,predictions_afterNMS

    def overlay_mask(self, image, predictions,alpha=0.4):
        """
        Adds the instances contours for each predicted object.
        Each label has a different color.
        Arguments:
            image (np.ndarray): an image as returned by OpenCV
            predictions (BoxList): the result of the computation by the model.
                It should contain the field `mask` and `labels`.
        """

        ## NMS
        masks = predictions.get_field("mask").numpy()
        scores = predictions.get_field("scores")
        labels = predictions.get_field("labels")



        keep_nms=self.py_mask_nms(masks,scores, 0.4)
        predictions_afterNMS = predictions[keep_nms]


        ## Paint
        masks = predictions_afterNMS.get_field("mask").numpy()
        labels = predictions_afterNMS.get_field("labels")

        # colors = self.compute_colors_for_labels(labels).tolist()
        colors = self.compute_colors_for_labels(labels)
        row, column, _ = image.shape




        mask_output = []

        # Todo(Clark): Changed to save mask
        for mask, color, label in zip(masks, colors, labels):
            single_mask = np.zeros((row, column))
            thresh = mask[0, :, :, None]
            contours, hierarchy = cv2_util.findContours(
                thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )
            label = label.numpy()
            single_mask = single_mask + thresh[:, :, 0] * label
            mask_output.append(single_mask)
            image = cv2.drawContours(image, contours, -1, color, 1)
            for c in range(3):
                image[:, :, c] = np.where(single_mask == label,
                                        image[:, :, c] *
                                        (1 - alpha) + alpha * color[c],
                                        image[:, :, c])


        ## Old
        # masks = predictions.get_field("mask").numpy()
        # labels = predictions.get_field("labels")
        #
        # colors = self.compute_colors_for_labels(labels).tolist()
        #
        # row, column, _ = image.shape
        #
        # mask_output = []
        #
        # # Todo(Clark): Changed to save mask
        # for mask, color, label in zip(masks, colors, labels):
        #     single_mask = np.zeros((row, column))
        #     thresh = mask[0, :, :, None]
        #     contours, hierarchy = cv2_util.findContours(
        #         thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        #     )
        #     label = label.numpy()
        #     single_mask = single_mask + thresh[:, :, 0] * label
        #     mask_output.append(single_mask)
        #     image = cv2.drawContours(image, contours, -1, color, 3)

        ## Original
        # for mask, color in zip(masks, colors):
        #     thresh = mask[0, :, :, None]
        #     contours, hierarchy = cv2_util.findContours(
        #         thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        #     )
        #     image = cv2.drawContours(image, contours, -1, color, 3)

        composite = image

        return composite,mask_output,predictions_afterNMS

    def overlay_keypoints(self, image, predictions):
        keypoints = predictions.get_field("keypoints")
        kps = keypoints.keypoints
        scores = keypoints.get_field("logits")
        kps = torch.cat((kps[:, :, 0:2], scores[:, :, None]), dim=2).numpy()
        for region in kps:
            image = vis_keypoints(image, region.transpose((1, 0)))
        return image

    def create_mask_montage(self, image, predictions):
        """
        Create a montage showing the probability heatmaps for each one one of the
        detected objects
        Arguments:
            image (np.ndarray): an image as returned by OpenCV
            predictions (BoxList): the result of the computation by the model.
                It should contain the field `mask`.
        """
        masks = predictions.get_field("mask")
        masks_per_dim = self.masks_per_dim
        masks = L.interpolate(
            masks.float(), scale_factor=1 / masks_per_dim
        ).byte()
        height, width = masks.shape[-2:]
        max_masks = masks_per_dim ** 2
        masks = masks[:max_masks]
        # handle case where we have less detections than max_masks
        if len(masks) < max_masks:
            masks_padded = torch.zeros(max_masks, 1, height, width, dtype=torch.uint8)
            masks_padded[: len(masks)] = masks
            masks = masks_padded
        masks = masks.reshape(masks_per_dim, masks_per_dim, height, width)
        result = torch.zeros(
            (masks_per_dim * height, masks_per_dim * width), dtype=torch.uint8
        )
        for y in range(masks_per_dim):
            start_y = y * height
            end_y = (y + 1) * height
            for x in range(masks_per_dim):
                start_x = x * width
                end_x = (x + 1) * width
                result[start_y:end_y, start_x:end_x] = masks[y, x]
        return cv2.applyColorMap(result.numpy(), cv2.COLORMAP_JET)

    def overlay_class_names(self, image, predictions):
        """
        Adds detected class names and scores in the positions defined by the
        top-left corner of the predicted bounding box
        Arguments:
            image (np.ndarray): an image as returned by OpenCV
            predictions (BoxList): the result of the computation by the model.
                It should contain the field `scores` and `labels`.
        """
        scores = predictions.get_field("scores").tolist()
        labels = predictions.get_field("labels").tolist()
        labels = [self.CATEGORIES[i] for i in labels]
        boxes = predictions.bbox

        template = "{}: {:.2f}"
        for box, score, label in zip(boxes, scores, labels):
            x, y = box[:2]
            s = template.format(label, score)
            cv2.putText(
                image, s, (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1
            )

        return image

import numpy as np
import matplotlib.pyplot as plt
from maskrcnn_benchmark.structures.keypoint import PersonKeypoints

def vis_keypoints(img, kps, kp_thresh=2, alpha=0.7):
    """Visualizes keypoints (adapted from vis_one_image).
    kps has shape (4, #keypoints) where 4 rows are (x, y, logit, prob).
    """
    dataset_keypoints = PersonKeypoints.NAMES
    kp_lines = PersonKeypoints.CONNECTIONS

    # Convert from plt 0-1 RGBA colors to 0-255 BGR colors for opencv.
    cmap = plt.get_cmap('rainbow')
    colors = [cmap(i) for i in np.linspace(0, 1, len(kp_lines) + 2)]
    colors = [(c[2] * 255, c[1] * 255, c[0] * 255) for c in colors]

    # Perform the drawing on a copy of the image, to allow for blending.
    kp_mask = np.copy(img)

    # Draw mid shoulder / mid hip first for better visualization.
    mid_shoulder = (
        kps[:2, dataset_keypoints.index('right_shoulder')] +
        kps[:2, dataset_keypoints.index('left_shoulder')]) / 2.0
    sc_mid_shoulder = np.minimum(
        kps[2, dataset_keypoints.index('right_shoulder')],
        kps[2, dataset_keypoints.index('left_shoulder')])
    mid_hip = (
        kps[:2, dataset_keypoints.index('right_hip')] +
        kps[:2, dataset_keypoints.index('left_hip')]) / 2.0
    sc_mid_hip = np.minimum(
        kps[2, dataset_keypoints.index('right_hip')],
        kps[2, dataset_keypoints.index('left_hip')])
    nose_idx = dataset_keypoints.index('nose')
    if sc_mid_shoulder > kp_thresh and kps[2, nose_idx] > kp_thresh:
        cv2.line(
            kp_mask, tuple(mid_shoulder), tuple(kps[:2, nose_idx]),
            color=colors[len(kp_lines)], thickness=2, lineType=cv2.LINE_AA)
    if sc_mid_shoulder > kp_thresh and sc_mid_hip > kp_thresh:
        cv2.line(
            kp_mask, tuple(mid_shoulder), tuple(mid_hip),
            color=colors[len(kp_lines) + 1], thickness=2, lineType=cv2.LINE_AA)

    # Draw the keypoints.
    for l in range(len(kp_lines)):
        i1 = kp_lines[l][0]
        i2 = kp_lines[l][1]
        p1 = kps[0, i1], kps[1, i1]
        p2 = kps[0, i2], kps[1, i2]
        if kps[2, i1] > kp_thresh and kps[2, i2] > kp_thresh:
            cv2.line(
                kp_mask, p1, p2,
                color=colors[l], thickness=2, lineType=cv2.LINE_AA)
        if kps[2, i1] > kp_thresh:
            cv2.circle(
                kp_mask, p1,
                radius=3, color=colors[l], thickness=-1, lineType=cv2.LINE_AA)
        if kps[2, i2] > kp_thresh:
            cv2.circle(
                kp_mask, p2,
                radius=3, color=colors[l], thickness=-1, lineType=cv2.LINE_AA)

    # Blend the keypoints.
    return cv2.addWeighted(img, 1.0 - alpha, kp_mask, alpha, 0)
