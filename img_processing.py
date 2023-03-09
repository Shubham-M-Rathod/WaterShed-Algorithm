import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def create_rgb(i):
    x = np.array(cm.tab10(i))[:3] * 255
    return tuple(x)


def mouse_callback(event, x, y, flags, param):
    global marks_updated

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(marker_image, (x, y), 10, (current_marker), -1)

        cv2.circle(img_copy, (x, y), 10, colors[current_marker], -1)
        marks_updated = True


img = cv2.imread('upload.jpg')
img_copy = np.copy(img)
marker_image = np.zeros(img.shape[:2], dtype=np.int32)
segments = np.zeros(img.shape, dtype=np.uint8)

colors = []
for i in range(10):
    colors.append(create_rgb(i))

current_marker = 1
marks_updated = False

cv2.namedWindow('Image')
cv2.namedWindow('WaterShed Segments')
cv2.setMouseCallback('Image', mouse_callback)

while True:
    cv2.imshow('WaterShed Segments', segments)
    cv2.imshow('Image', img_copy)
    k = cv2.waitKey(1)
    if k == 27:
        break

    elif k == ord('c'):
        img_copy = img.copy()
        marker_image = np.zeros(img.shape[0:2], dtype=np.int32)
        segments = np.zeros(img.shape, dtype=np.uint8)

    elif k > 0 and chr(k).isdigit():
        current_marker = int(chr(k))
        n = int(chr(k))
        if 1 <= n <= 10:
            current_marker = n

    if marks_updated:
        marker_image_copy = marker_image.copy()
        cv2.watershed(img, marker_image_copy)
        segments = np.zeros(img.shape, dtype=np.uint8)

        for color_ind in range(10):
            segments[marker_image_copy == (color_ind)] = colors[color_ind]

        marks_updated = False

cv2.destroyAllWindows()