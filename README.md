# [Satellite extractor](https://eo4society.esa.int/wp-content/uploads/2023/06/towards-a-smart-eco-epidemiological-model-of-dengue-in-colombia-using-satellite.pdf): Access Satellite Imagery with Geographical and Temporal Control


*Satellite Extractor provides users with the capability to retrieve satellite imagery for specific geographical coordinates and predefined timestamps. While it offers a powerful tool for accessing remote sensing data, it's important to note that the quality of the images may not always be perfect due to potential cloud interference, which users may need to filter or process as necessary.*. 

 
**Sentinelhub grant**: Sponsoring request ID 1c081a: Towards a Smart Eco-epidemiological Model of Dengue in Colombia using Satellite in Collaboration with [MIT Critical Data Colombia](https://github.com/MITCriticalData-Colombia).  
*Project supported by ESA Network of Resources Initiative*

Find the full open-opensource datasets in HuggingFace: [Link](https://huggingface.co/MITCriticalData)

<p align="left">
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.8-ff69b4.svg" /></a>
    <a href= "https://pytorch.org/">
      <img src="https://img.shields.io/badge/PyTorch-1.8-2BAF2B.svg" /></a>
    <a href= "https://github.com/sebasmos/vector-borne-satellite-predictor/blob/main/LICENCE">
      <img src="https://img.shields.io/badge/License-MIT-blue.svg" /></a>
</p>
<hr/>


**About this project**: In this work, we introduce a data collection and processing framework to extract Sentinel-2 satellite 1 based on modified Copernicus Sentinel data. Satellite images of the ten cities are extracted from sentinel 2 through the SentinelHub API using a scalable dockerized framework that orchestrates Google Earth Engine (GEE) to generate regions of interest (ROI), which are afterwards used to download images. The framework also proposes a recursive noise artifact removal algorithm that reduces camera capturing noise generated by Sentinel 2-L1C orbit transit per week. 


## Installation

```
pip install satellite-extractor
```


## Credentials

1. **Credentials for GCP**: Please follow the instructions as explained [here](https://developers.google.com/earth-engine/guides/service_account#use-a-service-account-with-a-private-key) and add update your credentials as follows.
      1. Inside of `src/satellite-extractor-dockerized/config.py`, update `service_account` with your new service account.
      1. Store the GCP json key inside of  `src/satellite-extractor-dockerized/data_config`  

1. **Credentials for SentinelHub**: The best of this project is that you can download data for free using the Free Tier from SentinelHub. Follow the instructions to create your username and password [here](https://docs.sentinel-hub.com/api/latest/api/overview/authentication/). Please remember it is a free trial, access is limited! 


## Docker pipeline

If you want to download data using docker,  please update the [config file](https://github.com/sebasmos/satellite.extractor/blob/main/src/satellite-extractor-dockerized/config.py) as desired and follow the next commands.

```
docker build -f Dockerfile -t docker .
```

Run with syncronized volume:

```
docker run -v /home/sebasmos/Desktop/satellite.extractor/src/satellite-extractor-dockerized:/Dengue -ti docker /bin/bash
```
Finally, run `python satellite.extractor.py` to download the satellites as customized.

## Working locally

1. Clone repository and install dependencies in `pip install -r requirements.txt`

1. Create account on Sentinelhub to obtain [credentials](https://apps.sentinel-hub.com/dashboard/#/): 

1. Install sentinelhub API, follow up the [official documentation](https://sentinelhub-py.readthedocs.io/en/latest/install.html).

<hr>

## Use cases:

1. [Read GCP bucket to Google Colab](https://github.com/sebasmos/satellite.extractor/blob/main/notebooks/Reading_GCP_from_Colab.ipynb)
1. [Download satellite data for 5 cities](https://github.com/sebasmos/satellite.extractor/blob/main/notebooks/downloader_sentinel_5_cities.ipynb)
1. [Download satellite data for 1024 cities](https://github.com/sebasmos/satellite.extractor/blob/main/notebooks/downloader_sentinel_all_cities.ipynb)
1. PART_1_satellite_imagery_augmentation: exploring forward artifact removal
1. PART_2_satellite_imagery_augmentation: exploring forward-backward artifcat removal
1. satellite_images_hashing: evaluate dataset quality by quantifying the number of duplicates on your data
1. viz_many_folders: explore the visualization of satellite images 
1. [create_Cloud2CloudlesDataset](https://github.com/sebasmos/satellite.extractor/blob/main/notebooks/create_Cloud2CloudlesDataset.ipynb): create cloud to cloudless paired image dataset

## Contributions

Feel free to contact me if want to collaborate on this project.

