import glob
import os
import copy
import shutil
import random
from skimage import io
from skimage.transform import rescale, resize
import skimage.exposure
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import config


def random_brightness(image):
  transform = A.RandomBrightnessContrast(p=0.4)
  augmentations = transform(image = image)
  im = Image.fromarray(augmentations['image'])
  return im

def apply_rgbshift(image):
  transform = A.RGBShift(r_shift_limit=30, g_shift_limit=30, b_shift_limit=30, p=1)
  augmentations = transform(image = image)
  im = Image.fromarray(augmentations['image'])
  return im

def apply_clahe(image):
  clip_limit=6.0
  tile_grid_size=(16, 16)

  transform = A.CLAHE(clip_limit, tile_grid_size, p=1.0)
  augmentations = transform(image = image)
  im = Image.fromarray(augmentations['image'])
  return im

def apply_rotation(image, mask):
  angle = random.randint(0, 90)
  transform = A.Rotate(limit=[angle, angle], p=1.0, border_mode=cv2.BORDER_CONSTANT)

  augmentations = transform(image = image)
  im = Image.fromarray(augmentations['image'])

  augmentations = transform(image = mask)
  msk = Image.fromarray(augmentations['image'])

  return im, msk


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


def find_closest_temporal_neighbor(path, images, threshold, resize_ratio = None, resizing = False, normalize = True, printing= False):
    """
    Find the closest temporal neighbor for an image that does not follow np.sum(img)>threshold. The best image is chosen 
    based on the distance calculated by the counters upward and backward, the closest to the current image will be replaced.

    ::param path: current image to be exhanged
    ::param images: list of images in current folder containing collection of possible candidates
    ::param threshold: minimum threshold to choose image. Integer representing the sum of pixels across width/height 

    return  image: the best possible replacement for current image.
    """
    upward = 0
    backward = 0
    current_idx = images.index(path)
    t1 = upward + current_idx 
    t2 = current_idx - backward
    neighborUp = ""
    neighborDown = ""
    img_up = read_tiff(images[t1], config.image_size, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
    img_down = read_tiff(images[t2], config.image_size,  resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
    # Analize future images and initialize counter
    while t1<=len(images) and np.sum(img_up)<threshold:
        t1+=1
        upward+=1
        img_up = read_tiff(images[t1], config.image_size,  resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
        neighborUp = images[t1]
    # Analize images in the past and initialize counter
    while t2>=0 and np.sum(img_down)<threshold:
        # if index starts off from 0, bound limits
        t2 = int([0 if t2==0 else t2-1][0]) 
        backward+=1
        img_down = read_tiff(images[t2], config.image_size, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
        neighborDown = images[t2]
        # If t2 = 0 and np.sum(image[t2])<0 while np.sum(image[t1])>threshold, 
        # choose upward by making backward>upward so upward is taken
        if t2==0 and np.sum(img_down)<=threshold:
            backward=upward+1
            t2=t1
            break
    current = os.path.join(images[current_idx].split("/")[-2:][0], images[current_idx].split("/")[-2:][1])
    f_img = os.path.join(images[t1].split("/")[-2:][0], images[t1].split("/")[-2:][1])
    b_img = os.path.join(images[t2].split("/")[-2:][0], images[t2].split("/")[-2:][1])
    
    if upward<backward :
        img = read_tiff(images[t1], config.image_size, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
        assert np.sum(img_up)>=threshold, "image < threshold"
        print(f"-->[FORWARD] - image {current} will be replaced with {f_img} - Temporal distance = [Forward = {upward}, backward = {backward}]")
        return img
    elif upward>backward:
        img = read_tiff(images[t2], config.image_size, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
        assert np.sum(img_down)>=threshold, "image < threshold"
        print(f"-->[BACKWARDS] - image {current} will be replaced with {b_img} - Temporal distance = [Forward = {upward}, backward = {backward}]")
        return img
    elif upward==backward:
        r = [t1 if random.choice(["t1","t2"]) == "t1" else t2][0]
        random_img = os.path.join(images[r].split("/")[-2:][0], images[r].split("/")[-2:][1])
        img = read_tiff(images[r], config.image_size, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
        print(f"-->[EQUIDISTANT] - image {current} will be replaced with {random_img} - Temporal distance = [Forward = {upward} = backward = {backward}]")
        return img