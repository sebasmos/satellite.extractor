'''
Author: Sebastian Cajas

Find coordinates with bboxfinder.com 

'''

from sentinelhub import SHConfig
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'..') # https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder 
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
    
# bboxfinder.com/#6.192609,-75.607738,6.301649,-75.538731 
#   -75.60946,   6.191755,   -75.554535,   6.283562
betsiboka_coords_wgs84 =  [-75.60946,   6.191755,   -75.554535,   6.283562]

CLIENT_ID = "5a0eee73-51af-4cee-b314-7169ce5798e5"
CLIENT_SECRET = "h@{#0;:P^Ol(xk04G#@Q%29r>?k2rrZ>IKg}4h:?"

config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret=CLIENT_SECRET

if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")
    
resolution = 60
betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

print(f'Image shape at {resolution} m resolution: {betsiboka_size} pixels')

# https://docs.sentinel-hub.com/api/latest/user-guides/cloud-masks/#cloud-masks-and-cloud-probabilities 
'''
Cloud masks and probabilites computed using s2cloudless are available at a fixed resolution of 160m per pixel. Sentinel Hub implements the 10-band version. These are meant as convenience bands with the purpose of speeding up processing. Cloud masks are generated in a very slightly different way than the implementation above but for most applications this should not matter.
'''
evalscript_clm = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04", "CLM"],
    output: { bands: 3 }
  }
}

function evaluatePixel(sample) {
  if (sample.CLM == 1) {
    return [0.75 + sample.B04, sample.B03, sample.B02]
  } 
  return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
}
"""

request_true_color = SentinelHubRequest(
    evalscript=evalscript_clm,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=('2020-06-12', '2020-06-13'),
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config
)

data_with_cloud_mask = request_true_color.get_data()
plot_image(data_with_cloud_mask[0], factor=1/255)


evalscript_true_color = """
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


request_true_color = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=('2020-06-01', '2020-06-30'),
            mosaicking_order='leastCC'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config
)

plot_image(request_true_color.get_data()[0], factor=3.5/255, clip_range=(0,1))

evalscript_all_bands = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B01","B02","B03","B04","B05","B06","B07","B08"],
                units: "DN"
            }],
            output: {
                bands: 13,
                sampleType: "INT16"
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B01, 
                sample.B02, 
                sample.B03, 
                sample.B04, 
                sample.B05, 
                sample.B06, 
                sample.B07, 
                sample.B08, 
                sample.B8A, 
                sample.B09, 
                sample.B10, 
                sample.B11, 
                sample.B12];
    }
"""

request_all_bands = SentinelHubRequest(
    evalscript=evalscript_all_bands,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=('2020-06-01', '2020-06-30'),
            mosaicking_order='leastCC'
    )],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF)
    ],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config
)

all_bands_response = request_all_bands.get_data()
plot_image(all_bands_response[0][:, :, 7], factor=3.5/1e4, vmax=1)
plot_image(all_bands_response[0][:, :, [2,3,7]], factor=3.5/1e4, clip_range=(0,1))


