FROM python:latest
## The MAINTAINER instruction sets the author field of the generated images.
MAINTAINER ulsordonez@unicauca.edu.co
RUN apt-get -y update && apt install --no-install-recommends -y python3-dev wget git curl nano
#--------------------- START GCLOUD CONFIG--------------------------------------------
# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

#--------------------- END GCLOUD CONFIG--------------------------------------------
COPY . Dengue/

RUN /bin/bash  -c "cd Dengue && pip install -r requirements.txt && python coordinate_extraction.py"
#RUN /bin/bash -c "git config --global --unset http.proxy && git config --global --unset https.proxy"
#---------------------START SentinelHub CONFIG--------------------------------------------
RUN /bin/bash -c "cd Dengue && pip install -r requirements.txt && git clone https://github.com/sentinel-hub/sentinelhub-py.git && cd sentinelhub-py && pip install -r requirements.txt && python setup.py build && python setup.py install"
#---------------------START SentinelHub CONFIG--------------------------------------------
# Run everything during compilation
RUN cd Dengue/ && chmod +x ./satellite.extractor.sh && bash -c "./satellite.extractor.sh"
# Run separately
#RUN cd Dengue/ && chmod +x ./satellite.extractor.sh"

