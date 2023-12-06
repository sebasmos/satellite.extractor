# -*- coding: utf-8 -*-

import shutil, os

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
sys.path.insert(0,'Dengue/') 

from satellite_extractor.algorithms import download_multiple_images_16_bit_forward_backward,download_image, get_folder_ID#, get_request_individual

import random
print("SentinelHub imports - passed")

def get_request_individual(request_file, img_format):
    with open(request_file, 'r') as req:
        json_decode = json.load(req)
        
        dataFilter = json_decode["request"]["payload"]["input"]["data"][0]
        timeRanges = dataFilter["dataFilter"]["timeRange"]
        start = timeRanges["from"].split("T")[0]
        end = timeRanges["to"].split("T")[0]
        time_stamp = start + "_to_" + end # best image calculated on this interval
        name_image = "image_" +   start
        print(name_image)
        data = {
            "start": start,
            "end": end,
            "time_stamp": time_stamp,
            "url": request_file,
            }
            
        df = pd.DataFrame(data, index =['date'])
        
        # Update name of files using JSON timestamp filter
        response_img = request_file.split("request.json")[0] + "response.tiff"# + "."+ img_format
        image_path = os.path.join(response_img).replace('response', name_image )        
        print("{0} renamed to {1}".format(response_img, image_path))
        shutil.move(response_img, image_path)
        
        return df 
    
    
def get_images(dic,city_str, coordenates, years, weeks, weeks_2015, img_format, root_images, CLIENT_ID, CLIENT_SECRET):
    # Download data
    folder_path = ""
    for year in years:
        if year == 2015:
            for week in weeks_2015:
                print(f"Year: {year} - week: {week}")
                # Set starting date for given year based on 
                start = Week(year, week).startdate()
                # Download individual images
                download_image(coordenates, start, str(year), CLIENT_ID, CLIENT_SECRET)
                # Obtain ID as the last-obtained response.tiff file, "real-time"
                # folder_path = get_folder_ID(root_images, img_format)
                
                folder_path = os.path.join(root_images, get_folder_ID(root_images, img_format))
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
                
                        
        else:
            for week in weeks:
                print(f"Year: {year} - week: {week}")
                # Set starting date for given year based on 
                start = Week(year, week).startdate()
                # Download individual images
                download_image(coordenates, start, str(year), CLIENT_ID, CLIENT_SECRET)
                # Obtain ID as the last-obtained response.tiff file, "real-time"
                folder_path = get_folder_ID(root_images, img_format)
                import pdb;pdb.set_trace()
                folder_path = os.path.join(root_images, get_folder_ID(root_images, img_format))
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


def run(TIMESTAPS, CLIENT_ID, CLIENT_SECRET, IMAGE_FORMAT, COORDINATES_PATH):
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    print("Installing SentinelHub")
    # CONFIGURATION 
    img_format = IMAGE_FORMAT
    initial_year = TIMESTAPS[0]
    end_year = TIMESTAPS[1]
    print(initial_year,end_year)
    years = list(range(initial_year,end_year+1))# +1 to consider 2018
    first_2015_week = 44
    start_2015 = Week(initial_year,first_2015_week).startdate()
    weeks_2015 = list(range(first_2015_week, 53))
    weeks = list(range(1,53))
    # path to municipalities
    path_csv = COORDINATES_PATH
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
        get_images(new_coord, city_str, current_coor, years, weeks, weeks_2015, img_format, root_images, CLIENT_ID, CLIENT_SECRET)

    # Move to structured folder in DATASETS
        root_images_store = "." + root_images
        dataset_store = "./" + city_str
        for root, dirs, files in os.walk(root_images_store, topdown=True):
            for name in files:
                path = os.path.join(root, name)
                #print(path)
                if img_format in path and not dataset_stsore in path:
                    shutil.copy(path, dataset_store)
                    
    images = glob.glob(dataset_store+"/*")

    print(images)
    print("Done")

    #shutil.rmtree("data")   
    #shutil.rmtree("DATASET")
import pandas as pd
import glob
import json
import datetime as dt
from urllib.parse import unquote
import os
import shutil
from sentinelhub import SHConfig
import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import timedelta
sys.path.insert(0,'..') 
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest
# !pip install epiweeks
from epiweeks import Week, Year
from datetime import date
import glob, shutil
from epiweeks import Week, Year
import sys
sys.path.insert(0,'../') 
from satellite_extractor.algorithms import download_multiple_images_16_bit_forward_backward, get_folder_ID,download_image
import argparse
import satellite_extractor.extractor_original as sat
import pandas as pd
cred = pd.read_csv("/Users/sebasmos/Desktop/satellite.extractor/satellite_extractor/satellite-extractor-dockerized/data_config/SentinelHub-credentials.csv")
CLIENT_ID = str(cred.iloc[0,:][0])
CLIENT_SECRET = str(cred.iloc[1,:][0])
LATITUDE = 3.4400
LONGITUDE= -76.5197
TIMESTAPS = [2016,2018]
# projection = CRS.WGS84
IMAGE_FORMAT = "tiff"
CODE = 5555
LENGTH = 750
RESOLUTION = 10
COORDINATES_PATH = "/Users/sebasmos/Desktop/satellite.extractor/data/10_municipalities_full.csv"
service_account = 'ee-account@mit-hst-dengue.iam.gserviceaccount.com'
sat.run(TIMESTAPS, CLIENT_ID, CLIENT_SECRET, IMAGE_FORMAT, COORDINATES_PATH )