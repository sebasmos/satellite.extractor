'''
Author: Sebastian Cajas

Find coordinates with bboxfinder.com 

We recommend to use eo-learn for more complex cases where you need multiple timestamps or high-resolution data for larger areas.
https://github.com/sentinel-hub/eo-learn

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
    
    '''
    # Fast test 
    start = datetime.datetime(2006,12,31) #2020-06-01', '2020-06-3
    end = datetime.datetime(2018,12,29)
    years = 12
    n_chunks = 48 * years # num semanas/año
    tdelta = (end - start) / n_chunks
    edges = [(start + i*tdelta).date().isoformat() for i in range(n_chunks)]
    slots = [(edges[i], edges[i+1]) for i in range(len(edges)-1)]
    '''
    # REAL TEST: 
    start = datetime.datetime(2015,8,1) #2020-06-01', '2020-06-3
    end = datetime.datetime(2015,12,31)
    years = 1
    days = 30
    n_chunks =  8*4# num semanas/año
    tdelta = (end - start) / n_chunks
    edges = [(start + i*tdelta).date().isoformat() for i in range(n_chunks)]
    slots = [(edges[i], edges[i+1]) for i in range(len(edges)-1)]
    
    print('Weekly time windows:\n')
    for slot in slots:
        print(slot)
    
    evalscript_true_color = """
    
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04", "B05", "B06", "B07", "B08"]
                }],
                output: {
                    bands: 7
                }
            };
        }
        function evaluatePixel(sample) {
            return [sample.B08, 
                    sample.B07, 
                    sample.B06, 
                    sample.B05, 
                    sample.B04, 
                    sample.B03, 
                    sample.B02];
        }
    """
        
    def get_true_color_request(time_interval):
        return SentinelHubRequest(
            data_folder='data/2016',
            evalscript=evalscript_true_color,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    time_interval=time_interval,
                    mosaicking_order='leastCC'
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.TIFF)
            ],
            bbox=coordinates_bbox,
            size=coordinates_size,
            config=config
        )
    
    # create a list of requests
    list_of_requests = [get_true_color_request(slot) for slot in slots]
    list_of_requests = [request.download_list[0] for request in list_of_requests]
    
    # download data with multiple threads
    
    data = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)
    
    ncols = 4
    nrows = 3
    
    aspect_ratio = coordinates_size[0] / coordinates_size[1]
    subplot_kw = {'xticks': [], 'yticks': [], 'frame_on': False}
    
    '''
    fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(5 * ncols * aspect_ratio, 5 * nrows),
                            subplot_kw=subplot_kw)
    
    for idx, image in enumerate(data):
        ax = axs[idx // ncols][idx % ncols]
        ax.imshow(np.clip(image * 2.5/255, 0, 1))
        ax.set_title(f'{slots[idx][0]}  -  {slots[idx][1]}', fontsize=10)
        
    plt.tight_layout()
    '''
    
    plot_image(data[0][:,:,:1], factor=1.0, cmap=plt.cm.Greys_r, vmin=0, vmax=120)

if __name__ == '__main__':
    
    coordinates = [-76.55323133405957, 3.4062672204498083, -76.4860619546151, 3.473745747318065]
    CLIENT_ID = "5a0eee73-51af-4cee-b314-7169ce5798e5"
    CLIENT_SECRET = "h@{#0;:P^Ol(xk04G#@Q%29r>?k2rrZ>IKg}4h:?"
    main(CLIENT_ID, CLIENT_SECRET,coordinates )
