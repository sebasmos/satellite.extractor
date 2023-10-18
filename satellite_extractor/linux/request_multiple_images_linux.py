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

def get_true_color_request(path, script, time_interval, bbox, bbox_size, config):
  return SentinelHubRequest(
      data_folder= path,
      evalscript=script,
      input_data=[
          SentinelHubRequest.input_data(
              data_collection=DataCollection.SENTINEL2_L2A,
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

def download_image(coordinates, start, year, CLIENT_ID, CLIENT_SECRET):
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

  #All S2L2A raw bands, original data (no harmonization)
  script = """
      //VERSION=3
      function setup() {
        return {
          input: [{
            bands: ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"],
            units: "DN"
          }],
          output: {
            id: "default",
            bands: 12,
            sampleType: SampleType.UINT16
          }
        }
      }

      function evaluatePixel(sample) {
          return [ sample.B01, sample.B02, sample.B03, sample.B04, sample.B05, sample.B06, sample.B07, sample.B08, sample.B8A, sample.B09, sample.B11, sample.B12]
      }
  """
  temporal_path = "data" + "/" + str(year)
  request = get_true_color_request(temporal_path, script, slots[0], bbox, bbox_size, config)
  request = request.download_list[0]

  image = SentinelHubDownloadClient(config=config).download(request, max_threads=5)
  img = np.array(image)
  return img


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


    #All S2L2A raw bands, original data (no harmonization)
    script_Medellin = """
        //VERSION=3
        function setup() {
          return {
            input: [{
              bands: ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"],
              units: "DN"
            }],
            output: {
              id: "default",
              bands: 12,
              sampleType: SampleType.UINT16
            }
          }
        }

        function evaluatePixel(sample) {
            return [ sample.B01, sample.B02, sample.B03, sample.B04, sample.B05, sample.B06, sample.B07, sample.B08, sample.B8A, sample.B09, sample.B11, sample.B12]
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
                    #data_collection=DataCollection.SENTINEL2_L1C,
                    data_collection=DataCollection.SENTINEL2_L2A,
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
    #print("Ended downloading")

    # Verify if images are empty, if not, correct
    img = np.array(image)
      
    #print("Shape:",img.shape)
    #print("Sum:",img.sum())
    #print("Max value:",img.max())

    #tolerance = 1e2
    tolerance = 0
    close_to_zero_mask = np.abs(img) == tolerance
    close_to_zero_count = np.count_nonzero(close_to_zero_mask)
    print(f"Number of values close to zero: {close_to_zero_count}")
    print(f"% of zeros: {(close_to_zero_count/img.size)*100}")

    # Verify if images are empty, if not, correct
    if img.sum() == 0:
        # Initialize  
        init = slots[0][0]
        end = slots[0][1]

        upward = 0
        backward = 0

        img_up = np.array(image)
        img_down = np.array(image)

        # Limit the number of day the function can go both forward and backward to 30 days
        # It can just to check 30 days before and after the current date to see if there's a better picture

        while np.sum(img_up) == 0 and upward < 30:
          upward+=1
          tdelta =  timedelta(days = 1)
          end = end + tdelta
          corrected_slot =  [(init, end)]

          list_of_requests = [get_true_color_request(slot) for slot in corrected_slot]
          list_of_requests = [request.download_list[0] for request in list_of_requests]
          image = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)
          img_up = np.array(image)

          print("Slot corrected (up) to: ", corrected_slot)

        print(f"img_up: {np.sum(img_up)}")
        end = slots[0][1]

        while np.sum(img_down) == 0 and backward < 30:
          # if index starts off from 0, bound limits
          tdelta =  timedelta(days = 1)
          init = init - tdelta
          corrected_slot =  [(init, end)]

          backward+=1

          list_of_requests = [get_true_color_request(slot) for slot in corrected_slot]
          list_of_requests = [request.download_list[0] for request in list_of_requests]
          image = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)
          img_down = np.array(image)

          print("Slot corrected (down) to: ", corrected_slot)

        print(f"img_down: {np.sum(img_down)}")

        if upward<backward :
          assert np.sum(img_up) > 0, "image is empty"
          print(f"-->[FORWARD] - image will be replaced with img_up - Temporal distance = [Forward = {upward}, backward = {backward}]")
          img = img_up

        elif upward>backward:
          assert np.sum(img_down) > 0, "image is empty"
          print(f"-->[BACKWARDS] - image down will be replaced with img_down - Temporal distance = [Forward = {upward}, backward = {backward}]")
          img = img_down

        elif upward==backward:
          final_img = img_up if random.choice(["t1","t2"]) == "t1" else img_down
          print(f"-->[EQUIDISTANT] - image random will be replaced with final_img - Temporal distance = [Forward = {upward} = backward = {backward}]")
          img = final_img

        # Add delay by 1 day step
        # while img.sum() == 0: # tune
        #     tdelta =  timedelta(days = 1)
        #     init =  slots[0][0]
        #     end = end + tdelta
        #     corrected_slot =  [(init, end)]
        #     #print("Slot corrected to: ", corrected_slot)
        #     list_of_requests = [get_true_color_request(slot) for slot in corrected_slot]
                
        #     list_of_requests = [request.download_list[0] for request in list_of_requests]
        #     image = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)
        #     img = np.array(image)
        #     print("This image is being replaced..")
        print("Slot corrected to: ", corrected_slot)
        print("Shape:",img.shape)
        print("Sum:",img.sum())
        print("Max value:",img.max())

        close_to_zero_mask = np.abs(img) <= tolerance
        close_to_zero_count = np.count_nonzero(close_to_zero_mask)
        print(f"Number of values close to zero: {close_to_zero_count}")
        print(f"% of zeros: {close_to_zero_count/img.size}")    
        
    else:
        print(f"Pixel values: ", np.unique(img))
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
