import utils as util
import matplotlib.pyplot as plt
test = "/home/sebasmos/Desktop/satellite.extractor/data/DATASET_augmented_23001_image_2016-01-03.tiff"
img = util.read_tiff(test, 750)
print(img.shape)
plt.figure(figsize=(6, 6))
plt.imshow(img[:,:,[2,3,4]])
plt.show()