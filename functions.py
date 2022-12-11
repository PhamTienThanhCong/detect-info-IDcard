import numpy as np 
from detecto import core, utils, visualize
import cv2

model = core.Model.load('./model/id_card_4_corner.pth', ['top_left', 'top_right', 'bottom_left', 'bottom_right'])
# function

def perspective_transoform(image, source_points):
    dest_points = np.float32([[0,0], [500,0], [500,300], [0,300]])
    M = cv2.getPerspectiveTransform(source_points, dest_points)
    dst = cv2.warpPerspective(image, M, (500, 300))
    
    return dst

def get_center_point(box):
    xmin, ymin, xmax, ymax = box
    return (xmin + xmax) // 2, (ymin + ymax) // 2

def non_max_suppression_fast(boxes, labels, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    #  
    # initialize the list of picked indexes   
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
         np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type
    
    final_labels = [labels[idx] for idx in pick]
    final_boxes = boxes[pick].astype("int")
    
    return final_boxes, final_labels

def detect_id_cart(image):
    # detect object
    labels, boxes, scores = model.predict(image)
    # check if all 4 corners are detected
    if "bottom_left" not in labels:
        return None
    if "bottom_right" not in labels:
        return None
    if "top_left" not in labels:
        return None
    if "top_right" not in labels:
        return None
    image2 = image.copy()
    # for i, bbox in enumerate(boxes):
    #     bbox = list(map(int, bbox))
    #     x_min, y_min, x_max, y_max = bbox
    #     cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),2)
    #     cv2.putText(image, labels[i], (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    final_boxes, final_labels = non_max_suppression_fast(np.array(boxes), labels, 0.3) 
    final_points = list(map(get_center_point, final_boxes))
    label_boxes = dict(zip(final_labels, final_points))
    source_points = np.float32([
        label_boxes['top_left'], label_boxes['top_right'], label_boxes['bottom_right'], label_boxes['bottom_left']
    ])

    # Transform 
    crop = perspective_transoform(image2, source_points)

    return crop
