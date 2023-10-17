import os
root = "media/sebasmos/Expansion/sebastian_data/DATASETS/"
#baseline = "/home/sebasmos/Desktop/DATASETS/DATASET_5_best_cities/Cúcuta"
#DATASET = "/home/sebasmos/Desktop/DATASETS/DATASET_5_best_cities"
DATASET = "/media/sebasmos/Expansion/sebastian_data/DATASETS/DATASETS_huggingface/SAT3_FULL_COLOMBIA/images"
#aug_root =  os.path.join(root, "DATASET_augmented",  str(code))
aug_root = os.path.join(root, "DATASET_augmented_v3_gaussian_blur", "DATASET_augmented_v3_gaussian_blur")
threshold = 5
image_size= 750
resize_ratio=(1, 1, 1)
resizing = False
normalize = True
printing = False
visualization = "data"
SAVE=True