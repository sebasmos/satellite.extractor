FROM python:latest
## The MAINTAINER instruction sets the author field of the generated images.
MAINTAINER ulsordonez@unicauca.edu.co
#COPY requirements.txt ./
#COPY utils.py ./Dengue/
#CMD ["python", "./utils.py"]
RUN apt-get -y update && apt install --no-install-recommends -y python3-dev wget git curl nano
#--------------------- START GCLOUD CONFIG--------------------------------------------
# Downloading gcloud package
#RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
#RUN curl -sSL https://sdk.cloud.google.com | bash
#ENV PATH $PATH:/root/google-cloud-sdk/bin
#RUN /bin/bash  -c "cd Dengue && pip install -r requirements.txt && python coordinate_extraction.py"
#--------------------- END GCLOUD CONFIG--------------------------------------------
COPY . Dengue/
#RUN /bin/bash -c "git config --global --unset http.proxy && git config --global --unset https.proxy"
#---------------------START SentinelHub CONFIG--------------------------------------------
RUN /bin/bash -c "cd Dengue && pip install -r requirements.txt && git clone https://github.com/sentinel-hub/sentinelhub-py.git && cd sentinelhub-py && pip install -r requirements.txt && python setup.py build && python setup.py install"
#---------------------START SentinelHub CONFIG--------------------------------------------
#RUN /bin/bash -c "bash ./Dengue/satellite.extractor.sh"
RUN cd Dengue/ && chmod +x ./satellite.extractor.sh  && bash -c "./satellite.extractor.sh"
#    && pip install -r requirements.txt \
#    && chmod +x ./satellite.extractor.sh \
    #&& ./satellite.extractor.sh
