# -*- coding: utf-8 -*-

'''
Author: Sebastian Cajas

We recommend to use eo-learn for more complex cases where you need multiple timestamps or high-resolution data for larger areas.
https://github.com/sentinel-hub/eo-learn

!pip install epiweeks


'''

from sentinelhub import SHConfig
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import timedelta
sys.path.insert(0,'..') 
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest
from rename import get_request_dt
from epiweeks import Week, Year
from datetime import date
import glob, shutil

def get_epi_weeks(start):
    
    n_chunks = 53

    tdelta =  timedelta(days = 7)
    
    edges = [(start + i*tdelta) for i in range(n_chunks)]
    
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

def download_multiple_images(coordinates, start, year):
    # put here your credentials
    CLIENT_ID = "****"
    CLIENT_SECRET = "***"

    config = SHConfig()

    if CLIENT_ID and CLIENT_SECRET:
        config.sh_client_id = CLIENT_ID
        config.sh_client_secret=CLIENT_SECRET
    
    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    resolution = 10
    bbox = BBox(bbox=coordinates, crs=CRS.WGS84)
    bbox_size = bbox_to_dimensions(bbox, resolution=resolution)

    print(f'Image shape at {resolution} m resolution: {bbox_size} pixels')

    slots = get_epi_weeks(start)

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
    
    evalscript_rgb ="""
    //VERSION=3
    
    function setup() {
      return {
        input: ["B02", "B03", "B04"],
        output: { bands: 3 }
      };
    }
    
    function evaluatePixel(sample) {
      return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
    }
    """
    '''Check if directory exists, if not, create it'''
    
    # You should change 'test' to your preferred folder.
    # If folder doesn't exist, then create it.
    
    # if windows: 
    path = os.path.abspath(os.getcwd()) + "\\data"  + "\\" + year
    # if linux: path = os.path.abspath(os.getcwd()) + "/data"  + "/" year
    
    if not os.path.isdir(path):
        os.makedirs(path)
        print("created folder : ", path)
    else:
        print(path, "Folder already exists. Rewriting*")
        pass
    
    def get_true_color_request(time_interval):
        return SentinelHubRequest(
            data_folder= 'data' + "/" + year,
            evalscript=evalscript_rgb,
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
            bbox=bbox,
            size=bbox_size,
            config=config
        )

    # create a list of requests
    list_of_requests = [get_true_color_request(slot) for slot in slots]
    list_of_requests = [request.download_list[0] for request in list_of_requests]

    
    # download data with multiple threads

    SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)
    print("Ended downloading")
    
    '''
    ncols = 4
    nrows = 3

    aspect_ratio = bbox_size[0] / bbox_size[1]
    subplot_kw = {'xticks': [], 'yticks': [], 'frame_on': False}

    plot_image(data[3][:,:,:1], factor=1.0, cmap=plt.cm.Greys_r, vmin=0, vmax=120)
    '''

coordenates =  [-75.607738,6.192609, -75.538731,6.301649]
# Customized for SENTINEL2_L1C 
root_images = "\\data\\"
dataset = "\\DATASET\\"

path = os.path.abspath(os.getcwd()) + root_images  
dataset_path = os.path.abspath(os.getcwd()) + dataset  
    
if not os.path.isdir(path):
    os.makedirs(path)
    print("Creating temporal data folder")
if not os.path.isdir(dataset_path):
    os.makedirs(dataset_path)
    print("Creating /DATASET")
else:
    print("Re-writing in temporal data folder")
    pass
img_format = "tiff"
# Define the range of years
initial_year = 2015
end_year = 2016
years = [initial_year, end_year]
first_2015_week = 44
end_year = 2020

start_2015 = Week(initial_year,first_2015_week).startdate()

weeks_2015 = list(range(first_2015_week, 53))
weeks = list(range(1,53))

# Download data
for year in years:
    if year == 2015:
        for week in weeks_2015:
            # Set starting date for given year based on 
            start = Week(year, week).startdate()
            download_multiple_images(coordenates, start, str(year))
            folders = glob.glob("." + root_images + str(year) + '\\*')
            # Rename image based on JSON timestamp filter 
            dates = [get_request_dt(f'{folder}\\request.json', img_format) for folder in folders]

# Move to structured folder in DATASETS
root_images = "." + root_images
dataset = "." + dataset
for root, dirs, files in os.walk(root_images, topdown=True):
    for name in files:
        path = os.path.join(root, name)
        print(path)
        if img_format in path and not dataset in path:
            shutil.copy(path, dataset)
            
            
images = glob.glob("./" + dataset + "/*")


'''
def cleaners(dataset, root_images):
    for root, dirs, files in os.walk(dataset, topdown=True):
        for name in files:
             path = os.path.join(root, name)
                #print(path)
             if ".tiff" in path:
                    os.remove(path)
                    
    
    return print("Ready")

shutil.rmtree("dataset")
shutil.rmtree("data")
cleaners(dataset, root_images)
'''