import config
import os
import matplotlib.pyplot as plt
import numpy as np
import utils as utils
import pandas as pd
import concurrent.futures
import datetime
from skimage import io
from skimage.transform import rescale, resize
from skimage.exposure import equalize_adapthist
import time
import datetime
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
viz = os.path.join(ROOT_DIR, config.visualization)
os.makedirs(viz, exist_ok=True)

def process_image(img_path):
    path = os.path.join(root, city, img_path)
    img = utils.read_tiff(path, config.image_size, resize_ratio=config.resize_ratio,
                          resizing=config.resizing, normalize=config.normalize, printing=config.printing)
    imageHash = utils.hash_difference(img)
    return imageHash

if __name__ == "__main__":
    a = 0
    root = config.DATASET
    pdf_filename = "output.pdf"


    for city in os.listdir(root):
        start_time = time.time()
        images_path = os.path.join(root, city)
        print(f'{city} : {len(os.listdir(images_path))} images '.center(60, "-"))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            list_hashes = list(executor.map(process_image, os.listdir(images_path)))

        total_time = time.time() - start_time
        total_time_str = str(datetime.timedelta(seconds=int(total_time)))
        print(f'Training time for {city} : {total_time_str}')
        m = np.array(list_hashes)
        print(m.shape)
        
        data = {"img_hash": m, "img_names": os.listdir(images_path)}
        df = pd.DataFrame(data=data)
        num_img_per_hash = df.groupby("img_hash").size().sort_values(ascending=False).reset_index(name="img_names")
        print(num_img_per_hash)

        ax = plt.figure()
        num_img_per_hash.hist("img_names", bins=20, orientation="horizontal", color='#86bf91')
        plt.xlabel("Number of Encrypted images")
        plt.ylabel("Relative Frequency")
        plt.title(f'{city}')
        plt.ylim(1, num_img_per_hash.img_names[0])
        plt.grid(False)
        yint = []
        locs, labels = plt.yticks()
        for each in locs:
            yint.append(int(each))
        plt.yticks(yint)
        plt.close()

