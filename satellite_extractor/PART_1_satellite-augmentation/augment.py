import config
import shutil
import utils as util
import os
import glob 
from os.path import exists
import numpy as np
from skimage import io
import matplotlib.pyplot as plt

if __name__ == "__main__":
    resize_ratio = config.resize_ratio
    resizing = config.resizing
    normalize = config.normalize
    printing= config.printing
    count = 0
    threshold = config.threshold
    neighbor = ""
    root = config.root
    code = config.code
    baseline = config.baseline
    # Path to dataset with improved images
    aug_root =  config.aug_root
    print(f"root: ", root)
    print(f"baseline: ", baseline)
    print(f"aug_root: ", aug_root)
    CLEAN = False
    if CLEAN:
        shutil.rmtree(aug_root)
    else: 
        try:
            shutil.copytree(baseline, aug_root)
        except:
            pass
    images = sorted(glob.glob(os.path.join(baseline)+"/*.tiff")) # use sorted to align images temporally back-forwards
    print(f"Total # images before augmentation: ", len(images))

    for path in images:
        image_name = os.path.join(path.split("/")[-2:][0], path.split("/")[-2:][1])
        img = util.read_tiff(path, config.image_size, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
        if np.sum(img)<threshold:
            # if image content is lower than threshold, replace with the "best" image
            img = util.find_closest_temporal_neighbor(path, images, threshold, resize_ratio= resize_ratio, resizing = resizing, normalize=normalize, printing=printing)
            assert np.sum(img)>=threshold, "img is above threshold"
            aug_path = os.path.join(aug_root, path.split("/")[-2:][1])
            print(f"[{count}] Storing augmented image version of {image_name} in: {aug_path}")
            print(img.shape)
            
            if exists(aug_path):
                os.remove(aug_path)
                io.imsave(aug_path, img)
            else: 
                io.imsave(aug_path, img)
            #display =False
            #
            
            plt.figure(figsize=(9, 3))
            print(img[:,:,1:4].shape)
            plt.imshow(img[:,:,1:4])
            
        else:
            print(f"[{count}] - Image {path} remains unchanged..")
        count+=1
        #if count==5:
        #    break
    images = sorted(glob.glob(os.path.join(aug_root)+"/*.tiff")) # use sorted to align images temporally back-forwards
    print(f"Total # images: ", len(images))