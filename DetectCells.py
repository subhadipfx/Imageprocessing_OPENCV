import cv2
import numpy as np
from imutils.contours import sort_contours


def draw_lines(img_for_box_extraction_path):
    dimension = []
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image

    (thresh, img_bin) = cv2.threshold(img, 127, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255 - img_bin  # Invert the image

    kernel_length = np.array(img).shape[1] // 40
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    contours_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)

    # extracting Contours
    contours, hierarchy = cv2.findContours(
        contours_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")  # Sorting in decending order by area
    contours = contours[1:]  # removing largest contour

    #  print(len(contours))

    # Getting contours dimension
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        dim = (x, y, w, h)
        dimension.append(dim)
    vis = cv2.imread(img_for_box_extraction_path)

    # horizontal lines
    for i in range(len(contours)):
        x, y, w, h = dimension[i]
        cv2.line(vis,
                 (x, y),
                 (x + w, y),
                 (0, 0, 255),
                 2)
        cv2.line(vis,
                 (x, y + h),
                 (x + w, y + h),
                 (0, 0, 255),
                 2)
    # vertical lines
    _, endy, _, _ = dimension[-1]
    for i in range(10):
        x, y, w, h = dimension[i]
        cv2.line(vis, (x, y),
                 (x, endy),
                 (0, 0, 255),
                 2)
        cv2.line(vis, (x + w, y),
                 (x + w, endy),
                 (0, 0, 255),
                 2)

    cv2.imwrite(f + '_cells.png', vis)


print('Enter File Name(with extension like icici.png):\n')
f = input()
draw_lines(f)
