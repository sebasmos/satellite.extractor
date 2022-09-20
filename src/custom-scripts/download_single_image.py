'''
Author: Sebastian Cajas

Find coordinates with bboxfinder.com 

'''

from sentinelhub import SHConfig
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import shutil
import sys
sys.path.insert(0,'../') # https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder 

from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest

def plot_image(image, factor=1.0, clip_range = None, **kwargs):
    """
    Utility function for plotting RGB images.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])
    

def main(CLIENT_ID, CLIENT_SECRET, coordinates):
      
    config = SHConfig()
    
    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret=CLIENT_SECRET
    
    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")
        
    resolution = 10
    
    coordinates_bbox = BBox(bbox=coordinates, crs=CRS.WGS84)
    
    coordinates_size = bbox_to_dimensions(coordinates_bbox, resolution=resolution)
    
    print(f'Image shape at {resolution} m resolution: {coordinates_size} pixels')
    
    
    evalscript_true_color = """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B01","B02", "B03", "B04", "B05", "B06","B07", "B08", "B09", "B10", "B11", "B12"]
                }],
                output: {
                    bands: 12
                }
            };
        }
    
        function evaluatePixel(sample) {
            return [sample.B12, sample.B11, sample.B10, sample.B09, sample.B08, sample.B07, sample.B06,sample.B05,sample.B04, sample.B03, sample.B02];
        }
    """
    evalscript_rbg_color = """
        //VERSION=3
    
        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }
        
        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """
    
    request_all_bands = SentinelHubRequest(
        data_folder='data/data_medellin',
        evalscript=evalscript_rbg_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=('2016-01-1', '2016-03-1'),
                mosaicking_order='leastCC'
        )],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=coordinates_bbox,
        size=coordinates_size,
        config=config
    )
    all_bands_response = request_all_bands.get_data(save_data=True)
    image = request_all_bands.get_data()[0]
    #image = image[:512,:512]
    print(f"Image shape: {image.shape}")
    print(f"Image pixel values: {len(np.unique(image))}")
    plot_image(image, factor=1/255, clip_range=(0,1))
    
    all_bands_response_downloaded = request_all_bands.get_data(redownload=True)
    
    import shutil, glob
    #shutil.rmtree("data")
    
    root_images = "/data"
    
    dataset = "/dataset"
    # Move to structured folder in DATASETS
    root_images_store = "." + root_images
    
    img_format = "png"
    
    dataset_store = "." + dataset
    for root, dirs, files in os.walk(root_images_store, topdown=True):
        for name in files:
            path = os.path.join(root, name)
            print(path)
            if img_format in path and not dataset_store in path:
                shutil.copy(path, dataset_store)
            
    images = glob.glob("./" + dataset + "/*")
    
if __name__ == '__main__':
    
    coordinates = [-76.55323133405957, 3.4062672204498083, -76.4860619546151, 3.473745747318065]
    CLIENT_ID = "****"
    CLIENT_SECRET =  "****"
    main(CLIENT_ID, CLIENT_SECRET, coordinates)
