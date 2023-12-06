# -*- coding: utf-8 -*-

import shutil, os
import config

from sentinelhub import SHConfig
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import timedelta
sys.path.insert(0,'..') 
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest

from epiweeks import Week, Year
from datetime import date
import glob, shutil
import pandas as pd
import config
sys.path.insert(0,'Dengue/') 
from satellite_extractor.satellite-extractor-dockerized.linux.request_multiple_images_linux import download_multiple_images
from satellite_extractor.satellite-extractor-dockerized.linux.request_multiple_images_linux import get_folder_ID
from satellite_extractor.satellite-extractor-dockerized.linux.rename_linux import get_request_individual

print("SentinelHub imports - passed")

######################################################################################    
def download_multiple_images_16_bit_forward_backward(coordinates, start, year, CLIENT_ID, CLIENT_SECRET):

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

def get_images(dic, coordenates, years, weeks, weeks_2015, img_format, root_images, CLIENT_ID, CLIENT_SECRET):
    # Download data
    folder_path = ""
    for year in years:
        if year == 2015:
            for week in weeks_2015:
                print(f"Year: {year} - week: {week}")
                # Set starting date for given year based on 
                start = Week(year, week).startdate()
                # Download individual images
                download_multiple_images(coordenates, start, str(year), CLIENT_ID, CLIENT_SECRET)
                # Obtain ID as the last-obtained response.tiff file, "real-time"
                folder_path = get_folder_ID(root_images, img_format)
                # Rename image based on JSON timestamp filter 
                dates = get_request_individual(folder_path+"/request.json", img_format)
                # Clean folders which contain black images
                path_to_blank_ids  = "." + root_images + "/" + str(year) + "/*/*" 
                ids = glob.glob(path_to_blank_ids)
                for idx in ids:
                    if "response" in idx:
                        folder_path = idx.replace("/" + "response." + img_format, "")
                        #print(folder_path)
                        shutil.rmtree(folder_path)
                ids = glob.glob(path_to_blank_ids)
                #print("ids available: ", ids)
                        
                #flag =  [idx if ("response" in idx) for idx in ids]
        #elif year ==2016:
        else:
            for week in weeks:
                print(f"Year: {year} - week: {week}")
                # Set starting date for given year based on 
                start = Week(year, week).startdate()
                # Download individual images
                download_multiple_images(coordenates, start, str(year), CLIENT_ID, CLIENT_SECRET)
                # Obtain ID as the last-obtained response.tiff file, "real-time"
                folder_path = get_folder_ID(root_images, img_format)
                # Rename image based on JSON timestamp filter 
                dates = get_request_individual(folder_path+"/request.json", img_format)
                # Clean folders which contain black images
                path_to_blank_ids  = "." + root_images + "/" + str(year) + "/*/*" 
                ids = glob.glob(path_to_blank_ids)
                for idx in ids:
                    if "response" in idx:
                        folder_path = idx.replace("/" + "response." + img_format, "")
                        #print(folder_path)
                        shutil.rmtree(folder_path)
                ids = glob.glob(path_to_blank_ids)


def run(TIMESTAPS, CLIENT_ID, CLIENT_SECRET):
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    print("Installing SentinelHub")
    # CONFIGURATION 
    img_format = config.IMAGE_FORMAT
    initial_year = TIMESTAPS[0]
    end_year = TIMESTAPS[1]
    print(initial_year,end_year)
    years = list(range(initial_year,end_year+1))# +1 to consider 2018
    first_2015_week = 44
    start_2015 = Week(initial_year,first_2015_week).startdate()
    weeks_2015 = list(range(first_2015_week, 53))
    weeks = list(range(1,53))
    # path to municipalities
    path_csv = config.COORDINATES_PATH
    dict_coordinates =  pd.read_csv(path_csv)
    print(f"Considering batch # {len(dict_coordinates)}")
    dict_coordinates = dict(zip(dict_coordinates['Municipality code'], dict_coordinates.square))
    
    coordenadas = []
    municipality = []
    for k, v in dict_coordinates.items():
            municipality.append(k)
            res = [float(value) for value in v[1:-1].split(', ')]
            res = np.array(res)
            coordenadas.append(res)
            
    columns_names = {'municipalities':municipality, 
                    'coordinates': coordenadas}
    df = pd.DataFrame(data=columns_names)
            
    new_coord = dict((columns_names))

    # CREATE TEMPORAL FOLDER
    root_images = "/data/"
       
    temporal_path = os.path.abspath(os.getcwd()) + root_images  
        
    if not os.path.isdir(temporal_path):
        os.makedirs(temporal_path)
        print(f"Creating temporal data folder in {temporal_path}")

    num = len(new_coord["municipalities"])

    # DOWNLOAD DATA

    for i in range(num):  
        print(f"City: {new_coord['municipalities'][i]} - Coordinates: {new_coord['coordinates'][i]}")	    	

        current_coor = list(new_coord["coordinates"][i])
            
        city_str = "DATASET" + "/" + str(new_coord['municipalities'][i])
            
        if not os.path.exists(city_str):
            os.makedirs(city_str)
            
        # Download images on given range
        get_images(new_coord, current_coor, years, weeks, weeks_2015, img_format, root_images, CLIENT_ID, CLIENT_SECRET)

    # Move to structured folder in DATASETS
        root_images_store = "." + root_images
        dataset_store = "./" + city_str
        for root, dirs, files in os.walk(root_images_store, topdown=True):
            for name in files:
                path = os.path.join(root, name)
                #print(path)
                if img_format in path and not dataset_store in path:
                    shutil.copy(path, dataset_store)
                    
    images = glob.glob(dataset_store+"/*")

    print(images)
    print("Done")

    #shutil.rmtree("data")   
    #shutil.rmtree("DATASET")
    
