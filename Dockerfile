#FROM python:3.8.9-buster
FROM tensorflow/tensorflow:2.4.1-gpu-jupyter 

## The MAINTAINER instruction sets the author field of the generated images.
MAINTAINER ulsordonez@unicauca.edu.co

## DO NOT EDIT the 3 lines.
RUN mkdir /sebasmos
COPY ./ /sebasmos
WORKDIR /sebasmos

## Install your dependencies here using apt install, etc.

## Include the following line if you have a requirements.txt file.
RUN pip install -r requirements.txt
