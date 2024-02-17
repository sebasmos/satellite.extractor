import os
#baseline = os.path.join(root, "DATASET_improved_10_cities", str(code))
#baseline = "/home/sebasmos/Desktop/DATASETS/DATASET_5_best_cities/Cúcuta"
DATASET = "/media/enc/vera1/sebastian/codes/satellite.extractor/notebooks/DATASET_rio_de_janeiro"
#aug_root =  os.path.join(root, "DATASET_augmented",  str(code))
# Where you want to save your dataset:
DESTINATION_FOLDER = "DATASET_rio_de_janeiro_fordward_backwardv2"
threshold = 100 
image_size= 750
resize_ratio=(1, 1, 1)
resizing = False
normalize = True
printing = False
visualization = "data"
SAVE=True