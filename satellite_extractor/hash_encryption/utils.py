import os
import sys
current_directory = os.getcwd()

# Add the current directory to sys.path if it's not already there
if current_directory not in sys.path:
    sys.path.append(current_directory)

import config
import os
import matplotlib.pyplot as plt
import glob
import os
import copy
import shutil
import random
import cv2
from skimage import io
from skimage.transform import rescale, resize
import skimage.exposure
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def read_tiff(img_path, image_size, resize_ratio=None, resizing = True, normalize=True, printing=True):
  img = io.imread(img_path)
  img_F =img.copy()
  if resize_ratio:
    img_F = rescale(img, resize_ratio, anti_aliasing=True)
  if resizing:
    img_F = resize(img_F, (image_size, image_size), anti_aliasing=True)
  
  path_img = os.path.basename(img_path)
  if normalize:
    CHANNELS = range(12)
    img_F = np.dstack([
        skimage.exposure.rescale_intensity(img_F[:,:,c], out_range=(0, 1)) 
        for c in CHANNELS])
  if printing:
    print(f"(origin shape: {path_img}: {img.shape} -> rescale: {str(img_F.shape)}) - Range -> [{img_F.min(), img_F.max()}]")
  return img_F

def hash_difference(image, hashSize=8):
	resized = cv2.resize(image, (hashSize + 1, hashSize))
	diff = resized[:, 1:] > resized[:, :-1]
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])