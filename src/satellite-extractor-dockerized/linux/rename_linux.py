# -*- coding: utf-8 -*-

'''
Author: Sebastian Cajas
'''
################### Read JSON requests #########################

import pandas as pd
import glob
import json
import datetime as dt
#from urllib.parse import unquote
#from bs4 import BeautifulSoup
import os
import sys
import shutil
sys.path.insert(0,'..') 

def get_request_dt(request_file, img_format):
    with open(request_file, 'r') as req:
        json_decode = json.load(req)
        dataFilter = json_decode["payload"]["input"]["data"][0]
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
        os.rename(response_img, image_path)
        
        return df 


def get_request_individual(request_file, img_format):
    with open(request_file, 'r') as req:
        json_decode = json.load(req)
        dataFilter = json_decode["payload"]["input"]["data"][0]
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
    
'''
if __name__ == "__main__":
    folders = glob.glob('.\\data\\2015\\*')    
    get_request_dt((f'{folders[0]}\\request.json'),"tiff")
    #get_request_dt("/home/sebasmos/Desktop/Sentinel.Medellin/data/2016/00ce1973aab9a8d4327fa44a27eb5a74/request.json")
    dates = [get_request_dt(f'{folder}\\request.json', "tiff") for folder in folders]
'''