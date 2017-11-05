# -*- coding: utf-8 -*-
import cv2


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def get_mixed(img, spectacles):
    cascade_fn = "cv_data/haarcascades/haarcascade_frontalface_alt.xml"
    # nested_fn  = "cv_data/haarcascades/haarcascade_eye.xml"
    cascade = cv2.CascadeClassifier(cascade_fn)
    # nested = cv2.CascadeClassifier(nested_fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    rects = detect(gray, cascade)
    vis = img.copy()
    draw_rects(vis, rects, (0, 255, 0))

    # if not nested.empty():
    #     for x1, y1, x2, y2 in rects:
    #         roi = gray[y1:y2, x1:x2]
    #         vis_roi = vis[y1:y2, x1:x2]
    #         subrects = detect(roi.copy(), nested)
    #         draw_rects(vis_roi, subrects, (255, 0, 0))

    return vis
