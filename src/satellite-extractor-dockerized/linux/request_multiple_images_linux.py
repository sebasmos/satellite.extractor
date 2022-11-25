# -*- coding: utf-8 -*-

'''
Author: Sebastian Cajas

We recommend to use eo-learn for more complex cases where you need multiple timestamps or high-resolution data for larger areas.
https://github.com/sentinel-hub/eo-learn

!pip install epiweeks


'''

from sentinelhub import SHConfig
import os
#import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import timedelta
sys.path.insert(0,'..') 
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest
#from rename_linux import *
from epiweeks import Week, Year
from datetime import date
import glob, shutil

def cleaners(dataset, root_images):
    for root, dirs, files in os.walk(dataset, topdown=True):
        for name in files:
             path = os.path.join(root, name)
             if ".tiff" in path:
                    os.remove(path)
    return print("Ready")

def get_epi_weeks(start):
    
    tdelta =  timedelta(days = 7)
    
    edges = [(start + i*tdelta) for i in range(2)]
    
    return [(edges[i], edges[i+1]) for i in range(len(edges)-1)]
    

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

def download_multiple_images(coordinates, start, year, CLIENT_ID, CLIENT_SECRET):

    # put here your credentials
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET

    config = SHConfig()

    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret=CLIENT_SECRET
    
    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    resolution = 10
    bbox = BBox(bbox=coordinates, crs=CRS.WGS84)
    bbox_size = bbox_to_dimensions(bbox, resolution=resolution)

    #print(f'Image shape at {resolution} m resolution: {bbox_size} pixels')

    slots = get_epi_weeks(start)
    
    # Visualization purposes
    d_init = slots[0][0].strftime('%m/%d/%Y')
    d_end  = slots[0][1].strftime('%m/%d/%Y')
    print(f"Requested week slot: {d_init} - {d_end} ")


    script_Medellin = """

        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10", "B11", "B12"], 
                }],
                output: {
                    bands: 12
                }
            };
        }
        function evaluatePixel(sample) {
            return [sample.B01, 
                    sample.B04,
                    sample.B03,
                    sample.B02,
                    sample.B05, 
                    sample.B06, 
                    sample.B07, 
                    sample.B08, 
                    sample.B09, 
                    sample.B10, 
                    sample.B11,
                    sample.B12];
        }
    """
    

    '''Check if directory exists, if not, create it'''
    
    # You should change 'test' to your preferred folder.
    # If folder doesn't exist, then create it.
    
    # if windows: 
    path = os.path.abspath(os.getcwd()) + "//data"  + "//" + year
    # if linux: path = os.path.abspath(os.getcwd()) + "/data"  + "/" year
    
    if not os.path.isdir(path):
        os.makedirs(path)
        #print("created folder : ", path)
    else:
        #print(path, "Folder already exists. Rewriting*")
        pass
    
    def get_true_color_request(time_interval):
        return SentinelHubRequest(
            data_folder= 'data' + "/" + year,
            evalscript=script_Medellin,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    #time_interval=('2015-11-1', '2015-11-20'), #time_interval,
                    time_interval=time_interval,
                    mosaicking_order='leastCC'
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.TIFF)
            ],
            bbox=bbox,
            size=bbox_size,
            config=config
        )

    # create a list of requests
    list_of_requests = [get_true_color_request(slot) for slot in slots]
    list_of_requests = [request.download_list[0] for request in list_of_requests]

    image = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)
    print("Ended downloading")
    
    # Verify if images are empty, if not, correct
    img = np.array(image)
    if img.sum() == 0: # or img.sum()>=threshold # threshold=70 
        print("Image empty: ", img.sum())
        # Initialize  
        end = slots[0][1]
        # Add delay by 1 day step
        while img.sum() == 0: # tune
            tdelta =  timedelta(days = 1)
            init =  slots[0][0]
            end = end + tdelta
            corrected_slot =  [(init, end)]
            #print("Slot corrected to: ", corrected_slot)
            list_of_requests = [get_true_color_request(slot) for slot in corrected_slot]
            list_of_requests = [request.download_list[0] for request in list_of_requests]
            image = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)
            img = np.array(image)
            print("This image is being replaced..")
        print("Slot corrected to: ", corrected_slot)
    else:
        pass

    '''
    # Remove extra dimension
    img = np.squeeze(image, axis = 0)
   
    ncols = 4
    nrows = 3

    aspect_ratio = bbox_size[0] / bbox_size[1]
    subplot_kw = {'xticks': [], 'yticks': [], 'frame_on': False}

    plot_image(img[:,:,1], factor=1.0, cmap=plt.cm.Greys_r, vmin=0, vmax=120)
    '''
    return img

def get_folder_ID(root_images, img_format):
    
    walker = "." + root_images
            
    for root, dirs, files in os.walk(walker, topdown=True):
        for name in files:
            path = os.path.join(root, name)
            if "response" in path:
                        
                folder_path = path.replace("/" + "response." + img_format, "")

    return folder_path
