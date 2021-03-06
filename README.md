# Satellite extractor

Satellite extractor allows to download satellite imagery on any coordinates and fixed timestamps. Do not expect perfect images, there is cloud interefence to be filtered out. 

The developed API is used to mantain [MIT Critical data](https://github.com/MITCriticalData-Colombia) Dengue projects.

<hr>

## Working locally

1. Clone repository and install dependencies in `pip install -r requirements.txt`

2. Create account on Sentinelhub to obtain [credentials](https://apps.sentinel-hub.com/dashboard/#/): 

3. Install sentinelhub API: 

    `pip install sentinelhub` if any errors then: `pip install sentinelhub --upgrade`

    or manually:

    `git clone https://github.com/sentinel-hub/sentinelhub-py.git`

    `cd sentinelhub-py`to contact me

    ` python setup.py build`

    ` python setup.py install`

    ` cd ..`

    ` pip install -r requirements.txt`
to contact me
    For more information, refer to [official documentation](https://sentinelhub-py.readthedocs.io/en/latest/install.html).

<hr>

## About the satellite data - notebook examples

The data collected is from 2015-2018.
All the data including a huge amount of images will be hosted on Google Cloud Platform and
on Oracle Data Storage. We developed the code to access the API and create our own dataset
for RGB and 12 bands ( B01, B04, B03, B02, B05, B06, B07, B08, B09, B10, B11, B12 ), which
can be downloaded using the following code here.

* Satellite images can be customized. Notebooks examplify the case for [sentinel-hub](https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l1c/), (with 5 days re-visiting time), which is a European wide-swath,
high-resolution, multi-spectral imaging mission.

* Sampled weekly based on epiweek

* Data is stored in TIFF format, containing 12 bands from Sentinel SENTINEL2_L1C, resolution
set to 10 metres

* (1024, 1024) pixels per image - customizable


* Images based on Epiweek clouds are avoided using the LeastCC algorithm, which is
configured using sentinel-hub API as a script request to select the image with the least
amount of clouds per epi week. It uses the satellite metadata to fetch the days in mosaicking
order in terms of the least amount of clouds. This is done through the API and Geopedia,
which orders the images based on the amount of captured features per 12 000 sq km. There
is [here](https://github.com/sentinel-hub/sentinelhub-py/blob/23f267db476d26ddf76a2076a4f9a1d81bd9e31d/tests/test_ogc.py) an example of how they do it.

* Google drive works like a local hard drive to store the images. However this could be done
on any virtual machine as the code uses the Sentinel API to create, modify, copy and delete
multiple folders with the package shutil, then storing all pre-processed
images with the right format into a single folder called DATASETS, ultimately moved to GCP. In
an alternative pipeline we could e.g , download all images on a GCP bucket or on an Oracle
bucket instead of using Google drive or GCP at al

<hr>


## Data per year 

Based on [epi week](https://www.cmmcp.org/mosquito-surveillance-data/pages/epi-week-calendars-2008-2021)

* 2016: (2016,1,3) - (2016,12,31)

* 2017: (2017,1,1) - (2017,12,30) 

* 2018: (2018,12,30) - (2018,12,29). First week from (2018,1,1) - (2018,1,6)

* 2019: (2018,12,29) to end first week the (2019,1,5), end (2019,12,31)

* 2020: (2019,12,28) to end first week the  (2020,1,4), end (2019,12,31)

* 2021: (2020,12,26) to end first week the  (2021,1,2), end (2021,9,8)

## Use cases:

1. [Read GCP bucket to Google Colab](https://github.com/sebasmos/satellite.extractor/blob/main/Reading_GCP_from_Colab.ipynb)
2. [Download satellite data for 5 cities](https://github.com/sebasmos/satellite.extractor/blob/main/downloader_sentinel_5_cities.ipynb)
3. [Download satellite data for 1024 cities](https://github.com/sebasmos/satellite.extractor/blob/main/downloader_sentinel_all_cities.ipynb)

## Contributions

Feel free to contact me if want to collaborate on this project.
