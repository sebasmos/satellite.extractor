import config
import shutil
import utils as util
import os
import glob 
from os.path import exists
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import time


if __name__ == "__main__":
    resize_ratio = config.resize_ratio
    resizing = config.resizing
    normalize = config.normalize
    printing= config.printing
    count = 0
    threshold = config.threshold
    neighbor = ""
    root = config.root
    baseline = config.DATASET
    # Path to dataset with improved images
    aug_root =  config.aug_root
    print(f"root: ", root)
    print(f"baseline: ", baseline)
    print(f"aug_root: ", aug_root)
    CLEAN = False
    #import pdb
    #pdb.set_trace()
    #if CLEAN:
    if not os.path.exists(aug_root):
        shutil.copytree(baseline, aug_root,dirs_exist_ok=True)
        #shutil.rmtree(aug_root)
    #else: 
    #    try:
    #        shutil.copytree(baseline, aug_root,dirs_exist_ok=True)
    #    except:
    #        pass
    if __name__ == "__main__":
        a = 0
        root = config.DATASET
        for city in os.listdir(root):
            start_time = time.time()
            list_images = []
            images_path = os.path.join(root, city)
            images = sorted(glob.glob(os.path.join(images_path)+"/*.tiff")) # use sorted to align images temporally back-forwards
            #print(f"Total # images before augmentation: ", len(images))
            print(f'{city} : {len(os.listdir(images_path))} images '.center(60,"-"))
            for img_path in sorted(os.listdir(images_path)):
                path = os.path.join(root, city, img_path)
                image_name = os.path.join(path.split("/")[-2:][0], path.split("/")[-2:][1])
                img = util.read_tiff(path, config.image_size, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
                if np.sum(img)<threshold:
                    # if image content is lower than threshold, replace with the "best" image
                    img = util.find_closest_temporal_neighbor(path, images, threshold, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
                    assert np.sum(img)>=threshold, "img is above threshold"
                    aug_path = os.path.join(aug_root, city, path.split("/")[-2:][1])
                    os.makedirs(os.path.join(aug_root, city), exist_ok=True)
                    print(f"[{count}] Storing augmented image version of {image_name} in: {aug_path}")
                    print(img.shape)
                    if exists(aug_path):
                        os.remove(aug_path)
                        io.imsave(aug_path, img)
                    else: 
                        io.imsave(aug_path, img)
                    #display =False
                    #
                    
                    #plt.figure(figsize=(9, 3))
                    #print(img[:,:,1:4].shape)
                    #plt.imshow(img[:,:,1:4])
                    
                else:
                    print(f"[{count}] - Image {path} remains unchanged..")
                count+=1
                #if count==5:
                #    break
            images = sorted(glob.glob(os.path.join(aug_root)+"/*.tiff")) # use sorted to align images temporally back-forwards
            print(f"Total # images: ", len(images))