import utils as util
import matplotlib.pyplot as plt
test = "/home/sebasmos/Desktop/DATASETS/DATASET_augmented/41001/image_2015-11-01.tiff"
img = util.read_tiff(test, 750)
print(img.shape)
plt.figure(figsize=(6, 6))
plt.imshow(img)
plt.show()