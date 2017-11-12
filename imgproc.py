# -*- coding: utf-8 -*-
import cv2
import numpy as np
import operator


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def add_overlay(background, overlay, (locx, locy), scale, angle):
    """ Добавляет изображение с альфа-каналом на статическое изображение """
    output = background

    a_rad = np.fabs(np.deg2rad(angle))

    cy, cx = overlay.shape[:2]
    h, w = cy * scale, cx * scale
    rotmat = cv2.getRotationMatrix2D((cx / 2, cy / 2), angle, scale)
    rotated = cv2.warpAffine(overlay, rotmat, (cx, cy))

    dy = np.cos(a_rad) * (h / 2) + np.sin(a_rad) * (w / 2)
    dx = np.cos(a_rad) * (w / 2) + np.sin(a_rad) * (h / 2)
    y1, y2 = int((cy / 2) - dy), int((cy / 2) + dy)
    x1, x2 = int((cx / 2) - dx), int((cx / 2) + dx)

    roi = rotated[y1:y2, x1:x2]

    bg_rows, bg_cols, bg_ch = background.shape
    ov_rows, ov_cols, ov_ch = roi.shape
    if ov_ch != 4:
        raise ValueError('Invalid overlay, must be with alpha-channel.')

    for y in range(max(int(locy - ov_rows / 2), 0), min(bg_rows, int(locy + ov_rows / 2))):
        for x in range(max(int(locx - ov_cols / 2), 0), min(bg_cols, int(locx + ov_cols / 2))):
            fX, fY = x - int(locx - ov_cols / 2), y - int(locy - ov_rows / 2)
            opacity = roi[fY, fX, 3] / 255.
            if opacity > 0.:
                output[y, x] = ((1. - opacity) * background[y, x]) + (opacity * (roi[fY, fX][:3]))

    return output


def get_eye_line(img, cascade, nested):
    """ Находит линию глаз """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    rects = detect(gray, cascade)

    if len(rects) == 0:
        return None

    vis = img.copy()
    x01, y01, x02, y02 = rects[0]
    roi = gray[y01:y02, x01:x02]
    vis_roi = vis[y01:y02, x01:x02]
    subrects = detect(roi.copy(), nested)

    if len(subrects) == 0:
        return None

    w = vis_roi.shape[0]
    rect_count, _ = subrects.shape
    points = []
    for i in range(rect_count):
        x1, y1, x2, y2 = subrects[i]
        points.append(((x1 + x2) / 2., (y1 + y2) / 2.))

    if len(points) == 2:
        # найдено два глаза
        pass
    elif len(points) == 1:
        return None
    elif len(points) == 0:
        return None
    else:
        # Найдено более двух глаз. Как правило, глаза - самые разнесенные по x точки
        points = sorted(points, key=operator.itemgetter(0))
        points = [points[0], points[-1]]

    x1, y1 = points[0]
    x2, y2 = points[1]

    alpha = np.arctan((y1 - y2) / (x2 - x1))
    center = (x01 + x1 + (x2 - x1) / 2, y01 + y1 + (y2 - y1) / 2)
    width = w / np.cos(alpha)

    return width, center, alpha


def get_mixed(img, specs, session):
    cascade_fn = "cv_data/haarcascades/haarcascade_frontalface_alt.xml"
    nested_fn = "cv_data/haarcascades/haarcascade_eye.xml"
    cascade = cv2.CascadeClassifier(cascade_fn)
    nested = cv2.CascadeClassifier(nested_fn)

    k = 0.88

    eye_line = get_eye_line(img, cascade, nested)
    if eye_line is None:
        if 'eye_line' in session.keys():
            eye_line = session['eye_line']
        else:
            return img

    session['eye_line'] = eye_line
    width, center, alpha = eye_line
    img = add_overlay(img, specs, center, k * width / specs.shape[1], np.rad2deg(alpha))

    return img
