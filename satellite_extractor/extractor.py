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
from epiweeks import Week, Year
from datetime import date
import glob, shutil
import pandas as pd
sys.path.insert(0,'Dengue/') 

from satellite_extractor.algorithms import download_multiple_images_16_bit_forward_backward,download_image, download_multiple_images, get_request_individual, get_folder_ID_optimized

import random
print("SentinelHub imports - passed")

def clean_blank_folders(year, img_format):
    """
    Remove folders containing blank or empty images for a specified year and image format.

    Parameters:
    - year (str): The year for which blank folders should be cleaned.
    - img_format (str): The image format (e.g., 'png', 'tiff') of the blank images.

    Note:
    This function assumes that blank images are identified by the presence of a file
    named 'response.{img_format}' within each folder. Folders containing such images
    will be recursively removed.

    Example:
    clean_blank_folders('2023', 'png')

    This example will remove all folders containing blank PNG images within the '2023' directory.

    Caution:
    Use this function with care as it permanently deletes folders and their contents.
    """
    path_to_blank_ids = f"./data/{year}/*/*response.{img_format}"
    ids = glob.glob(path_to_blank_ids)
    for idx in ids:
        folder_p = os.path.dirname(idx)
        shutil.rmtree(folder_p)

def get_images(coordinates, city_str, current_coor, years, weeks, img_format, root_images, CLIENT_ID, CLIENT_SECRET):
    """
    Download and organize satellite images for a specified city and time range.

    Parameters:
    - coordinates (tuple): Geographic coordinates (latitude, longitude) of the target location.
    - city_str (str): Unique identifier or name for the city.
    - current_coor (tuple): Current coordinates (latitude, longitude) for image retrieval.
    - years (list): List of years for which images should be downloaded.
    - weeks (list): List of weeks within each year for image retrieval.
    - img_format (str): Image format (e.g., 'png', 'jpg') for downloaded images.
    - root_images (str): Root directory for storing downloaded images.
    - CLIENT_ID (str): Client ID for accessing the satellite imagery API.
    - CLIENT_SECRET (str): Client secret for accessing the satellite imagery API.

    Note:
    This function iterates through specified years and weeks, downloads satellite images,
    organizes them into folders, renames images based on JSON timestamp filters, and removes
    folders containing blank images.

    Example:
    get_images(
        coordinates=(latitude, longitude),
        city_str='example_city',
        current_coor=(latitude, longitude),
        years=[2022, 2023],
        weeks=range(1, 53),
        img_format='png',
        root_images='./data',
        CLIENT_ID='your_client_id',
        CLIENT_SECRET='your_client_secret'
    )

    This example will download and organize satellite images for 'example_city' from 2022 to 2023.

    Caution:
    Ensure the provided CLIENT_ID and CLIENT_SECRET are valid and authorized to access the satellite imagery API.
    """

    folder_path = ""
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
        
        current_coor = [float(value) for value in row['coordinates'][1:-1].split(',')]
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

# cred = pd.read_csv("/Users/sebasmos/Desktop/satellite.extractor/satellite_extractor/satellite-extractor-dockerized/data_config/SentinelHub-credentials.csv")
# CLIENT_ID = str(cred.iloc[0,:][0])
# CLIENT_SECRET = str(cred.iloc[1,:][0])
# LATITUDE = 3.4400
# LONGITUDE= -76.5197
# TIMESTAPS = [2016,2018]
# # projection = CRS.WGS84
# IMAGE_FORMAT = "tiff"
# CODE = 5555
# LENGTH = 750
# RESOLUTION = 10
# COORDINATES_PATH = "/Users/sebasmos/Desktop/satellite.extractor/data/10_municipalities_full.csv"
# service_account = 'ee-account@mit-hst-dengue.iam.gserviceaccount.com'
# sat.run(TIMESTAPS, CLIENT_ID, CLIENT_SECRET, IMAGE_FORMAT, COORDINATES_PATH )
