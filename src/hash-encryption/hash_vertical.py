from genericpath import exists
import config
import os
import matplotlib.pyplot as plt
import glob
import os
import copy
import shutil
import cv2 
from PIL import Image
import random
import datetime
import time
from skimage import io
from skimage.transform import rescale, resize
import skimage.exposure
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import utils as utils
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
viz = os.path.join(ROOT_DIR, config.visualization)
os.makedirs(viz, exist_ok=True)

if __name__ == "__main__":
    a = 0
    root = config.DATASET
    for city in os.listdir(root):
        start_time = time.time()
        list_images = []
        images_path = os.path.join(root, city)
        print(f'{city} : {len(os.listdir(images_path))} images '.center(60,"-"))
        for img_path in os.listdir(images_path):
            path = os.path.join(root, city, img_path)
            print("Processing image ", os.path.join(root, city, img_path))
            img = utils.read_tiff(path, config.image_size, resize_ratio=config.resize_ratio, resizing = config.resizing, normalize=config.normalize, printing=config.printing)
            list_images.append(img)
        total_time = time.time() - start_time
        total_time_str = str(datetime.timedelta(seconds=int(total_time)))
        print(f'Training time for {city} : {total_time_str}')
        m = np.array(list_images)
        print(np.array(list_images).shape)
        dict_hash = []
        for img in m:
            imageHash = utils.hash_difference(img)
            dict_hash.append(imageHash)
        data = {"img_hash": dict_hash,"img_names": os.listdir(images_path) }
        df = pd.DataFrame(data = data)
        num_img_per_hash = df.groupby("img_hash").size().sort_values(ascending = False).reset_index(name = "img_names")
        print(num_img_per_hash)
        #display(num_img_per_hash.head(10))
        print(sum(num_img_per_hash["img_names"]))
        ax = plt.figure()
        num_img_per_hash.hist("img_names", bins = 20, orientation = "vertical",  color='#86bf91',  edgecolor='black', linewidth=1.2)
        plt.xlabel("Relative Frequency")
        plt.ylabel("Number of Encrypted images")
        plt.title('')
        plt.xlim(1, num_img_per_hash.img_names[0])
        plt.grid(False)

        # ------- 
        # make the y ticks integers, not floats
        xint = []
        locs, labels = plt.xticks()
        for each in locs:
            xint.append(int(each))
        plt.xticks(xint)
        # -------
        plt.savefig(f'{viz}/{city}.png', transparent=True)

        #a+=1
        #if a==1:
        #    break



