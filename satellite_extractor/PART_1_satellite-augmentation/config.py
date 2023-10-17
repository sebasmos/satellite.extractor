import os
root = "/home/sebasmos/Desktop/DATASETS/"
code = 23001
#baseline = os.path.join(root, "DATASET_improved_10_cities", str(code))
#baseline = "/home/sebasmos/Desktop/DATASETS/DATASET_5_best_cities/Cúcuta"
DATASET = "/home/sebasmos/Desktop/DATASETS/DATASET_improved_10_cities"
#aug_root =  os.path.join(root, "DATASET_augmented",  str(code))
aug_root = os.path.join(root, "DATASET_augmented")
threshold = 100 
image_size= 750
resize_ratio=(1, 1, 1)
resizing = False
normalize = True
printing = False
visualization = "data"
SAVE=True