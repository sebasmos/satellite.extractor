# -*- coding: utf-8 -*-

import shutil, os

from sentinelhub import SHConfig
import os
import json
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

from satellite_extractor.algorithms import download_multiple_images_16_bit_forward_backward,download_image, download_multiple_images, get_request_individual, get_folder_ID_optimized

import random
print("SentinelHub imports - passed")

def clean_blank_folders(year, img_format):
    path_to_blank_ids = f"./data/{year}/*/*response.{img_format}"
    ids = glob.glob(path_to_blank_ids)
    for idx in ids:
        folder_p = os.path.dirname(idx)
        shutil.rmtree(folder_p)

def get_images(coordinates, city_str, current_coor, years, weeks, img_format, root_images, CLIENT_ID, CLIENT_SECRET):
    folder_path = ""
    for year in years:
        print(f"Year: {year}")
        weeks_range = weeks if year != 2015 else range(44, 53)
        
        for week in weeks_range:
            print(f"Week: {week}")
            start = Week(year, week).startdate()
            download_multiple_images(current_coor, start, str(year), CLIENT_ID, CLIENT_SECRET)
            # download_image(current_coor, start, str(year), CLIENT_ID, CLIENT_SECRET)
            folder_path = get_folder_ID_optimized(root_images)
            # Rename image based on JSON timestamp filter
            dates = get_request_individual(os.path.join(folder_path, "request.json"), city_str)
            clean_blank_folders(year, img_format)

def run(TIMESTAPS, CLIENT_ID, CLIENT_SECRET, IMAGE_FORMAT, COORDINATES_PATH):
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    
    img_format = IMAGE_FORMAT
    initial_year, end_year = TIMESTAPS
    years = list(range(initial_year, end_year + 1))
    
    first_2015_week = 44
    weeks_2015 = list(range(first_2015_week, 53))
    weeks = list(range(1,53))
    
    path_csv = COORDINATES_PATH
    df = pd.read_csv(path_csv)
    root_images = "./data"
    
    if not os.path.isdir(root_images):
        os.makedirs(root_images)
        print(f"Creating data folder in {root_images}")

    for i, row in df.iterrows():
        city_code = row['municipalities']
        city_str = os.path.abspath(f"DATASET/{row['municipalities']}")
        
        if not os.path.exists(city_str):
            os.makedirs(city_str)
            
        print(f"City: {row['municipalities']} - Coordinates: {row['coordinates']}")
        
        current_coor = [float(value) for value in row['coordinates'][1:-1].split(', ')]
        get_images(coordinates=row, city_str=city_code, current_coor=current_coor,
                   years=years, weeks=weeks, img_format=img_format,
                   root_images=root_images, CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET)

        # Move to structured folder in DATASETS
        root_images_store = "./data"
        dataset_store =  f"{city_str}"
        for root, dirs, files in os.walk(root_images_store, topdown=True):
            for name in files:
                path = os.path.join(root, name)
                if img_format in path and dataset_store not in path:
                #     shutil.copy(path, dataset_store)
                    file_city_code = name.split("_")[0]
                    # If the extracted city code matches the current city_str, copy the file
                    # import pdb;pdb.set_trace()
                    if int(file_city_code) == int(city_code):
                        shutil.copy(path, dataset_store)
                        print(path, dataset_store)

    images = glob.glob(f"{dataset_store}/*")
    print(images)
    print("Done")

# import pandas as pd
# import glob
# import json
# import datetime as dt
# from urllib.parse import unquote
# import os
# import shutil
# from sentinelhub import SHConfig
# import datetime
# import numpy as np
# import matplotlib.pyplot as plt
# import sys
# from datetime import timedelta
# sys.path.insert(0,'..') 
# from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest
# # !pip install epiweeks
# from epiweeks import Week, Year
# from datetime import date
# import glob, shutil
# import sys
# sys.path.insert(0,'../') 
# from satellite_extractor.algorithms import download_multiple_images_16_bit_forward_backward, get_folder_ID,download_image
# import argparse
# import pandas as pd
# cred = pd.read_csv("/Users/sebasmos/Desktop/satellite.extractor/satellite_extractor/satellite-extractor-dockerized/data_config/SentinelHub-credentials.csv")
# CLIENT_ID = str(cred.iloc[0,:][0])
# CLIENT_SECRET = str(cred.iloc[1,:][0])
# LATITUDE = 3.4400
# LONGITUDE= -76.5197
# TIMESTAPS = [2016,2016]
# # projection = CRS.WGS84
# IMAGE_FORMAT = "tiff"
# CODE = 5555
# LENGTH = 750
# RESOLUTION = 10
# COORDINATES_PATH = "/Users/sebasmos/Desktop/satellite.extractor/data/10_municipalities_full.csv"
# service_account = 'ee-account@mit-hst-dengue.iam.gserviceaccount.com'
# run(TIMESTAPS, CLIENT_ID, CLIENT_SECRET, IMAGE_FORMAT, COORDINATES_PATH )