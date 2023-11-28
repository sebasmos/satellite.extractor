import glob
import os
import matplotlib.pyplot as plt
from skimage import io, exposure
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import random
import tifffile
import sys
import satellite_extractor.utils as utils
from torch.utils.data import Dataset

def plot_image_pairs_to_pdf(output_data, pdf_filename="image_pairs.pdf", num_pairs=10):
    cloudless_files = glob.glob(os.path.join(output_data, 'cloudless_*.tiff'))
    cloudy_files = glob.glob(os.path.join(output_data, 'cloudy_*.tiff'))

    # Check if both cloudless and cloudy images exist
    if not cloudless_files or not cloudy_files:
        print(f"Insufficient images found in '{output_data}'.")
        return

    # Ensure the number of pairs is not more than the available images
    num_images = min(len(cloudless_files), len(cloudy_files))
    if num_images < num_pairs:
        print(f"Insufficient images found in '{output_data}'.")
        return

    # Sort the file lists to ensure matching by name
    cloudless_files.sort()
    cloudy_files.sort()

    selected_indices = np.random.choice(num_images, num_pairs, replace=False)

    with PdfPages(pdf_filename) as pdf:
        fig, axes = plt.subplots(num_pairs, 2, figsize=(15, 5 * num_pairs))

        for j, idx in enumerate(selected_indices):
            cloudless_image_path = cloudless_files[idx]
            cloudy_image_path = cloudy_files[idx]

            cloudless_image = utils.read_tiff(cloudless_image_path)[:, :, 1:4]
            cloudy_image = utils.read_tiff(cloudy_image_path)[:, :, 1:4]

            axes[j, 0].imshow(cloudless_image)
            axes[j, 0].set_title(f"Cloudless\n{os.path.basename(cloudless_image_path)}", fontsize=12)
            axes[j, 0].axis('off')

            axes[j, 1].imshow(cloudy_image)
            axes[j, 1].set_title(f"Cloudy\n{os.path.basename(cloudy_image_path)}", fontsize=12)
            axes[j, 1].axis('off')

        plt.subplots_adjust(wspace=0.1)  # Adjust the horizontal space between subplots
        plt.show()
        pdf.savefig(fig)
        plt.close(fig)

        print(f"Processed images in '{output_data}' with {num_images} images.")

