#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# FILE: average-filter.py
#
# @author: Arafat Hasan Jenin <opendoor.arafat[at]gmail[dot]com>
#
# DATE CREATED: 08-12-19 21:05:54 (+06)
# LAST MODIFIED: 23-12-19 01:00:23 (+06)
#
# DEVELOPMENT HISTORY:
# Date         Version     Description
# --------------------------------------------------------------------
# 08-12-19     1.0         Deleted code is debugged code.
#
#               _/  _/_/_/_/  _/      _/  _/_/_/  _/      _/
#              _/  _/        _/_/    _/    _/    _/_/    _/
#             _/  _/_/_/    _/  _/  _/    _/    _/  _/  _/
#      _/    _/  _/        _/    _/_/    _/    _/    _/_/
#       _/_/    _/_/_/_/  _/      _/  _/_/_/  _/      _/
#
##############################################################################

import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.exposure import rescale_intensity
import os
import sys


def convolve(image, kernel):
    (iH, iW) = image.shape[:2]
    (kH, kW) = kernel.shape[:2]

    pad = (kW - 1) // 2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    output = np.zeros((iH, iW), dtype="float32")

    for y in np.arange(pad, iH + pad):
        for x in np.arange(pad, iW + pad):
            roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
            k = (roi * kernel).sum()
            output[y - pad, x - pad] = k

    output = rescale_intensity(output, in_range=(0, 255))
    output = (output * 255).astype("uint8")

    return output


if __name__ == '__main__':
    path = 'img/lennaNoisy.png'

    if os.path.isfile(path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        print("[INFO] Image has been read successfully...")
    else:
        print("[INFO] The file '" + path + "' does not exist.")
        sys.exit(0)

    averageKernel = np.ones((3, 3), np.float32) / 9

    print("[INFO] Applying average kernel...")
    convoleOutput = convolve(img, averageKernel)

    titles = ['Input Image', 'After Applying Average Filter']
    imgarr = [img, convoleOutput]
    for i in range(2):
        plt.subplot(1, 2, i + 1)
        plt.imshow(imgarr[i], cmap='gray', vmin=0, vmax=255)
        plt.title(titles[i])
        plt.xticks([])
        plt.yticks([])

    plt.show()

    print("[INFO] All operations finished successfully...")
